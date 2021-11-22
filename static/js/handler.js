/* Opens filesystem. */
 document.getElementById("add-image").onclick = function() {
     document.getElementById("upload-image").click();
 };

 /* Previews image. */
 document.getElementById("upload-image").onchange = function() {
     var file = this.files[0];

     if (['image/jpeg', 'image/png'].indexOf(file.type) != -1)
         document.getElementById("span-image").outerHTML =
                 '<img id="span-image" class="dim-img" src="' + URL.createObjectURL(file) + '">';
     else
         document.getElementById("messages").innerHTML =
                  '<div class="alert alert-warning alert-dismissible">' +
                  '<a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>' +
                  'Unsupported File Format. <strong>Supported Image File Formats:</strong> PNG(.png), JPEG(.jpg, .jpeg).' +
                  '</div>';

 };

/*
 *  Sends data and displays the received synthesized image.
 */
function transferStyle() {
    const fd = new FormData(document.forms["form-data"]);

    if (!fd.get('image') || !fd.get('style'))
       document.getElementById('messages').innerHTML =
                 '<div class="alert alert-warning alert-dismissible">' +
                 '<a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>' +
                 'Image or Style Not Found. Upload the missing one or check both, and try again.' +
                 '</div>';
    else {
        document.getElementById('transfer-img').innerHTML =
                '<img id="span-style-" class="icon-loading" src="/static/images/loading.gif" alt="">';

        let xhr = new XMLHttpRequest({mozSystem: true});
        xhr.open('POST', 'https://flaskserver-gjcbyup5ka-uc.a.run.app', true);
        xhr.responseType = "blob";

        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                if(xhr.response.type == 'image/png') {
                    document.getElementById('transfer-img').innerHTML =
                             '<img class="dim-img" src="' + URL.createObjectURL(xhr.response) + '">';
                }
                else {
                    document.getElementById('transfer-img').innerHTML =
                             '<span id="transfer-img"><div class="icon-fake"></div></span>';

                    document.getElementById('messages').innerHTML =
                             '<div class="alert alert-danger alert-dismissible">' +
                             '<a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>' +
                             'Internal Server Error.' +
                             '</div>';
                }
            }
        }

        xhr.onload = function() {};
        xhr.send(fd);
    }
};
