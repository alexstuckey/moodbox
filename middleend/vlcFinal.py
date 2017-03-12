import urllib.request
import json
import os
import time

playlist = 'sad'
try:
    getJSONForMoodRequest = 'http://community.dur.ac.uk/mohammed.m.rahman/moodbox/backend/api.php?action=getTrack&emotion=' + str(playlist)
    getJSONForMoodData = urllib.request.urlopen(getJSONForMoodRequest)
    #print(getJSONForMoodData.read())
except ValueError:  # includes simplejson.decoder.JSONDecodeError
    print('Decoding JSON has failed')

#Extract data:
# parsed_json = json.loads(str(getJSONForMoodData.read()))

#print(getJSONForMoodData.read().decode('utf-8'))

#song_data = json.loads(getJSONForMoodData.read())

output = getJSONForMoodData.read().decode('utf-8').replace(" ", "").split(",")

#print(output)
os.system("echo clear | nc -U /home/pi/vlc.sock")
for song in output:
    # songs.append(song['stream_url'])
    os.system("echo add " + song + " | nc -U /home/pi/vlc.sock")



os.system("echo goto 1 | nc -U /home/pi/vlc.sock")
##time.sleep(4000)
##os.system("echo next | nc -U /home/pi/vlc.sock")
##os.system("echo next | nc -U /home/pi/vlc.sock")
#os.system("echo previous | nc -U /home/pi/vlc.sock")


while True:
    try:
        getControlRequst = 'http://community.dur.ac.uk/mohammed.m.rahman/moodbox/backend/api.php?action=updatePi'
        getControlRequstData = urllib.request.urlopen(getControlRequst).read().decode("utf-8")
    except ValueError:
        print('Decoding JSON has failed')


 #   print(getControlRequstData)
    getControlRequstData = str(getControlRequstData)

    if getControlRequstData == 'next':
        os.system("echo next | nc -U /home/pi/vlc.sock")
    elif getControlRequstData == 'previous':
        os.system("echo prev | nc -U /home/pi/vlc.sock")
    elif getControlRequstData == 'pause':
        os.system("echo pause | nc -U /home/pi/vlc.sock")
    else:
        pass
