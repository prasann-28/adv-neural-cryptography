from flask import Flask, render_template, request, redirect
from keras.models import load_model
import numpy as np


app = Flask(__name__)

@app.route('/')
def hello():
    
    return render_template('home.html', cryp=cryp)

if __name__ == '__main__':
    app.run(debug=True)