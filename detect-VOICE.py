import numpy as np
import cv2
import matplotlib as mpimp
import os
import winsound
import base64
import glob
import json
import requests
from gtts import gTTS
'''from gtts import gTTS

def sound():
    mytext = 'Pay attention it s a danger !'
    language = 'en'
    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj.save("danger.mp3")
    os.system("danger.mp3")
    return 0
'''
def sound(object):
    mytext = object
    language = 'en'

    # Passing the text and language to the engine,
    # here we have marked slow=False. Which tells
    # the module that the converted audio should
    # have a high speed
    myobj = gTTS(text=mytext, lang=language, slow=False)

    myobj.save("danger.mp3")

    # Playing the converted file
    #os.system("mpg321 danger.mp3")
    os.startfile('danger.mp3')

    return 0
# If you are using a Jupyter notebook, uncomment the following line.
#%matplotlib inline
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

# Replace <Subscription Key> with your valid subscription key.
subscription_key = "df3821039a5f4f5a885d487b4016051f"
assert subscription_key


cap = cv2.VideoCapture(0)

def process(img):
    vision_base_url = "https://eastus2.api.cognitive.microsoft.com/vision/v2.0/"

    analyze_url = vision_base_url + "analyze"

    # Set image_path to the local path of an image that you want to analyze.
    image_path = "picture/pic1.jpg"

    # Read the image into a byte array
    image_data = open(image_path, "rb").read()
    headers = {'Ocp-Apim-Subscription-Key': subscription_key,
               'Content-Type': 'application/octet-stream'}
    # params     = {'visualFeatures': 'Categories,Description,Color,Objects'}
    params = {'visualFeatures': 'Objects'}
    response = requests.post(
        analyze_url, headers=headers, params=params, data=image_data)
    print(response)
    response.raise_for_status()

    # The 'analysis' object contains various fields that describe the image. The most
    # relevant caption for the image is obtained from the 'description' property.
    analysis = response.json()
    print(analysis)

    y = json.dumps(analysis)
    y1 = json.loads(y)
    for object in y1['objects']:
        print(object['object'])
        print(object['rectangle']['w'] * object['rectangle']['h'])
    return y1

ret, img = cap.read()

cv2.imwrite('picture\pic1.jpg', img)
y1 = process(img)

while (True):
    ret, img = cap.read()
    cv2.imwrite('picture\pic1.jpg', img)

    y2=process(img)

    for object1 in y1['objects']:
            for object2 in y2['objects']:
                if (object1['object'] == object2['object']):
                        print((object1['rectangle']['w'] * object1['rectangle']['h']) / (object2['rectangle']['w'] * object2['rectangle']['h']))
                if(object1['object']== object2['object'] and
                        (object1['rectangle']['w'] * object1['rectangle']['h'])/(object2['rectangle']['w'] * object2['rectangle']['h']) < 0.9):
                   sound(object1['object'])

                    #winsound.Beep(2500, 1000)


    y1 = y2

