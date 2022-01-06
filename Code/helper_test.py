from helper import *
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from keras.models import load_model


message = 'hello world'
block_padding= 11
block_size = 16

encrypt = encstr(message,block_padding)
bin_ciph = strToArr(encrypt[0], block_size)

alice = load_model('alice.h5')

bin_message = bin_ciph[0]
bin_key = bin_ciph[1]

cipher = alice.predict([bin_message, bin_key])

bob  = load_model('bob.h5')
eve = load_model('eve.h5')

bob_pred = (bob.predict([cipher, bin_key]) > 0.5).astype(int)
eve_pred = (eve.predict(cipher) > 0.5).astype(int)

bob_str = arrToStr(bob_pred)
eve_str = arrToStr(eve_pred)
decipher = decstr(bob_str,len(message),block_padding)
adversary = decstr(eve_str,len(message),block_padding)

print('Bob: ', decipher)
print('Eve: ',adversary)

print(len(bob_pred))



