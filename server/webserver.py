import os
# import face_recognition as fr
from flask import Flask, render_template, request
from facetest import Conv_network
import numpy as np
from PIL import Image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join('static','faces')
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.jpeg', '.png', '.bmp']

# initial page
@app.route('/')
def index():
    return render_template('index.html')

def delete_old_files():
    directory = app.config['UPLOAD_FOLDER']
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        os.remove(f)

# after file submition, recognize face and gives answer
def recognize(filename, origin):
    result = network.predict_face(filename)
    print(result)
    # Após obter resultado, deleto arquivos antigos
    delete_old_files()
    print(origin)
    if origin != 'arduino':
        return render_template('recognize.html', ans=result, filename=filename)
    return result["result"] == "Approved"
    # return jsonify({'name': name, 'ans': ans}) if flag else jsonify({'ans': 'no'})

@app.route('/oi', methods=['GET'])
def oi():
    return "oi"

@app.route('/receive-img', methods=['POST'])
def receive_img():
    print("oi")
    r = request
    print(f"len of r.data = {len(r.data)}")
    nparr = np.frombuffer(r.data, np.uint8)
    mat = np.reshape(nparr, (240, 320))
    img = Image.fromarray(mat, 'L')
    print(img)
    dirname = '\\'.join(os.path.dirname(__file__).split("/"))
    full_filename = os.path.join(dirname, app.config['UPLOAD_FOLDER'], 'image.png')
    print(full_filename)
    img.save(full_filename)
    return recognize(full_filename, 'arduino')

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
    network = Conv_network(224, 224)
    app.run(host='0.0.0.0', port=5000, debug=True)