import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from flask import Flask, render_template, request, redirect, flash
from keras.models import load_model
from keras.preprocessing.image import img_to_array, load_img
import numpy as np
import base64
from werkzeug.utils import secure_filename

# Importing local helper.py for helper functions
from helper import *

UPLOAD_FOLDER = './received/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


alice = load_model('./models/alice.h5')
bob = load_model('./models/bob.h5')
eve = load_model('./models/eve.h5')
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
        # # if user does not select file, browser also
        # # submit a empty part without filename
        # if file.filename == '':
        #     # flash('No selected file')
        #     return redirect(request.url)
        # else:
        #     file.save('./uploads/' + file.filename)
        #     img = load_img('./uploads/' + file.filename)
        #     # image_list = img_to_array(img)
        #     image_str = processImageList(img.tobytes())
        #     processed_img = processRawMessage(str(image_str))
        #     img_bin = processed_img[0]
        #     img_key = processed_img[1]

        #     cipher_img = alice.predict([img_bin,img_key])
        #     decipher_img = (bob.predict([cipher_img, img_key]) > 0.5).astype(int)
        #     # print(img_bin==decipher_img)
        #     plaintext_img = processBinaryMessage(decipher_img)
        #     abnormalities = testEquality(str(image_str),plaintext_img)
        #     print(abnormalities)
        #     for i in range(len(plaintext_img)):
        #         if str(image_str)[i] != plaintext_img[i]:
        #             print('Original: ', str(image_str)[i]  )
        #             print('Decrypted: ', plaintext_img[i]  )
        #             print('Location: ', i)
            
        cryp = [plaintext,adv]

    return render_template('home.html', cryp = cryp)

if __name__ == '__main__':
    app.run(debug=True)

# from werkzeug.utils import secure_filename
# import base64
# from helper import *
# import numpy as np
# from keras.models import load_model
# import pyrebase
# from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
# import os
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# app = Flask(__name__)  # Initialze flask constructor

# # Add your own details
# config = {
#     "apiKey": "AIzaSyDUvIsdnl6O_JTr-jaWfUYOuGefSFRl7e0",
#     "authDomain": "neural-chat-f8456.firebaseapp.com",
#     "databaseURL": "https://neural-chat-f8456-default-rtdb.asia-southeast1.firebasedatabase.app/",
#     "storageBucket": "neural-chat-f8456.appspot.com"
# }

# # initialize firebase
# firebase = pyrebase.initialize_app(config)
# auth = firebase.auth()
# db = firebase.database()

# alice = load_model('models/alice.h5')
# bob = load_model('models/bob.h5')
# eve = load_model('models/eve.h5')
# block_padding = 11
# block_size = 16


# def processRawMessage(raw_message):
#     encrypt = encstr(raw_message, block_padding)
#     bin_cipher = strToArr(encrypt[0], block_size)
#     bin_message = bin_cipher[0]
#     bin_key = bin_cipher[1]

#     return [bin_message, bin_key]


# def processBinaryMessage(binary_message):
#     message_str = arrToStr(binary_message)
#     decipher = decstr(message_str, len(binary_message), block_padding)
#     return decipher


# def processRawFile(file):
#     converted_string = base64.b64encode(file.read())
#     return converted_string


# def processBinaryFile(img_text):
#     image_file = base64.b64decode(img_text)
#     return image_file


# # Initialze person as dictionary
# person = {"is_logged_in": False, "name": "", "email": "", "uid": ""}

# # Login


# @app.route("/")
# def login():
#     return render_template("login.html")

# # Sign up/ Register


# @app.route("/signup")
# def signup():
#     return render_template("signup.html")

# # Welcome page


# @app.route("/welcome")
# def welcome():
#     if person["is_logged_in"] == True:
#         return render_template("welcome.html", email=person["email"], name=person["name"])
#     else:
#         return redirect(url_for('login'))

# # If someone clicks on login, they are redirected to /result


# @app.route("/result", methods=["GET", "POST"])
# def result():
#     if request.method == "POST":  # Only if data has been posted
#         result = request.form  # Get the data
#         email = result["email"]
#         password = result["pass"]
#         print(email) 
#         print(password)
#         try:
#             # Try signing in the user with the given information
#             print("inside try")
#             user = auth.sign_in_with_email_and_password(email, password)
#             print("user created")   
#             # Insert the user data in the global person
#             global person
#             person["is_logged_in"] = True
#             person["email"] = user["email"]
#             person["uid"] = user["localId"]
#             # Get the name of the user
#             print("person created")
#             data = db.child("users").get()
#             print(data)
#             person["name"] = data.val()[person["uid"]]["name"]
#             # Redirect to welcome page
#             return redirect(url_for('home'))
#         except:
#             # If there is any error, redirect back to login
#             return redirect(url_for('login'))
#     else:
#         if person["is_logged_in"] == True:
#             return redirect(url_for('home'))
#         else:
#             return redirect(url_for('login'))

# # If someone clicks on register, they are redirected to /register


# @app.route("/register", methods=["POST", "GET"])
# def register():
#     if request.method == "POST":  # Only listen to POST
#         result = request.form  # Get the data submitted
#         email = result["email"]
#         password = result["pass"]
#         name = result["name"]
#         try:
#             # Try creating the user account using the provided data
#             auth.create_user_with_email_and_password(email, password)
#             # Login the user
#             user = auth.sign_in_with_email_and_password(email, password)
#             # Add data to global person
#             global person
#             person["is_logged_in"] = True
#             person["email"] = user["email"]
#             person["uid"] = user["localId"]
#             person["name"] = name
#             # Append data to the firebase realtime database
#             data = {"name": name, "email": email}
#             db.child("users").child(person["uid"]).set(data)
#             # Go to welcome page
#             return redirect(url_for('home'))
#         except:
#             # If there is any error, redirect to register
#             return redirect(url_for('register'))

#     else:
#         if person["is_logged_in"] == True:
#             return redirect(url_for('home'))
#         else:
#             return redirect(url_for('register'))


# @app.route('/home', methods=['GET', 'POST'])
# def home():
#     cryp = []
#     if request.method == 'POST':
#         raw_message = request.form['alice_input']
#         # print(raw_message)
#         messages = processRawMessage(raw_message)
#         message = messages[0]
#         key = messages[1]

#         cipher = alice.predict([message, key])
#         decipher = (bob.predict([cipher, key]) > 0.5).astype(int)
#         adversary = (eve.predict(cipher) > 0.5).astype(int)

#         plaintext = processBinaryMessage(decipher)
#         adv = processBinaryMessage(adversary)
#         '''
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # if user does not select file, browser also
#         # submit a empty part without filename
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         else:
#             filename = secure_filename(file.filename)
#             img_str = processRawFile(file)
#             # print(img_str)
#             img_messages = processRawMessage(str(img_str))
#             img = img_messages[0]
#             img_key = img_messages[1]
#             cipher = alice.predict([img, img_key])
#             decipher = (bob.predict([cipher, img_key]) > 0.5).astype(int)
#             adversary = (eve.predict(cipher) > 0.5).astype(int)
#             # img_plaintext = processBinaryMessage(decipher)
#             # img_adv = processBinaryMessage(adversary)
#             # print(img_plaintext == img_str)
#             # plaintext_img = processBinaryFile(img_plaintext)
#             # adversary_img = processBinaryFile(img_adv)
#             # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))'''

#         cryp = [plaintext, adv]

#     return render_template('home.html', cryp=cryp)


# if __name__ == "__main__":
#     app.run(debug=True)