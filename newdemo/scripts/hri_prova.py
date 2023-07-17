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
    ask = im.ask(None, timeout = 10)
    im.executeModality('TEXT','Waiting for a human!')
    prova = im.listConditions('play')
    print(prova)
    someone = False 
    if(someone == False): ask = im.ask(None, timeout = 10)
    #else: arriva qualcuno facciamo ask welcome
    #ask = im.ask('welcome', timeout=20)
    eta = 'timeout' ##
    ret = ''
    while(eta == 'timeout'):
        eta = im.ask('welcome', timeout=20)
        if(eta == 'child'):
            ret = im.ask('child')
        elif(eta == 'guy'):
            ret = im.ask('guy')

        elif(eta!='timeout'):
            #cambiareee
            #im.execute(ask)   #eseguo una delle azioni definite
            im.execute('goodbye')
        
    if(ret == 'put_trash'):
        piantina = im.ask('put_trash')
        time.sleep(10)
    elif(ret == 'sents'):
        pagina = im.ask('sents')
        print(pagina)
        time.sleep(10)
    elif(ret == 'play'):
        que = im.ask('play')
        if que == 'paper': im.execute('correct')
        else: im.execute('wrong')
        time.sleep(10)

    im.init()           #ritorno alla schermata iniziale

    
def example_exeMod():
    im.executeModality('LOGO', '/img/trash/cartone.jpeg')
    im.executeModality('IMAGE', 'img/trash/all_secchioni.jpg')
    im.executeModality('TEXT', 'Tocca il secchio corretto')
    im.executeModality('TTS', 'Tocca il secchio corretto')
    im.executeModality('BUTTONS', [('paper', 'PAPER'),  ('glass', 'GLASS'), ('metal', 'METAL'), ('plastic', 'PLASTIC')])
    ask = im.ask(None, timeout = 55)
    print('AAAAAAAAAASSSSSSKKKKK', ask)


if __name__ == "__main__":

    mws = ModimWSClient()

    # local execution
    mws.setDemoPathAuto(__file__)
    # remote execution
    # mws.setDemoPath('<ABSOLUTE_DEMO_PATH_ON_REMOTE_SERVER>')

    mws.run_interaction(i1)     #i1, i2 sono i task che deve compiere, capire se fare funzioni separate o un unico flusso su una funzione 
                                #all'interno definisco classi, e faccio un grande while True con degli elif? 
