from flask import Flask, render_template, request, redirect
from keras.models import load_model
import numpy as np


app = Flask(__name__)

alice1 = load_model('alice.h5')
bob1 = load_model('bob.h5')
eve1 = load_model('eve.h5')


@app.route('/')
def hello():
    
    message = np.array([[0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1],
                    [1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1]])
    key = np.array([[0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1],
                [0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1]])

    cipher = alice1.predict([message, key])
    decipher = (bob1.predict([cipher, key]) > 0.5).astype(int)
    adversary = (eve1.predict(cipher) > 0.5).astype(int)

    cryp = [cipher, decipher, adversary]

    return render_template('home.html', cryp = cryp)

if __name__ == '__main__':
    app.run(debug=True)
