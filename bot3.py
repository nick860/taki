import socket
import sys
import time
import json
import random
import re
def mycolor(game):
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
     return color
def colorCheck(game,color):
    hand=game['hand']
    count=0
    for c in hand:
        if c["color"]==color:
            count=count+1
    return count

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
    
def littleCards(game,idm):
    nextPlayer=0
    if idm==3:
        nextPlayer=0
    else:
        nextPlayer=nextPlayer+1

    handNext=game['others']
    cardsOfNext=handNext[nextPlayer]+1
    if cardsOfNext<10:
        return True
    else:
        return False
    
def choose_best_option(game):
    global takiopen
    global equal 
    hand = game['hand']
    pile = game['pile']
    pile_color = game['pile_color']
    card_options = []
    color=0
    num=0
    for c in hand:
        
        if c['color'] == pile_color:
            card_options.append(c)
            color=color+1
            
        elif c['value'] == pile['value']:
            card_options.append(c)
            num=num+1
        
    if len(card_options) == 0:
        return None
    else:
        for c in card_options:
            if c['value']=='TAKI' and c['color']=='ALL':
                
                return c
                #....
            elif c['value']=='TAKI':
                return c
                #...
            elif c['value']=='+2':
                 if pile['value']=='+2' and equal>=1:
                      return None
                 else:
                      return c
                
                #...
            elif c['value']=='STOP':
                 
                 if pile['value']=='STOP' and equal==0:
                      return None
                 else:
                      return c
                #...
            elif c['value']=='CHCOL':
                color=mycolor(game)
                return (c,color)
                #...
            elif c['value']=='CHDIR' and littleCards(game,game['turn']):
                    
                return c       
                #..
            elif c['value']=='+':
                return c
                #...
            elif c['value'] in ["1","2","3","4","5","6","7","8","9"]:
                return c
        
    
    return None


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 50040)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

time.sleep(1)
json_kwargs = {'default': lambda o: o.__dict__, 'sort_keys': True, 'indent': 4}

password = '1234'

global takiopen
global equal 
takiopen=False
try:
    # Send data
    # Connection setup
    print >>sys.stderr, 'sending Password "%s"' % password
    sock.send(password)

    data = sock.recv(1024)[4:]
    print >> sys.stderr, 'For Password "%s"' % data

    data = sock.recv(1024)[4:]
    my_id = int(re.findall('[0-9]', data)[0])
    print >> sys.stderr, 'For ID "%s"' % data[4:]
    
    # From now on each time
    time.sleep(1)
    while True:
        
        data = sock.recv(1024)
        print data
        print data[:4]
        data=data[4:]
        print >> sys.stderr, 'For game state "%s"' % data

        if "Error[" not in data:
            game = json.loads(data)
            cur_turn = game['turn']
        if cur_turn ==game['others'][TwoBeforeUs(my_id)]:
           saveOneBefore= game['others'][BeforeUs(my_id)]
           
           
           if cur_turn == my_id: 
                card = choose_best_option(game)
                OneBefore=game['others'][BeforeUs(my_id)]
                equal=OneBefore-saveOneBefore
                
                if card:
                     if len(card)==2:
                       play_turn = {'card': card, 'order': str(card)[1]}
                     else:    
                       play_turn = {'card': card, 'order': ''}
                else:
                    play_turn = {'card': {"color": "", "value": ""}, 'order': 'draw card' }
                dus = json.dumps(play_turn, **json_kwargs)
                sock.send(dus)



finally:
    print >>sys.stderr, 'closing socket'
    sock.close()
