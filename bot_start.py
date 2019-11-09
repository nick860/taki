#   Imports
import socket
import sys
import time
import json
import random
import r

#   Defs:

# if someone put +2 --> return +2 card or None(take cards from the pile)
def check_plus_2(game):
    hand = game['hand']
    for c in hand:
        if c['value'] == "+2":
            return c
    return None

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
server_address = ('localhost', 50000)

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
    print 'my id - ' + my_id

    time.sleep(1)
    
    #   Loop Game:
    while True:
        data = sock.recv(1024)[4:]
        if "Error[" not in data:   #need to check - Error[ ??
            game = json.loads(data)
            cur_turn = game['turn']

            if cur_turn == my_id: # my turn
            pile = game['pile']
            
            if pile['value'] == "+2": # if someone put +2
                card = check_plus_2(game)
                if card: # put the card : +2
                    play_turn = card
                else: # take card from the server
                    play_turn = {'card': {"color": "", "value": ""}, 'order': 'draw card' }



                

finally:
    print 'closing socket'
    sock.close()
