from tensorflow.keras.models import load_model
import numpy as np

mess = np.array([[0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1],
                    [1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1]])
key = np.array([[0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1],
                [0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1]])


alice1 = load_model('alice.h5')
bob1 = load_model('bob.h5')
eve1 = load_model('eve.h5')

print(bob1.predict([mess, key]))
