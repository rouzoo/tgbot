import cv2
import os
import subprocess
import numpy as np
import yaml


with open('./config.yml') as file:
        config = yaml.safe_load(file)

token = config['token']
photos = (config['photo_path'] , '/photo_')
voices = (config['voice_path'] , '/audio_message_')

faceCascade = cv2.CascadeClassifier( 'haarcascade_frontalface_alt.xml' )

def concatIdWithPhoto(user_id):
    return f'{photos[0]}{user_id}'

def concatIdWithVoice(user_id):
    return f'{voices[0]}{user_id}'

def setUp():
    os.makedirs(photos[0], exist_ok=True)
    os.makedirs(voices[0], exist_ok=True)

def countFiles(path):
    return sum(
        os.path.isfile(os.path.join(path, f)) for f in os.listdir(path)
    )

def savePhoto(user_id, name, number):
    directory = concatIdWithPhoto(user_id)
    os.makedirs(directory, exist_ok=True)

    path = generatePath('photo', user_id, number)
    path = f'{path}.jpg'

    with open(path, 'wb') as new_file:
        new_file.write(name)

def saveVoice(user_id, name, number):
    directory = concatIdWithVoice(user_id)
    os.makedirs(directory, exist_ok=True)

    path = generatePath('voice', user_id,number)
    path = f'{path}.ogg'

    with open(path, 'wb') as new_file:
        new_file.write(name)        

def faceRecognition(img):
    nparr = np.fromstring(img, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    faces = faceCascade.detectMultiScale(img_np, scaleFactor=1.1, minNeighbors=4, minSize=(30, 30))

    return len(faces)

def isFace(img):
    return faceRecognition(img)

def generatePath(f_type, user_id, number):
    if f_type == 'photo' :
        return f'{photos[0]}{user_id}{photos[1]}{number}'
    elif f_type == 'voice' :
        return f'{voices[0]}{user_id}{voices[1]}{number}'
    else:
        raise RuntimeError(f'Invalid f_type provided. Expect photo or voice but "{f_type}" found')

def oggToWav(path):
    cmd = 'ffmpeg  -hide_banner -loglevel panic -i ' +path + '.ogg -ar 16000 '+path + '.wav'
    subprocess.call(cmd)
    os.remove(f'{path}.ogg')
