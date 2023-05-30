import os
# import face_recognition as fr
from flask import Flask, render_template,request, redirect, url_for, jsonify
import time

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join('static','faces')
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.jpeg', '.png', '.bmp']

# # initial page
@app.route('/')
def index():
    return render_template('index.html')

def delete_old_files():
    cur_time = time.time()
    directory = app.config['UPLOAD_FOLDER']
    two_days = 2*24*60*60
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if cur_time - os.path.getmtime(f) >= two_days:
            os.remove(f)

# after file submition, recognize face and gives answer
def recognize(filename, origin):
    # time.sleep(3)
    # ans, name = fr.test_face(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    # ans = "Autorizado" if ans else "Não Autorizado"
    
    ans = "Autorizado"
    name = "Gabriel"
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    flag = 1 if full_filename else 0
    
    # Após obter resultado, deleto arquivos antigos
    delete_old_files()
    
    if origin == "http://127.0.0.1:5000":
        return render_template('recognize.html', ans=ans, name=name, filename=filename)
    return jsonify({'name': name, 'ans': ans}) if flag else jsonify({'ans': 'no'})

# saves uploaded image and call recognize function
@app.route('/send-file', methods=['POST'])
def upload_img():
    try:
        img = request.files['file']
    except:
        return 'Error in image processing'
    if img.filename != '':
        file_ext = os.path.splitext(img.filename)[1]
        if file_ext in app.config['UPLOAD_EXTENSIONS']:
            full_filename = os.path.join(app.config['UPLOAD_FOLDER'], img.filename)
            img.save(full_filename)
            return recognize(full_filename, request.origin)
    return 'Error in image processing'

if __name__ == "__main__":
    app.run(debug=True)