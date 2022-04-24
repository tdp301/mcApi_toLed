# Read from mcapi.us on a server status and send serial request to gaint led

import requests
import time
import serial

#TODO replace IP.IP.IP.IP and PORT with actual IP and Port
url = 'https://mcapi.us/server/status?ip=IP.IP.IP.IP&port=PORT'


#Get number of players and return integer
def getNumPlayers(_url):
    response = requests.get(url)

    print('Request status...')

    if response.status_code == 200:
        #response ok
        print('ok')
        json_response = response.json()
        if 'players' in json_response:
            #print('Max players: ' + str(json_response['players']['max']))
            #print('Current players: ' + str(json_response['players']['now']))
            return int(json_response['players']['now'])
    else:
        print('Warning, bad return ' + str(response.status_code))
        
    return 0

#Given number of players, return color string
def mapNumToColorStr(num):
    #note that led expects "$rrggbb#"
    if num <= 1:
        return "$00ffff#"
    elif num == 2:
        return "$ffff00#"
    elif num == 3:
        return "$ff8000#"
    else:
        return "$ff0000#"

#--- start of program ----

ser = serial.Serial('/dev/ttyAMA0') #opens first serial port, 9600 8n1

while 1==1:

    print( "Fetching Page")
    numPlayers = getNumPlayers(url)

    print ("Returned num: " + str(numPlayers))

    if (numPlayers > 0):
        #Map to color...
        colorString = mapNumToColorStr(numPlayers)
        ser.write(colorString.encode()) #set color command
        time.sleep(1)
        ser.write(str.encode("$$$$#")) #turn on command
    else:
        ser.write(str.encode("%%%%#")) #turn off command
        
    time.sleep(60)   #only check every 1 minute

        
ser.close()
