import os
import imghdr
from flask import Flask, render_template, request, redirect, url_for, abort
from flask.helpers import send_file
from werkzeug.utils import secure_filename
import pixellib
from pixellib.tune_bg import alter_bg

#INIT FLASK
app = Flask(__name__)

#FLASK CONFIG
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = 'images'

#VALIDATE IMAGE
def validate_image(stream):
    header = stream.read(512)
    stream.seek(0) 
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

#REMOVE BG FUNCTION
def removeBackground(filename):
    newname = 'images/' + filename
    change_bg = alter_bg()
    change_bg.load_pascalvoc_model("models/deeplabv3_xception_tf_dim_ordering_tf_kernels.h5")
    if '.png' in filename:
        filename.replace('.png', '.jpg')
    change_bg.change_bg_img(f_image_path = newname,b_image_path = "background.jpg", output_image_name=filename)
    #change_bg.blur_bg(newname, moderate = True, output_image_name=filename)

def removeBackgroundBlur(filename):
    newname = 'images/' + filename
    change_bg = alter_bg()
    change_bg.load_pascalvoc_model("models/deeplabv3_xception_tf_dim_ordering_tf_kernels.h5")
    if '.png' in filename:
        filename.replace('.png', '.jpg')
    change_bg.blur_bg(newname, moderate = True, output_image_name=filename)

def removeBackgroundColor(filename):
    newname = 'images/' + filename
    change_bg = alter_bg()
    change_bg.load_pascalvoc_model("models/deeplabv3_xception_tf_dim_ordering_tf_kernels.h5")
    if '.png' in filename:
        filename.replace('.png', '.jpg')
    change_bg.color_bg(newname, colors=(255, 255, 255), output_image_name=filename)

#HOME ROUTE
@app.route('/')
def index():
    return render_template('index.html')

#POST ROUTE FOR API
@app.route('/', methods=['POST'])
def upload_files():
    bgType = request.form['bg_type']
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))

    if bgType == 'color':
        removeBackgroundColor(filename)
    elif bgType == 'blur':
        removeBackgroundBlur(filename)
    else:
        removeBackground(filename)
    return send_file(filename, as_attachment=True)
    #return { "message": "Successfully Removed Background"}
    

app.run()


#Author: Bhupender Singh
#Github: @bhupenderlost ( https://github.com/bhupenderlost )
#Instagram: @bhupender___singh
