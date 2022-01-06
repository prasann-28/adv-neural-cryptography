import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from flask import Flask, render_template, request, redirect
from keras.models import load_model
import numpy as np
from helper import *


app = Flask(__name__)

alice = load_model('alice.h5')
bob = load_model('bob.h5')
eve = load_model('eve.h5')
block_padding= 11
block_size = 16

def processRawMessage(raw_message):
    encrypt = encstr(raw_message,block_padding)
    bin_cipher = strToArr(encrypt[0], block_size)
    bin_message = bin_cipher[0]
    bin_key = bin_cipher[1]

    return [bin_message,bin_key]

def processBinaryMessage(binary_message):
    message_str = arrToStr(binary_message)
    decipher = decstr(message_str,len(binary_message),block_padding) 
    return [decipher]

@app.route('/', methods=['GET', 'POST'])
def hello():
    cryp = []
    if request.method == 'POST':
        raw_message = request.form['alice_input']
        print(raw_message)
        messages = processRawMessage(raw_message)
        message = messages[0]
        key = messages[1]

        cipher = alice.predict([message,key])
        decipher = (bob.predict([cipher, key]) > 0.5).astype(int)
        adversary = (eve.predict(cipher) > 0.5).astype(int)

        plaintext = processBinaryMessage(decipher)
        adv = processBinaryMessage(adversary)
        
        cryp = [plaintext,adv]

    return render_template('home.html', cryp = cryp)

if __name__ == '__main__':
    app.run(debug=True)
