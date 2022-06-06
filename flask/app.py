import os
from distutils.log import debug
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image, ImageOps

UPLOAD_FOLDER = './images'
DEFAULT_SIZE = 1024

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'43#FFI304A92348AZyohuwsfdaAFF'

CORS(app)

@app.route('/api/upload', methods=['POST'])
def upload_file():

    if request.method == 'POST':
        if 'upload_file' not in request.files:
            return 'there is no upload_file in form!'

        file1 = request.files['upload_file']
        os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], os.path.dirname(file1.filename) ), exist_ok=True)
        path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)

        file2 = resize_image(file1)
        file2.save(path)
        return path
    else:
        return '''
        <h1>Upload new File</h1>
        <form method="post" enctype="multipart/form-data">
        <input type="text" name="group">
        <input type="file" name="upload_file">
        <input type="submit">
        </form>
        '''
def resize_image(in_img):

    img1 = Image.open(in_img)
    img = ImageOps.exif_transpose(img1)
    
    ratio_width = img.width / DEFAULT_SIZE if img.width > DEFAULT_SIZE else 1
    ratio_height = img.height / DEFAULT_SIZE if img.height > DEFAULT_SIZE else 1
    ratio = ratio_width if ratio_height < ratio_width else ratio_height

    if ratio > 1 :
        img_resize = img.resize((int(img.width/ratio), int(img.height/ratio)))
        return img_resize
    else:
        return in_img

if __name__ == '__main__':

    app.run()