# Input format

# !pip3 install joblib

# load_model works with Python 3.6.13 :: Anaconda, Inc.
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# import joblib
from keras.models import load_model
import numpy as np


alice1 = load_model('alice.h5')
bob1 = load_model('bob.h5')
eve1 = load_model('eve.h5')

message = np.array([[0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1],
                    [1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1]])
key = np.array([[0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1],
                [0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1]])

cipher = alice1.predict([message, key])

decipher = (bob1.predict([cipher, key]) > 0.5).astype(int)

adversary = (eve1.predict(cipher) > 0.5).astype(int)

print(cipher[0])
print(decipher[0])
print(adversary[0])
