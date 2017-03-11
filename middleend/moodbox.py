from __future__ import print_function
import time
import requests
import cv2
import operator
import numpy as np
import os

# # Api Script
# _url = 'https://api.projectoxford.ai/emotion/v1.0/recognize'
# _key = "ba924568b887445180e64b501cd1e689" #Here you have to paste your primary key
# _maxNumRetries = 10


########### Python 3.2 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64, sys

headers = {
    # Request headers. Replace the placeholder key below with your subscription key.
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'ba924568b887445180e64b501cd1e689',
}

params = urllib.parse.urlencode({
})

# Replace the example URL below with the URL of the image you want to analyze.
body = "{ 'url': 'http://www.newstatesman.com/sites/default/files/styles/nodeimage/public/blogs_2015/10/gettyimages-484567630.jpg' }"

try:
    conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/emotion/v1.0/recognize?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print(e.args)
####################################
