# coding=utf-8
import sys
import time
import os
import random

# Set MODIM_IP to connnect to remote MODIM server
try:
    sys.path.insert(0, os.getenv('MODIM_HOME')+'/src/GUI')
except Exception as e:
    print("Please set MODIM_HOME environment variable to MODIM folder.")
    sys.exit(1)



import ws_client
from ws_client import *

def i1():
    #IM-> interaction manager
    im.init()   #azione che va lanciata per prima (dopo le varie strutture e inizializzazioni - nel while true)
    #im.executeModality('TEXT_default','Waiting for a human!')


    ask = im.ask('welcome', timeout=20)
    if (ask!='timeout'):
        im.execute(ask)   #eseguo una delle azioni definite
        im.execute('goodbye')

    im.executeModality('IMAGE', '/img/trash/all_secchi.jpeg')
    im.executeModality('TEXT', 'ABBIAMO FINITO ANDATE IN PACE')
    ask = im.ask(None, timeout = 5)        #lo posso usare come modo per lasciare una cosa in attesa senza eseguire nulla
        
	
    action = 'play'
    que = im.ask(action)   

    if que == 'paper': im.execute('correct')
    else: im.execute('wrong')
    ask = im.ask(None, 10)

    im.init()           #ritorno alla schermata iniziale

    
def example_exeMod():
    im.executeModality('LOGO', '/img/trash/cartone.jpeg')
    im.executeModality('IMAGE', 'img/trash/all_secchioni.jpg')
    im.executeModality('TEXT', 'Tocca il secchio corretto')
    im.executeModality('TTS', 'Tocca il secchio corretto')
    im.executeModality('BUTTONS', [('paper', 'PAPER'),  ('glass', 'GLASS'), ('metal', 'METAL'), ('plastic', 'PLASTIC')])
    ask = im.ask(None, timeout = 55)
    print('AAAAAAAAAASSSSSSKKKKK', ask)

#def i2():
#    im.execute('put_trash')     #Questo lo lasciamo così


if __name__ == "__main__":

    mws = ModimWSClient()

    # local execution
    mws.setDemoPathAuto(__file__)
    # remote execution
    # mws.setDemoPath('<ABSOLUTE_DEMO_PATH_ON_REMOTE_SERVER>')

    mws.run_interaction(i1)     #i1, i2 sono i task che deve compiere, capire se fare funzioni separate o un unico flusso su una funzione 
                                #all'interno definisco classi, e faccio un grande while True con degli elif?

    #mws.run_interaction(i2)  #i2 è il 


