from flask import  Flask, request, flash, render_template, redirect, send_file, send_from_directory
from werkzeug.utils import secure_filename
import os
import io
import base64
import ntpath
from PIL import Image

app = Flask(__name__)

RUTA_DATASET = "datasets/images/"
RUN_MONET = 'python runModel.py --dataroot datasets/images --name style_monet_pretrained --model test --no_dropout'
RUN_CEZANNE = 'python runModel.py --dataroot datasets/images --name style_cezanne_pretrained --model test --no_dropout'
RUN_UKIYOE = 'python runModel.py --dataroot datasets/images --name style_ukiyoe_pretrained --model test --no_dropout'
RUN_VANGOGH = 'python runModel.py --dataroot datasets/images --name style_vangogh_pretrained --model test --no_dropout'

def whoName(i):
    if i == "style_monet":
        return "Estilo de Monet"
    elif i == "style_cezanne":
        return "Estilo de Cezanne"
    elif i == "style_ukiyoe":
        return "Estilo de Ukiyoe"
    else:
        return "Estilo de Van Gogh"

def transferStyle(imagefile,filename,style):
    os.chdir('pytorch-CycleGAN-and-pix2pix-master/')
    os.system('rm -r datasets/images/*')
    #os.system('rm -r results/style_monet_pretrained/test_latest/images/*')
    print("\nSe ha recibido la siguiente imagen : " + imagefile.filename)
    imagefile.save(RUTA_DATASET + filename)

    if style == "style_monet":
        os.system(RUN_MONET)
    elif style == "style_cezanne":
        os.system(RUN_CEZANNE)
    elif style == "style_ukiyoe":
        os.system(RUN_UKIYOE)
    else:
        os.system(RUN_VANGOGH)
    os.chdir('../')


@app.route('/', methods = ['GET', 'POST'])
def handle_request():
    if request.method == 'GET':
        return render_template("home.html")
    else:
        if 'image' not in request.files or 'style' not in request.form:
            flash('No image or style found.')
            return redirect(flask.request.url)

        imagefile = request.files['image']
        if imagefile.filename == '':
            flash('Empty image.')
            return redirect(request.url)

        _, extension = os.path.splitext(secure_filename(imagefile.filename))
        if extension.lower() in [".jpeg", ".jpg", ".png"]:
            style = request.form['style']
            filename = secure_filename(imagefile.filename)
            transferStyle(imagefile,filename,style)

            filename = filename.split(".")[0]
            imFake = Image.open('pytorch-CycleGAN-and-pix2pix-master/results/' + filename + '_' + style +  '.png')
            dataFake = io.BytesIO()
            imFake.save(dataFake, "PNG")
            dataFake.seek(0)

            return send_file(dataFake,mimetype='image/PNG')

        flash('Unsupported File Format. Supported Image File Formats: PNG(.png), JPEG(.jpg, .jpeg).')
        return redirect(request.url)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
