#   Imports
import socket
import sys
import time
import json
import random
import re



def help4(game,card):
    hand = game['hand']
    pile = game['pile']
    pile_color = game['pile_color']
    for c in hand:
        if c['color'] == pile_color:
            return c
        if c['value'] == pile['value']:
            return c


        
def help3(game):
    hand = game['hand']
    green = 0
    blue = 0
    yellow = 0
    red = 0
    for c in hand:
        if c['color'] == "green":
            green+=1
        elif c['color'] == "yellow":
            yellow+=1
        elif c['color'] == "blue":
            blue+=1
        elif c['color'] == "red":
            red+=1
            
    if green > blue and green > yellow and green > red:
        return "green"
    elif blue > green and blue > yellow and blue > red:
        return "blue"
    elif red > green and red > yellow and red > blue:
        return "red"
    else:
        return "yellow"
    
    
    
    


def help2(game):
    hand = game['hand']
    pile = game['pile']
    pile_color = game['pile_color']
    for c in hand:
        if c['color'] == pile_color:
            return c
        if c['value'] == pile['value']:
            return c
    for c in hand:
        if c['value'] == "TAKI":
            return c
        if c['value'] == "CHCOL":
            return c

def Exist(game,Value,color):
    hand=game['hand']
    flag=len(color)
    for c in hand:
        if flag==0:
            if c['value'] in Value:#we dont care about the color
                print c
                return c
        else:
            if (c['value'] in Value) and (c['color'] in color):
                print c
                return c
    return None

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
         "+2":"+2",
         "ALL":""
        }
    return dif[colo]

# -------------------------------------------------------------------------
#   Sockets and Data
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('192.168.1.214', 50000)

sock.connect(server_address)
print 'connected'
time.sleep(1)
password = '1234'
json_kwargs = {'default': lambda o: o.__dict__, 'sort_keys': True, 'indent': 4}

try:
    sock.send(password)

    data = sock.recv(1024)[4:]
    print data

    data = sock.recv(1024)[4:]
    my_id = int(re.findall('[0-9]', data)[0])
    print 'my id - ' ,my_id
    flagTaki = False
    #   Loop Game:
    while True:
        cs = 0
        flag = False
        data = sock.recv(1024)[4:]
        print >> sys.stderr, 'For game state "%s"' % data
        if "error" not in data:   
            game = json.loads(data)
            if 'error' in game: 
                break
            cur_turn = game['turn']
            hand= game['hand']
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
                          file2.write(str(cs)+". "+colorforg(value)+colorforg(colorr)+"\n")  
                    
            if cur_turn == my_id:
                pile = game['pile']
                # + 2
                if pile['value'] == "+2":
                    card=Exist(game,["+2"],[])
                    if card: # put the card : +2
                        play_turn = {'card': {"color": (str)(card["color"]), "value": (str)(card["value"])}, 'order': ''}
                        flag = True
                else:
                    card = help2(game)
                    if card:
                        if flagTaki == True:
                            play_turn = {'card': card, 'order': 'close taki'}
                            flagTaki = False
                            
                        if card['value'] == "CHCOL":
                            newcolor = help3(game)
                            play_turn = {'card': card, 'order': newcolor}
                            flag = True
                        elif card['value'] == "TAKI":
                            play_turn = {'card': card, 'order': ''}
                            flag = True
                            flagTaki = True
                        else:
                            play_turn = {'card': card, 'order': ''}
                            flag = True
                        
                


                if flag == False:
                    play_turn = {'card': {"color": "", "value": ""}, 'order': 'draw card'}

                print play_turn
                dus = json.dumps(play_turn, **json_kwargs)
                sock.send(dus)
            time.sleep(1)
    
finally:
    print 'closing socket'
    sock.close()

