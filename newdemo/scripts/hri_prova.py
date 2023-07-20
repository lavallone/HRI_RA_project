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

    def face_detection():
        print('faceDetection')

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
    
    finished = False
    someone_people = ''
    list_peoples = []

    while True:
        finished = False
        someone = False
        while(not someone): 
            ask = im.ask(None)
            sensor = im.robot.sensorvalue()     #--> 0laser, 1 sonarfront, 2sonarback, 3head, 4hand, 4hand
            if debug: print(sensor)
            '''if sensor[2] < 1.5:
                time.sleep(5) 
                if sensor[2] < 1.5: 
                    im.executeModality('TTS', 'Do you need help? Come here!')
                    time.sleep(3)
                    if sensor[1] < 1.5:
                        #start interaction
                        face_detection()
                        #someone = True
                        #continue
                else: print('I am alone!')
            if sensor[1] < 1.5:
                time.sleep(3)
                if sensor[1] < 1.5: 
                    face_detection()
                    #someone = True
                    #continue'''


            someone = True 
            '''if someone == True
            someone_people = 'Piero'
            '''


        #TODO
        #if someone_people not in list_peoples: 
            # chiedo la scuola, faccio i controlli e aggiungo le info etc
            # else :leggo info list people, setto il profilo giusto e vado diretto a riga ---  activity = im.ask('activity') (farla fuori dall if)

        age = 'timeout' ##
        face_age = ['elementary', 'middle']
        while(age == 'timeout'):
            age = im.ask('welcome', timeout=15)
            if(age == 'elementary'):
                im.profile[0] = 'elementary'
                if debug: print(im.profile)
                
            elif(age == 'middle'):
                im.profile[0] = 'middle'
                if debug: print(im.profile)
                
                if face_age[0] != 'middle':
                    im.executeModality('TEXT', 'Maybe you have selected the wrong choice! Are not you from the elementary school?')
                    im.executeModality('TTS', 'Maybe you have selected the wrong choice! Are not you from the elementary school?')
                    im.executeModality('BUTTONS', [('yes', 'YES'), ('no', 'NO')])
                    ans_age = im.ask(None, timeout = 15)
                    if ans_age == 'yes':
                        im.profile[0] = 'elementary'
                        if debug: print(im.profile)
        #else: ####    
        #im.profile[0] = someone_people.scholl
        # im.executeModality('TEXT', 'Hi someone_people.name, what do you want to do?' )
        # im.executeModality('TTS', 'Hi someone_people.name, what do you want to do?')
        #
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
            im.executeModality('IMAGE', 'img/loading/loading-25.gif')      
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
            else:
                finished = True
                im.executeModality('TEXT', 'Exiting...')
            time.sleep(10)
            
        if finished: 
            feed = im.ask('feedback', timeout = 20)
            im.execute('goodbye')


        im.init()           #ritorno alla schermata iniziale


if __name__ == "__main__":

    mws = ModimWSClient()

    # local execution
    mws.setDemoPathAuto(__file__)

    mws.run_interaction(i1)     #i1, i2 sono i task che deve compiere, capire se fare funzioni separate o un unico flusso su una funzione 
                                #all'interno definisco classi, e faccio un grande while True con degli elif? 
