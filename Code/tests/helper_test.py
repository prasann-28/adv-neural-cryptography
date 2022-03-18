# Imports helper.py for testing purposes
from email.mime import image
from helper import *
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from keras.models import load_model
from matplotlib.pyplot import imshow

message = 'hello world'

# Block padding and size to be kept constant
block_padding= 11
block_size = 16

# Encryption of message and key generation and binary conversion
encrypt = encstr(message,block_padding)
print(encrypt)
bin_ciph = strToArr(encrypt[0], block_size)

alice = load_model('alice.h5')

bin_message = bin_ciph[0]
bin_key = bin_ciph[1]

# Alice's prediction
cipher = alice.predict([bin_message, bin_key])

bob  = load_model('bob.h5')
eve = load_model('eve.h5')

# Bob and Eve decryption test
bob_pred = (bob.predict([cipher, bin_key]) > 0.5).astype(int)
eve_pred = (eve.predict(cipher) > 0.5).astype(int)

bob_str = arrToStr(bob_pred)
eve_str = arrToStr(eve_pred)
decipher = decstr(bob_str,len(message),block_padding)
adversary = decstr(eve_str,len(message),block_padding)

print('Bob: ', decipher)
print('Eve: ',adversary)

print(len(bob_pred))

image = 'test1'
ext = '.png'
im_mat = getImageMatrix(imageName=image+ext)
print(im_mat)
LogisticEncryption(image+ext, "keykeykeykeykey")
LogisticDecryption(image + "_LogisticEnc.png", "keykeykeykeykey")


