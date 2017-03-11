from __future__ import print_function
import time
import requests
import cv2
import operator
import numpy as np
import os
import RPi.GPIO as GPIO
import picamera

#if no people in all 3 pictures
#? reset values of emo

GPIO_TRIGGER = 23
GPIO_ECHO = 24

camera = picamera.PiCamera()
camera.resolution=(640,480)


# Import library to display results
import matplotlib.pyplot as plt# Display images within Jupyter


# In[12]:

# Variables

_url = 'https://api.projectoxford.ai/emotion/v1.0/recognize'
_key = "3c7ed1778e2a4fc5aed6d0c1ae5c295a" #Here you have to paste your primary key
_maxNumRetries = 10


# ## Helper functions

# In[13]:

def pulse():
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)


def maxi(toBeProcessed):
    maxi = toBeProcessed[0]
    nextmax = toBeProcessed[0]
    maxPos = 0
    nextmaxPos=0
    for i in range(0, len(toBeProcessed)):
        if toBeProcessed[i]>maxi:
            maxPos = i
            maxi = toBeProcessed[i]
        elif toBeProcessed[i]>nextmax:
            nextmaxPos = i
            nextmax = toBeProcessed[i]
    return maxi, maxPos, nextmax, nextmaxPos


def ultrasound():

    print("ultrasonic measurement")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)

    GPIO.output(GPIO_TRIGGER, False)
    time.sleep(0.5)

    pulse()

    start = time.time()
    x=0 #timeout variable
    stop = 0

    while GPIO.input(GPIO_ECHO) == 0:
        start=time.time()
        if x > 15000:
            print ("TIMEOUT")
            break
            x = 0
        x += 1

    while GPIO.input(GPIO_ECHO) == 1:
        stop=time.time()

    print ("Start is ", start)
    print ("stop is ", stop)
    elapsed = stop-start
    print (elapsed)
    distance = elapsed * 34000
    distance = distance / 2
    print ("Distance:" , distance)
    personFound = person(distance)
    GPIO.cleanup()
    return personFound

def person(distance):
    if distance < 100 and distance > 20:
        print ("person found")
        startTime = time.time()
        for i in range (0,3):
            fileName = 'image' + str(i) + '.jpg'
            #TAKE PICTURE
            #camera.resolution(640, 480)
            camera.capture(fileName)
        endTime = time.time()
        overallTime = endTime - startTime
        print ('overall', overallTime)
        return True
    else:
        print ("not a person")
        return False
def imageProcessing():
    personThere=False
    numberOfResults = 0
    for i in range (0,3):
        imageNumber = str(i)
        sadness = 0
        happiness = 0
        anger = 0
        neutral = 0
        surprise = 0
        contempt = 0
        disgust = 0
        fear = 0
        empty = 0
        print(imageNumber)
        pathName = r'/home/pi/image'+imageNumber+'.jpg'
        pathToFileInDisk = pathName
        print(pathName)
        #pathToFileInDisk =r'/home/pi/image1.jpg'
        #pathToFileInDisk = /home/pi/image1.jpg
        #pathToFileInDisk = r'/home/pi/Downloads/rsz_cam.jpg'
        with open( pathToFileInDisk, 'rb' ) as f:
            data = f.read()

        headers = dict()
        headers['Ocp-Apim-Subscription-Key'] = _key
        headers['Content-Type'] = 'application/octet-stream'

        json = None
        params = None

        result = processRequest( json, data, headers, params )
        if result is not None:
            numberOfResults += 1







            # Load the original image from disk
            data8uint = np.fromstring( data, np.uint8 ) # Convert string to an unsigned int array
            img = cv2.cvtColor( cv2.imdecode( data8uint, cv2.IMREAD_COLOR ), cv2.COLOR_BGR2RGB )

            renderResultOnImage( result, img )

            ig, ax = plt.subplots(figsize=(15, 20))
            ax.imshow( img )

            numberOfPeople = len(result)
            #print("result", result)
            print("number of people", numberOfPeople)
            if numberOfPeople != 0:
                print(numberOfPeople)
                print("number of people =", numberOfPeople)
                for i in range(0,len(result)):
                    sadness += result[i][u'scores'][u'sadness']
                    happiness += result[i][u'scores'][u'happiness']
                    anger += result[i][u'scores'][u'anger']
                    neutral += result[i][u'scores'][u'neutral']
                    surprise += result[i][u'scores'][u'surprise']
                    contempt += result[i][u'scores'][u'contempt']
                    disgust += result[i][u'scores'][u'disgust']
                    fear += result[i][u'scores'][u'fear']

                sadness = sadness/numberOfPeople
                happiness = happiness/numberOfPeople
                anger = anger/numberOfPeople
                neutral = neutral/numberOfPeople
                surprise = surprise/numberOfPeople
                contempt = contempt/numberOfPeople
                disgust = disgust/numberOfPeople
                fear = fear/numberOfPeople

                emotionNames = ['sadness', 'happiness', 'anger', 'neutral', 'surprise', 'contempt', 'disgust', 'fear']
                emotion = [sadness, happiness, anger, neutral, surprise, contempt, disgust, fear]
                maxVal, maxPos, nextMaxVal, nextMaxPos = maxi(emotion)
                maxValList.append(maxVal)
                maxEmoList.append(emotionNames[maxPos])
                nextMaxValList.append(nextMaxVal)
                nextMaxEmoList.append(emotionNames[nextMaxPos])
                print("max emo val", maxVal)
                print("max emo", emotionNames[maxPos])
                print("next max emo val", nextMaxVal)
                print("next max emo", emotionNames[nextMaxPos])
            else:
                print("no people found")
                empty += 1
                print(empty)
    print("empty",empty)
    sadnessOcc = 0
    happinessOcc = 0
    angerOcc=0
    neutralOcc=0
    surpriseOcc=0
    contemptOcc = 0
    disgustOcc=0
    fearOcc = 0
    if empty != 1:
        for i in range(0, len(maxEmoList)):
            if maxEmoList[i]=='sadness':
                sadnessOcc +=2
            elif maxEmoList[i]== 'happiness':
                happinessOcc += 2
            elif maxEmoList[i]== 'anger':
                angerOcc += 2
            elif maxEmoList[i]== 'neutral':
                neutralOcc += 2
            elif maxEmoList[i]== 'surprise':
                surpriseOcc += 2
            elif maxEmoList[i]== 'contempt':
                contemptOcc += 2
            elif maxEmoList[i]== 'disgust':
                disgustOcc += 2
            elif maxEmoList[i]== 'fear':
                fearOcc += 2
            else:
                print("emotion not valid")
        for i in range(0, len(nextMaxEmoList)):
            if nextMaxEmoList[i]=='sadness':
                sadnessOcc +=1
            elif nextMaxEmoList[i]== 'happiness':
                happinessOcc += 1
            elif nextMaxEmoList[i]== 'anger':
                angerOcc += 1
            elif nextMaxEmoList[i]== 'neutral':
                neutralOcc += 1
            elif nextMaxEmoList[i]== 'surprise':
                surpriseOcc += 1
            elif nextMaxEmoList[i]== 'contempt':
                contemptOcc += 1
            elif nextMaxEmoList[i]== 'disgust':
                disgustOcc += 1
            elif nextMaxEmoList[i]== 'fear':
                fearOcc += 1
            else:
                print("emotion not valid")
        overallEmo = [sadnessOcc, happinessOcc, angerOcc, neutralOcc, surpriseOcc, contemptOcc, disgustOcc, fearOcc]
        #emotionNames = ['sadness', 'happiness', 'anger', 'neutral', 'surprise', 'contempt', 'disgust', 'fear']
        print(overallEmo)
        print(type(overallEmo))
        maxOcc, maxPos, nextOcc, nextPos = maxi(overallEmo)
        maxEmotionOverall = emotionNames[maxPos]
        nextMaxEmotionOverall = emotionNames[nextPos]
        print("max emo overall", maxEmotionOverall)
        print("next max emo", nextMaxEmotionOverall)
        personThere= True
        #return maxEmotionOverall, nextMaxEmotionOverall, personThere
    else:
        print("no people detected")
        personThere = False
        maxEmotionOverall = "none"
        nextMaxEmotionOverall = "none"
    return maxEmotionOverall, nextMaxEmotionOverall, personThere

def generatePlaylist(maxEmo):
    if maxEmo in ["sadness","happiness","neutral","anger","disgust","contempt"]:
        print("suitable")
        if maxEmo == "sadness":
            playlist = "Sad"
        elif maxEmo == "happiness":
            playlist = "Happy"
        elif maxEmo == "neutral":
            playlist = "Neutral"
        else:
            playlist = "Angry"

    else:
        print("not in list")
        playlist = "Neutral"
    return playlist

def processRequest( json, data, headers, params ):

    """
    Helper function to process the request to Project Oxford

    Parameters:
    json: Used when processing images from its URL. See API Documentation
    data: Used when processing image read from disk. See API Documentation
    headers: Used to pass the key information and the data type request
    """

    retries = 0
    result = None

    while True:

        response = requests.request( 'post', _url, json = json, data = data, headers = headers, params = params )

        if response.status_code == 429:

            print( "Message: %s" % ( response.json()['error']['message'] ) )

            if retries <= _maxNumRetries:
                time.sleep(1)
                retries += 1
                continue
            else:
                print( 'Error: failed after retrying!' )
                break

        elif response.status_code == 200 or response.status_code == 201:

            if 'content-length' in response.headers and int(response.headers['content-length']) == 0:
                result = None
            elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str):
                if 'application/json' in response.headers['content-type'].lower():
                    result = response.json() if response.content else None
                elif 'image' in response.headers['content-type'].lower():
                    result = response.content
        else:
            print( "Error code: %d" % ( response.status_code ) )
            print( "Message: %s" % ( response.json()['error']['message'] ) )

        break

    return result


# In[14]:

def renderResultOnImage( result, img ):

    """Display the obtained results onto the input image"""

    for currFace in result:
        faceRectangle = currFace['faceRectangle']
        cv2.rectangle( img,(faceRectangle['left'],faceRectangle['top']),
                           (faceRectangle['left']+faceRectangle['width'], faceRectangle['top'] + faceRectangle['height']),
                       color = (255,0,0), thickness = 5 )


    for currFace in result:
        faceRectangle = currFace['faceRectangle']
        currEmotion = max(currFace['scores'].items(), key=operator.itemgetter(1))[0]


        textToWrite = "%s" % ( currEmotion )
        cv2.putText( img, textToWrite, (faceRectangle['left'],faceRectangle['top']-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1 )




sadness = 0
happiness = 0
anger = 0
neutral = 0
surprise = 0
contempt = 0
disgust = 0
fear = 0


cont = False


while cont == False:
    numberOfResults= 0
    maxValList=[]
    maxEmoList=[]
    nextMaxValList=[]
    nextMaxEmoList=[]
    playlist = "Neutral"

    personFound = ultrasound()

    if personFound == True:
        maxEmo,nextEmo, personPresent = imageProcessing()
    else:
        personPresent = False
        print("person not found")

    if personPresent == False:
        print("person not found")
    else:
        playlist = generatePlaylist(maxEmo)
        print("playlist chosen", playlist)
        cont = True
    time.sleep(10)

HappyPlaylist = "https://www.youtube.com/watch?v=PGJX9tutZEA"
SadPlaylist = "https://www.youtube.com/watch?v=4N3N1MlvVc4"
NeutralPlaylist = "https://www.youtube.com/watch?v=VjHMDlAPMUw"
AngryPlaylist = "https://www.youtube.com/watch?v=00Z-Gbyb7l8"

if playlist == "Happy":
    os.system("echo add " + HappyPlaylist + " | nc -U /home/pi/vlc.sock")
    print("Playing Happy Playlist")

elif playlist == "Sad":
    os.system("echo add " + SadPlaylist + " | nc -U /home/pi/vlc.sock")
    print("Playing Sad Playlist")

elif playlist == "Angry":
    os.system("echo add " + AngryPlaylist + " | nc -U /home/pi/vlc.sock")
    print("Playing Angry Playlist")

else:
    os.system("echo add " + NeutralPlaylist + " | nc -U /home/pi/vlc.sock")
    print("Playing Neutral Playlist")

#url = "https://www.youtube.com/watch?v=nYh-n7EOtMA"
