import os
# import face_recognition as fr
from flask import Flask, render_template,request, redirect, url_for, jsonify
import time

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join('static','faces')
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.jpeg', '.png', '.bmp']

# # initial page
# @app.route('/')
# def index():
#     return render_template('index.html')

# after file submition, recognize face and gives answer
def recognize(filename):
    # time.sleep(3)
    # ans, name = fr.test_face(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    # ans = "Autorizado" if ans else "Não Autorizado"
    ans = "Autorizado"
    name = "Gabriel"
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    flag = 1 if full_filename else 0
    return jsonify({'ans': ans}) if flag else jsonify({'ans': 'no'})
    # return render_template('recognize.html', ans=ans, name=name, filename=filename)

# saves uploaded image and call recognize function
@app.route('/', methods=['POST'])
def upload_img():
    img = request.files['image']
    if img.filename != '':
        file_ext = os.path.splitext(img.filename)[1]
        if file_ext in app.config['UPLOAD_EXTENSIONS']:
            full_filename = os.path.join(app.config['UPLOAD_FOLDER'], img.filename)
            img.save(full_filename)
            return recognize(full_filename)
    return 'Error in image processing'

if __name__ == "__main__":
    app.run(debug=True)