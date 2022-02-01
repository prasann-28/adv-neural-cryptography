import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from flask import Flask, render_template, request, redirect, flash
from keras.models import load_model
import numpy as np
import base64
from werkzeug.utils import secure_filename

# Importing local helper.py for helper functions
from helper import *

UPLOAD_FOLDER = './received/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


alice = load_model('alice.h5')
bob = load_model('bob.h5')
eve = load_model('eve.h5')
block_padding= 11
block_size = 16


@app.route('/', methods=['GET', 'POST'])
def hello():
    cryp = []
    if request.method == 'POST':
        raw_message = request.form['alice_input']
        # print(raw_message)
        messages = processRawMessage(raw_message)
        message = messages[0]
        key = messages[1]

        cipher = alice.predict([message,key])
        decipher = (bob.predict([cipher, key]) > 0.5).astype(int)
        adversary = (eve.predict(cipher) > 0.5).astype(int)

        plaintext = processBinaryMessage(decipher)
        adv = processBinaryMessage(adversary)

        # if 'file' not in request.files:
        #     flash('No file part')
        #     return redirect(request.url)
        # file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        # if file.filename == '':
        #     flash('No selected file')
        #     return redirect(request.url)
        # else:
        #     filename = secure_filename(file.filename)
        #     img_str = processRawFile(file)
        #     # print(img_str)
        #     img_messages = processRawMessage(str(img_str))
        #     img = img_messages[0]
        #     img_key = img_messages[1]

        #     cipher = alice.predict([img,img_key])
        #     decipher = (bob.predict([cipher, img_key]) > 0.5).astype(int)
        #     adversary = (eve.predict(cipher) > 0.5).astype(int)

        #     img_plaintext = processBinaryMessage(decipher)
        #     img_adv = processBinaryMessage(adversary)       

        #     print(img_plaintext == img_str)     

        #     # plaintext_img = processBinaryFile(img_plaintext)
        #     # adversary_img = processBinaryFile(img_adv)
        
        #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        cryp = [plaintext,adv]

    return render_template('home.html', cryp = cryp)

if __name__ == '__main__':
    app.run(debug=True)
