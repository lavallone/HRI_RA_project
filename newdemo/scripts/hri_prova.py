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

    garbage_bin = {'plastic': 'img/trash/bin_plastic.png', 
               'paper':'img/trash/bin_paper.png', 
               'compost':'img/trash/bin_compost.png', 
               'waste':'img/trash/bin_waste.png'}
    
    def giochino():
        dir_path = 'img/play_trash/'
        dict_trash = {}

        for elem in os.listdir('/home/robot/playground/newdemo/'+dir_path):
            waste_class = elem.split('_')[0]
            dict_trash[elem] = waste_class

        img_waste = random.choice(list(dict_trash.keys()))
        class_wast = dict_trash[img_waste] 
        path_waste = dir_path+img_waste
        print('CLASSE', class_wast)
        print('CLASSE', path_waste)
        c = 0
        while c < 3: 
            im.executeModality('IMAGE', path_waste)
            ans = im.ask('play', timeout = 15)
            if ans == class_wast: 
                c += 1
                im.execute('correct')
                img_waste = random.choice(list(dict_trash.keys()))
                class_wast = dict_trash[img_waste] 
                path_waste = dir_path+img_waste
            else: 
                im.execute('wrong')
        return True

    debug = True
    im.init()   #azione che va lanciata per prima (dopo le varie strutture e inizializzazioni - nel while true)
    someone = False
    finished = False
    if debug:
        p = im.robot.sensorvalue()
        print(p)
    while True:
        while(not someone): 
            ask = im.ask(None, timeout = 10)
            someone = True 

        eta = 'timeout' ##
        while(eta == 'timeout'):
            eta = im.ask('welcome', timeout=15)
            if(eta == 'elementary'):
                im.profile[0] = 'elementary'
                if debug: print(im.profile)
                
            elif(eta == 'middle'):
                im .profile[0] = 'middle'
                if debug: print(im.profile)
            
        activity = im.ask('activity')
            
        if(activity == 'recycle'):
            im.profile[3] = 'recycle'
            ans_rec = im.ask('recycle') #TODO come impostare la rispota
            garbage_class = ''
            ans_rec = 'see_object'
            if(ans_rec == 'see_object'):
                if(im.profile[0] == 'elementary'):
                    im.executeModality('IMAGE', 'img/trash/walle.jpg')
                im.executeModality('TEXT', 'Let me see the object')
                time.sleep(5)
                #TODO 
                # chiamare per fare object detection
                garbage_class = random.choice(['paper', 'compost', 'plastic', 'waste'])
            elif(ans_rec == 'object'):
                garbage_class = random.choice(['paper', 'compost', 'plastic', 'waste'])
    
            im.executeModality('TEXT', "It's "+garbage_class+"!")
            im.executeModality('IMAGE', garbage_bin[garbage_class])
            time.sleep(5)
            im.executeModality('TEXT', "I'm searching for the best path to the "+garbage_class+" bin")
            im.executeModality('IMAGE', 'img/trash/loading-25.gif')      
            #TODO              
            #fare pezzo del caricamento della mappa con il percorso
            time.sleep(10)
            im.ask('maps', timeout = 5)
            finished = True
            time.sleep(10)

        elif(activity == 'news'):
            im.profile[3] = 'news'
            
            while not finished:
                pagina = im.ask('news')
                im.executeModality('IMAGE', '')
                #button = im.executeModality('BUTTONS', [('exit', 'EXIT'), ('back', 'BACK')])
                if pagina == '1':
                    button = im.ask('microplastics', timeout = 15)
                elif pagina == '2':
                    button = im.ask('pollution', timeout = 15)
                elif pagina == '3':
                    button = im.ask('fashion', timeout = 15)
                else:
                    button = im.ask('recycled', timeout = 15)        

                if button == 'exit': finished = True
                elif button == 'back': finished = False
                elif button == 'timeout':finished = True
            
            #im.display.loadUrl('https://bitbucket.org/mtlazaro/modim/src/master/')


        elif(activity == 'play'):
            im.profile[3] = 'play'
            if debug: print(im.profile)
            st = im.ask('play_welcome', timeout = 15)
            if st == 'start':
                finished = giochino()
            im.executeModality('TEXT', 'Waiting...')
            time.sleep(10)

        if finished: im.execute('goodbye')


        im.init()           #ritorno alla schermata iniziale


if __name__ == "__main__":

    mws = ModimWSClient()

    # local execution
    mws.setDemoPathAuto(__file__)

    mws.run_interaction(i1)     #i1, i2 sono i task che deve compiere, capire se fare funzioni separate o un unico flusso su una funzione 
                                #all'interno definisco classi, e faccio un grande while True con degli elif? 
