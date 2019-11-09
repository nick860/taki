#   Imports
import socket
import sys
import time
import json
import random
import re

#   Defs:
#cheks the amount of cards that having the same color of spacifics number
#return the card that his color repets more times than the other cards
def colorNumCheck(game,card)
    hand=game['hand']
    maxx=-9999
    color=""
    cardR=None
    deck=[]
    for c in hand:
        if c["Value"]==card["Value"] and (c in deck)==False:
            deck.append(c)

    for c2 in deck:
        if WeHave(c2["Color"])>maxx:
            maxx=WeHave(game,c2["Color"])
            color=c2["Color"]
            cardR=c2
            
    return (cardR,maxx)
#cheks the color amount in our hand for the color that have been sent
def colorCheck(game,color)
    hand=game['hand']
    count=0
    for c in hand:
        if c["Color"]==color:
            count=count+1
    return count
#function that checks if we have enough cards to put on the Taki/+1 cards
#that we just have droped-return how many cards we have like this
def WeHave(game,card):
    hand=game['hand']
    flag=card['Color ']
    count=0
    for c in hand:
        if flag=='ALL':  
            if c['Color ']==pile['Color ']:
                count=count+1
        else:
            if c['Color ']==card['Color '] and card['Value']=="TAKI":
                count=count+1
            elif c['Color ']==card['Color '] and card['Value']=="+":
                count=count+1
    return count           
        
#sending the value and color we want to find in our hand
def ExistC(game,Value,color):
    hand=game['hand']
    flag=len(color)
    for c in hand:
        if flag==0:
            if c['Value'] in Value:#we dont care about the color
                return c
        else:
            if (c['Value'] in Value) and (c['Color'] in color):
                return c
    return None

#here we check if to the next player has under than 4 cards
#if yes so return true, others return false
def littleCards(game,idm):
    nextPlayer=0
    if idm==3:
        nextPlayer=1
    else:
        nextPlayer=nextPlayer+1

    handNext=game['others']
    cardsOfNext=handNext[nextPlayer]+1
    if cardsOfNext<4:
        return True
    else:
        return False
        
    
"""  משתנים:
data - מהסרבר
my_id - הid שלנו
game - כל מה שצריך מהמשחק
cur_turn - התור כרגע
pile - the leading card
card - הקלף שאנחנו מקבלים מהפעולה שלנו
play_turn - הקלף שאנחנו שולחים לסרבר
"""
# -------------------------------------------------------------------------
#   Sockets and Data
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('192.168.1.20', 50011)

sock.connect(server_address)

time.sleep(1)
json_kwargs = {'default': lambda o: o.__dict__, 'sort_keys': True, 'indent': 4}

password = '1234'

try:
    # Send data
    # Connection setup
    sock.send(password)

    data = sock.recv(1024)[4:]
    print data

    data = sock.recv(1024)[4:]
    my_id = int(re.findall('[0-9]', data)[0])
    print 'my id - ' ,my_id

    time.sleep(1)
    takeFrom=False
    #   Loop Game:
    while True:
        data = sock.recv(1024)[4:]
        if "Error[" not in data:   #need to check - Error[ ??
            game = json.loads(data)
            cur_turn = game['turn']

            if cur_turn == my_id: # my turn
              pile = game['pile']
            
            if pile['value'] == "+2": # if someone put +2
                card=Exist(game,["+2"],[])
                if card: # put the card : +2
                    play_turn = {'card': card, 'order': ''}
                else:
                    takeFrom=True
                #else: # take card from the server
                   # play_turn = {'card': {"color": "", "value": ""}, 'order': 'draw card' }

            #if to the next player has 4- cards so try to put spacifcs card
            elif littleCards(game,my_id)==True:
                card=Exist(game,["+2","STOP","CHDIR"],[pile['color']])
                if card:
                    play_turn = {'card': card, 'order': ''}
                else:
                     takeFrom=True
           #================In this else we dont care about the amount of card
                     #of the next player and we dont need to take +2 card
            else: 
                #cheking if we have a storng card we can use and if its usefull for us
                card=Exist(game,["TAKI","+"],["ALL",pile['color']])
                if card:
                    count=WeHave(game,card)
                    if card["Value"]=="TAKI":                    
                        if count>0:
                            play_turn = {'card': card, 'order': ''}
                        elif card["Value"]=="+":
                            if count>0:
                                play_turn = {'card': card, 'order': ''}
                            else:
                                takeFrom=True
                #if we dont have a strong card or the card not usefull in our case
                #so we may check the change color card
                card=Exist(game,["CHCOL"],[])
                if card and takeFrom==True:
                    yellow=colorCheck(game,"Yellow")
                    red=colorCheck(game,"red")
                    blue=colorCheck(game,"blue")
                    green=colorCheck(game,"green")
                    #dictionary to find out what color to chose
                    dicColor={"Yellow":yellow,"red":red,"blue":blue,"green":green}
                    num= max(dicColor.values())
                    color=""
                    for key, value in dictionary.items():
                        if num == value:
                         color==key
                    
                    play_turn = {'card': card, 'order': color}     
                else: #if this a regular card game turn
                   col=colorCheck(game,pile['color'])
                   colOfNum=colorNumCheck(game,pile)
                   card=Exist(game,["1","2","3","4","5","6","7","8","9"],[pile['color']])

                   if col>colOfNum[1]:
                       play_turn = {'card': card, 'order': ''}
                   elif col<=colOfNum[1]:
                       play_turn = {'card': colOfNum[0], 'order': ''}
                   else:
                       takeFrom=True



            if takeFrom==True:
                    play_turn = {'card': {"color": "", "value": ""}, 'order': 'draw card' }
            dus = json.dumps(play_turn, **json_kwargs)
            sock.send(dus)
            
        time.sleep(1)


                

finally:
    print 'closing socket'
    sock.close()
