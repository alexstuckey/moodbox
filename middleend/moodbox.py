from __future__ import print_function
import time
import requests
import cv2
import operator
import numpy as np
import os
import matplotlib.pyplot as plt
import requests
import json
import urllib.request

# # Api Script
# _url = 'https://api.projectoxford.ai/emotion/v1.0/recognize'
# _key = "ba924568b887445180e64b501cd1e689" #Here you have to paste your primary key
# _maxNumRetries = 10

### NEW WAY
# ########### Python 3.2 #############
# import http.client, urllib.request, urllib.parse, urllib.error, base64, sys
#
# headers = {
#     # Request headers. Replace the placeholder key below with your subscription key.
#     'Content-Type': 'application/json',
#     'Ocp-Apim-Subscription-Key': 'ba924568b887445180e64b501cd1e689',
# }
#
# params = urllib.parse.urlencode({
# })
#
# # Replace the example URL below with the URL of the image you want to analyze.
# body = "{ 'url': 'http://is-a-cunt.com/wp-content/uploads/2016/07/18137-1t8ewuk.jpg' }"
#
# try:
#     conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
#     conn.request("POST", "/emotion/v1.0/recognize?%s" % params, body, headers)
#     response = conn.getresponse()
#     data = response.read()
#     print(data)
#     conn.close()
# except Exception as e:
#     print(e.args)
# ####################################

_url = 'https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognize'
_key = "ba924568b887445180e64b501cd1e689" #Here you have to paste your primary key
_maxNumRetries = 10

## Emotion Analysis

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
        pathName = r'image'+imageNumber+'.jpg'
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
            numberOfResults += 1            # Load the original image from disk
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
    if maxEmo in ["sadness","happiness","neutral","anger","disgust","contempt", "fear","surprise"]:
        print("suitable")
        if maxEmo == "sadness":
            playlist = "Sad"
        elif maxEmo == "happiness":
            playlist = "Happy"
        elif maxEmo == "neutral":
            playlist = "Neutral"
        elif maxEmo == "disgust":
            playlist = "Disgust"
        elif maxEmo == "contempt":
            playlist = "Contempt"
        elif maxEmo == "fear":
            playlist = "Fear"
        elif maxEmo == "surprise":
            playlist = "Surprise"
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

    personFound = True

    if personFound == True:
        maxEmo,nextEmo, personPresent = imageProcessing()
    else:
        personPresent = False
        print("person not found")

    if personPresent == False:
        print("person not found")
    else:
        playlist = generatePlaylist(maxEmo)
        try:
            getJSONForMoodRequest = 'http://community.dur.ac.uk/mohammed.m.rahman/moodbox/backend/api.php?action=getTrack&emotion=' + str(playlist)
            getJSONForMoodData = urllib.request.urlopen(getJSONForMoodRequest)
            #print(getJSONForMoodData.read())
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            print('Decoding JSON has failed')
        #Extract Playlist PlaylistUrl =
        print("playlist chosen", playlist)
        cont = True
    time.sleep(10)


#Extract data:
# parsed_json = json.loads(str(getJSONForMoodData.read()))

# print(str(getJSONForMoodData.read()))

song_data = json.loads(getJSONForMoodData.read())

songs = []

for song in song_data['queue']:
    # songs.append(song['stream_url'])
    os.system("echo add " + song['stream_url'] + " | nc -U /home/pi/vlc.sock")



pass
# os.system("echo add " + songs[0] + " | nc -U /home/pi/vlc.sock")
