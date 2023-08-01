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


def behaviour():
    
    garbage_bin = {'plastic': 'img/trash/bin_plastic.png', 
               'paper':'img/trash/bin_paper.png', 
               'compost':'img/trash/bin_compost.png', 
               'waste':'img/trash/bin_waste.png'}

    key_words = {'plastic': ['bottle', 'coke', 'can', 'water'], 
                 'paper': ['notebook','sheet', 'copybook', 'newspaper', 'mail'], 
                 'trash':['snack', 'dirty', 'coffee'], 
                 'compost':['apple', 'banana', 'fruit', 'bread', 'food', 'sandwich']}

    DEBUG = True
    im.init()   
    
    fd_w = open('/home/robot/playground/info_people.txt', 'a')
    fd_r = open('/home/robot/playground/info_people.txt', 'r')
    

    #print(im.robot.alive)
    #im.robot.setAlive(True)
    #print(im.robot.isConnected)
    
    finished = False
    p_back = False          #True if there is a people behind pepper
    new_user = ''

    def onTouched(value):
        print('IN ON-TOUCHED', value)
        im.executeModality('TTS', 'Hey Do not touch me!')
    
    anyTouch = im.robot.memory_service.subscriber("TouchChanged")

    #im.robot.people_service = im.robot.app.session.service("ALPeoplePerception")
    ##print(im.robot.people_service)
    ##print(im.robot.memory_service.getData('TouchChanged'))

    #idAnyTouch = anyTouch.signal.connect(onTouched)
    #print(im.robot.memory_service.getEventList())
    
    while True:
        finished = False
        someone = False

        read = fd_r.read()
        if DEBUG: print('La READ:', read)
        list_peoples = []
        list_peoples = read.split('\n')
        if DEBUG: print('LIST PEOPLEE', list_peoples)

        im.robot.startSensorMonitor()
        idAnyTouch = anyTouch.signal.connect(onTouched)
        
        while(not someone): 
            #ask = im.ask(None)
            sensor = im.robot.sensorvalue()     #--> 0laser, 1 sonarfront, 2sonarback, 3head, 4hand, 4hand
            if DEBUG: print(sensor)
            time.sleep(2)
            if sensor[2] > 0.0 and sensor[2] < 1.5:
                time.sleep(5) 
                if sensor[2] > 0.0 and  sensor[2] < 1.5: 
                    im.executeModality('TTS', 'Do you need help? Come here!')
                    time.sleep(3)
                    p_back = True
                    while (p_back):
                        sensor = im.robot.sensorvalue()
                        if DEBUG: print(sensor)
                        #im.executeModality('IMAGE', 'img/pepper.back.jpg')
                        im.executeModality('TTS', 'Do you need help? Come here!')
                        if sensor[1] > 0.0 and sensor[1] < 1.5:
                            someone = True
                            print('I HAVE DETECT ONE PEOPLE FOR MORE THAN 5 SECONDS')
                            #start interaction
                            #continue
                        elif sensor[2] > 1.5: p_back = False
                else: print('I am alone!')
            if sensor[1] > 0.0 and sensor[1] < 1.5:
                time.sleep(3)
                if sensor[1] > 0.0 and sensor[1] < 1.5: 
                    someone = True
                    #continue

        im.robot.stopSensorMonitor()    

        #print('VOCA', im.vocabulary)

        if someone:                 #start interaction
            im.ask('presentation', timeout = 10)
            new_user = im.robot.memory_service.getData('FakeRobot/ASR')
            #new_user = 'leo lavalle 10'
            #print(new_user)
            new_user_s = new_user.split(' ')
            #print(new_user_s)

            #lo metto in un while??
            if new_user not in list_peoples:
                fd_w.write(new_user+'\n')
                age = 'timeout'
                while(age == 'timeout'):
                    age = im.ask('welcome', timeout=15)
                    if(age == 'elementary'):
                        im.profile[0] = 'elementary'
                        if DEBUG: print(im.profile)
                        
                    elif(age == 'middle'):
                        im.profile[0] = 'middle'
                        if DEBUG: print(im.profile)
                        #modifiare interazione con bambino elementari, vedi foglio (1)
                        #if int(new_user[2]) < int('11'):
                            #im.executeModality('TEXT', 'Maybe you have selected the wrong choice! Are not you from the elementary school?')
                            #im.executeModality('TTS', 'Maybe you have selected the wrong choice! Are not you from the elementary school?')
                            #im.executeModality('BUTTONS', [('yes', 'YES'), ('no', 'NO')])
                            #ans_age = im.ask(None, timeout = 15) #cambaire ask
                            #if ans_age == 'yes':
                                #im.profile[0] = 'elementary'
                                
                                #if DEBUG: print(im.profile)
                    #MODIFY PROFILE - lasciare solo vocale
                    #im.executeModality('TEXT', 'Hi '+new_user[0]+' 'new_user[1]+', what do you want to do?')
                    #im.executeModality('TTS', 'Hi '+new_user[0]+' 'new_user[1]+', what do you want to do?')
                    #inserire parte di presentation su quello che fa
                    #add gesture di saluto

            else:
                if int(new_user_s[2]) < int('11'): im.profile[0] = 'elementary'
                else: im.profile[0] = 'middle'
                #MODIFY PROFILE - lasciare solo vocale
                #im.executeModality('TEXT', 'Welcom back '+new_user[0]+' 'new_user[1]+', what do you want to do?')
                #im.executeModality('TTS', 'Welcom back '+new_user[0]+' 'new_user[1]+', what do you want to do?')
                #vedi testo

        activity = im.ask('activity', timeout = 25)
            
        if(activity == 'recycle'):
            im.profile[3] = 'recycle'
            im.ask('recycle', timeout = 15) #only asr answer
            ans_rec = im.robot.memory_service.getData('FakeRobot/ASR')
            print('ANSSSSS RECCC', ans_rec)
            ans_rec = ans_rec.split(' ')
            garbage_class = '' 
            
            for w in ans_rec:
                for k in key_words.keys():
                    if w in key_words[k]:
                        garbage_class = k
                        break

            print('GARBAGE KEy', garbage_class)
            
            if(garbage_class == ''):
                if(im.profile[0] == 'elementary'):
                    im.executeModality('IMAGE', 'imgs/trash/walle.jpg')
                im.executeModality('TEXT', 'Let me see the object') #cambiare il text aggiungere tts
                time.sleep(5)

                img_path = "data/users_imgs/"+str(random.randint(1, 20))+".jpg"
                garbage_class, ris_img_path= im.detect_garbage(img_path)
                im.executeModality('IMAGE', 'vision/garbage_detection/'+ris_img_path)
                time.sleep(5)
            
            im.executeModality('IMAGE', 'imgs/map/map.png')
            im.executeModality('TTS', 'This is the map of the school, these are the available bins in which you can throw your object')
            
            map_goals_path, map_bestpath_path =im.shortest_path(garbage_class)
            map_goals_path = map_goals_path[3:]
            map_bestpath_path = map_bestpath_path[3:]


            im.executeModality('IMAGE', map_goals_path)
            im.executeModality('TTS', 'Now I will show you the fastest path to reach the '+garbage_class+' bin')
            im.executeModality('IMAGE', 'imgs/loading/loading-25.gif')   
            time.sleep(5)
            im.executeModality('IMAGE', map_bestpath_path)
            im.executeModality('TTS', "Here's the path!")
            time.sleep(10)

            finished = True

        elif(activity == 'news'):
            im.profile[3] = 'news'
            
            while not finished:
                article = im.ask('news')
                im.executeModality('IMAGE', '')
                #button = im.executeModality('BUTTONS', [('exit', 'EXIT'), ('back', 'BACK')])
                article = int(article)-1
                
                pages = ['microplastics', 'pollution', 'fashion', 'recycled']
                print(pages)
                button = im.ask(pages[article], timeout = 25)        

                if button == 'exit': finished = True
                elif button == 'back': finished = False
                elif button == 'timeout':finished = True
            
            #im.display.loadUrl('https://bitbucket.org/mtlazaro/modim/src/master/')


        elif(activity == 'play'):
            im.profile[3] = 'play'
            if DEBUG: print(im.profile)
            st = im.ask('play_welcome', timeout = 15)
            if st == 'start':
                finished = im.super_recycling_game()
                im.executeModality('TEXT', 'Waiting...')
            else:
                finished = True
                im.executeModality('TEXT', 'Exiting...')
            time.sleep(10)
            
        if finished: 
            im.execute('goodbye')
            feed = im.ask('feedback', timeout = 20)

        ### mettere in attesa finche non si allontana (tramite laser e sonar)        

        anyTouch.signal.disconnect(idAnyTouch)    

        tm = int(time.time())
        im.robot.memory_service.insertData('Device/SubDeviceList/Platform/Front/Sonar/Sensor/Value', 0.0)
        im.robot.memory_service.insertData('Device/SubDeviceList/Platform/Back/Sonar/Sensor/Value', 0.0)

        print(im.robot.sensorvalue())
        im.init() 


if __name__ == "__main__":

    mws = ModimWSClient() # $MODIM_HOME$/src/GUI/ws_client.py
    mws.setDemoPathAuto(__file__)
    mws.run_interaction(behaviour)