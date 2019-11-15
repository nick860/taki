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
def colorNumCheck(game,card):
    hand=game['hand']
    maxx=-9999
    color=""
    cardR=None
    deck=[]
    for c in hand:
        if c["value"]==card["value"] and (c in deck)==False:
            deck.append(c)

    for c2 in deck:
        if WeHave(game, c2)>maxx:
        #if WeHave(game, c2["color"])>maxx:
            #maxx=WeHave(game,c2["color"])
            maxx=WeHave(game,c2)
            color=c2["color"]
            cardR=c2
            
    return (cardR,maxx)
#cheks the color amount in our hand for the color that have been sent
def colorCheck(game,color):
    hand=game['hand']
    count=0
    for c in hand:
        if c["color"]==color:
            count=count+1
    return count
#function that checks if we have enough cards to put on the Taki/+1 cards
#that we just have droped-return how many cards we have like this
def WeHave(game,card):
    hand=game['hand']
    flag=card['color']
    count=0
    for c in hand:
        if flag=='ALL':  
            if c['color']==pile['color']:
                count=count+1
        else:
            if c['color']==card['color'] and card['value']=="TAKI":
                count=count+1
            elif c['color']==card['color'] and card['value']=="+":
                count=count+1
    return count           
        
#sending the value and color we want to find in our hand
def Exist(game,Value,color):
    hand=game['hand']
    flag=len(color)
    for c in hand:
        if flag==0:
            if c['value'] in Value:#we dont care about the color
                return c
        else:
            if (c['value'] in Value) and (c['color'] in color):
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
    if cardsOfNext<20:
        return True
    else:
        return False
        
def BeforeUs(i):
    if i>0:
        return i-1
    else:
        return 3


def TwoBeforeUs(i):
    if i+2<4:
        return i+2
    else:
        return i-2

def colorforg(colo):
    dif={"yellow":"_Y",
         "red":"_R",
         "green":"_G",
         "blue":"_B",
         "CHDIR":">",
         "STOP":"S",
         "TAKI":"T",
         "CHCOL":"cc",
         "TAKICOLOR":"ct",
         "+":"+",
         "+2":"+2"
        }
    return dif[colo] 
# -------------------------------------------------------------------------
#   Sockets and Data
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 50000)

sock.connect(server_address)
print 'connected'
time.sleep(1)
json_kwargs = {'default': lambda o: o.__dict__, 'sort_keys': True, 'indent': 4}
start=True
password = '1234'
opentaki=False
saveCard=True
Maybe=0
check=0
saveOneBefore=0
OneBefore=0
hand=None
stop=False
try:
    # Send data
    # Connection setup
    sock.send(password)

    data = sock.recv(1024)[4:]
    print data

    data = sock.recv(1024)[4:]
    my_id = int(re.findall('[0-9]', data)[0])
    print 'my id - ' ,my_id

    
    takeFrom=True
    play_turn = None
    #   Loop Game:
    while True:
        data = sock.recv(1024)[4:]
        print >> sys.stderr, 'For game state "%s"' % data
        if "error" not in data:   #need to check - Error[ ??
            game = json.loads(data)
            if 'error' in game: 
                break
            cur_turn = game['turn']
            cs=0
            if hand:
                with open(r"c:\takifolder\cardfile.txt", 'w') as file2:
                    for c in hand:
                        colorr=c["color"]
                        value=c["value"]
                        cs=cs+1
                        if value in ["1","2","3","4","5","6","7","8","9"]:            
                          file2.write(str(cs)+". "+value+colorforg(colorr)+"\n")
                        else:
                            if value=="TAKI" and colorr=="ALL":     
                              file2.write(str(cs)+". "+colorforg("TAKICOLOR")+"\n")
                            else:
                              file2.write(str(cs)+". "+colorforg(value)+"\n")  
                    
            print cur_turn
            print game['others']
            
            if cur_turn ==game['others'][TwoBeforeUs(my_id)]:
                saveOneBefore= game['others'][BeforeUs(my_id)]

                
            if cur_turn == my_id: # my turn
                pile = game['pile']
                OneBefore=game['others'][BeforeUs(my_id)]
                hand=game['hand']
                
                if OneBefore-saveOneBefore==0 and pile['value'] == "STOP":
                    print "Stop not our"
                    saveCard=True
                    stop = True
                    
                elif OneBefore-saveOneBefore >=1 and pile['value'] == "+2":
                    saveCard=False
                    
                else:
                    saveCard=True
                
                print saveCard
                
                if pile['value'] == "STOP":
                    if stop:
                        takeFrom = True
                        stop = False
                elif pile['value'] == "+2" and saveCard==True : # if someone put +2
                    print ";;;;;;;;;;;;;;1"
                    card=Exist(game,["+2"],[])
                    if card: # put the card : +2
                        play_turn = {'card': {"color": (str)(card["color"]), "value": (str)(card["value"])}, 'order': ''}
                        takeFrom=False
                    else:
                        takeFrom=True

                
                #else: # take card from the server
                   # play_turn = {'card': {"color": "", "value": ""}, 'order': 'draw card' }

            #if to the next player has 4- cards so try to put spacifcs card
                
                elif Exist(game,["+2","STOP","CHDIR"],[pile['color']]) and takeFrom==True:
                        print ";;;;;;d;;;;;;;;1"
                        card=Exist(game,["+2","STOP","CHDIR"],[pile['color']])
                        play_turn = {'card': {"color": (str)(card["color"]), "value": (str)(card["value"])}, 'order': ''}
                        
                        takeFrom=False
           #================In this else we dont care about the amount of card
                     #of the next player and we dont need to take +2 card
               
                #cheking if we have a storng card we can use and if its usefull for us
                
                elif Exist(game,["TAKI","+"],["ALL",pile['color']]) and takeFrom==True:
                    print ";;;;6;;d;;;;;;;;1"
                    card=Exist(game,["TAKI","+"],["ALL",pile['color']])
                    count=WeHave(game,card)
                    if card["value"]=="TAKI":                    
                            if count>0:
                                play_turn = {'card': {"color": (str)(card["color"]), "value": (str)(card["value"])}, 'order': ''}
                                takeFrom=False
                    elif card["value"]=="+":
                            if count>0:
                                play_turn = {'card': {"color": (str)(card["color"]), "value": (str)(card["value"])}, 'order': ''}
                                takeFrom=False
                    else:
                        takeFrom=True
                #if we dont have a strong card or the card not usefull in our case
                #so we may check the change color card
              
                elif Exist(game,["CHCOL"],[]) and takeFrom==True:
                        print ";;;;6;;d;;;;;;;;1"
                        card=Exist(game,["CHCOL"],[])
                        yellow=colorCheck(game,"Yellow")
                        red=colorCheck(game,"red")
                        blue=colorCheck(game,"blue")
                        green=colorCheck(game,"green")
                    #dictionary to find out what color to chose
                        dicColor={"Yellow":yellow,"red":red,"blue":blue,"green":green}
                        num= max(dicColor.values())
                        color=""
                        for key, value in dicColor.items():
                            if num == value:
                             color=key
                    
                        play_turn = {'card': {"color": (str)(card["color"]), "value": (str)(card["value"])}, 'order': color}     
                        takeFrom=False
                        
                elif takeFrom==True: #if this a regular card game turn
                       print "fuck" 
                       col=colorCheck(game,pile['color'])
                       print "cheking for regalir card"
                       colOfNum=colorNumCheck(game,pile)
                       card=Exist(game,["1","2","3","4","5","6","7","8","9"],[pile['color']])
                       if pile['value']=="TAKI" and card:
                           if col==1:
                               play_turn = {'card': {"color": (str)(card["color"]), "value": (str)(card["value"])}, 'order': 'close taki'}
                               takeFrom=False 
                           else:
                               opentaki=True
                               #takeFrom=False
                             #try to fix daniel  #play_turn = {'card': {"color": (str)(card["color"]), "value": (str)(card["value"])}, 'order': ''}
                               
                               
                       elif col>colOfNum[1] and card:
                           play_turn = {'card': {"color": (str)(card["color"]), "value": (str)(card["value"])}, 'order': ''}
                           takeFrom=False 
                       elif col<=colOfNum[1]:
                           card=colOfNum[0]
                           play_turn = {'card': {"color": (str)(card["color"]), "value": (str)(card["value"])}, 'order': ''}
                           takeFrom=False 
                       else:
                           takeFrom=True


                
                start=False
                print play_turn
                try:
                    print card["color"]
                    print takeFrom
                except:
                    pass
                
                
                if takeFrom==True or play_turn==pile:
                        play_turn = {'card': {"color": "", "value": ""}, 'order': 'draw card'}
                        
                if opentaki==True:
                    if colorCheck(game,pile['color'])==1:
                        play_turn['order']='close taki'
                        opentaki=False
                if play_turn["card"]["value"]=="TAKI":
                    print "suvh"
                dus = json.dumps(play_turn, **json_kwargs)
                sock.send(dus)
            
        


                

finally:
    print 'closing socket'
    sock.close()
