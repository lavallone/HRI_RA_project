# coding=utf-8
import sys
import time
import os
import random
import threading


# Set MODIM_IP to connnect to remote MODIM server
try:
    sys.path.insert(0, os.getenv('MODIM_HOME')+'/src/GUI')
except Exception as e:
    print("Please set MODIM_HOME environment variable to MODIM folder.")
    sys.exit(1)

import ws_client
from ws_client import *

sys.path.append(os.getenv('PEPPER_TOOLS_HOME')+'/cmd_server')

def behaviour():
    
    garbage_bin = {'plastic': 'img/trash/bin_plastic.png', 
               'paper':'img/trash/bin_paper.png', 
               'compost':'img/trash/bin_compost.png', 
               'waste':'img/trash/bin_waste.png'}

    key_words = {'plastic': ['bottle', 'coke', 'can', 'water'], 
                 'paper': ['notebook','sheet', 'copybook', 'newspaper', 'paper', 'mail'], 
                 'trash':['snack', 'dirty', 'coffee'], 
                 'compost':['apple', 'banana', 'fruit', 'bread', 'food', 'sandwich']}

    DEBUG = True
    im.init()   
    
    finished = False
    p_back = False          #True if there is a people behind pepper
    new_user = ''

    def onTouched(value):
        print('IN ON-TOUCHED', value)

        #####################
        thread = threading.Thread(target = lambda: im.robot.notouch(age = "elementary")) 
        thread.start()
        #####################

        im.executeModality('TTS', 'Hey Do not touch me!')
        time.sleep(1)
    

    anyTouch = im.robot.memory_service.subscriber("TouchChanged")

    #im.robot.people_service = im.robot.app.session.service("ALPeoplePerception")
    ##print(im.robot.people_service)
    ##print(im.robot.memory_service.getData('TouchChanged'))

    #idAnyTouch = anyTouch.signal.connect(onTouched)
    #print(im.robot.memory_service.getEventList())

    '''
    im.robot.animation_player_service = im.robot.app.session.service("ALAnimationPlayer")
    im.robot.beh_service = im.robot.app.session.service("ALBehaviorManager")
    im.robot.al_service = im.robot.app.session.service("ALAutonomousLife")
    im.robot.rp_service = im.robot.app.session.service("ALRobotPosture")
    im.robot.bm_service = im.robot.app.session.service("ALBackgroundMovement")
    im.robot.ba_service = im.robot.app.session.service("ALBasicAwareness")
    im.robot.sm_service = im.robot.app.session.service("ALSpeakingMovement")

    im.robot.alive = True
    '''
    
    while True:

        finished = False
        someone = False

        read = open('/home/robot/playground/info_people.txt', 'r').read()
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

                ######################
                im.robot.turnHead()
                ######################

                time.sleep(5) 
                if sensor[2] > 0.0 and  sensor[2] < 1.5: 
                    
                    ##############################################
                    thread = threading.Thread(target = im.robot.turnHead) 
                    thread.start()
                    ##############################################

                    im.executeModality('TTS', 'Do you need help? Come here!')
                    time.sleep(3)
                    p_back = True
                    while (p_back):
                        sensor = im.robot.sensorvalue()
                        if DEBUG: print(sensor)
                        time.sleep(5)
                        #im.executeModality('IMAGE', 'img/pepper.back.jpg')

                        ##############################################
                        thread = threading.Thread(target = im.robot.turnHead) 
                        thread.start()
                        ##############################################

                        im.executeModality('TTS', 'Do you need help? Come here!')
                        if sensor[1] > 0.0 and sensor[1] < 1.5:
                            someone = True
                            print('I HAVE DETECT ONE PEOPLE FOR MORE THAN 5 SECONDS')
                            p_back = False
                            #start interaction
                            #continue
                        elif sensor[2]== 0.0 or  sensor[2] > 1.5: p_back = False
                else: print('I am alone!')
            if sensor[1] > 0.0 and sensor[1] < 1.5:
                time.sleep(3)
                if sensor[1] > 0.0 and sensor[1] < 1.5: 
                    someone = True
                    #continue

        im.robot.stopSensorMonitor()

        #print('VOCA', im.vocabulary)

        
        if someone:                 #start interaction
            
            #######################################
            im.robot.hello('elementary')
            thread = threading.Thread(target = lambda: im.robot.talkingfast(age = "elementary")) 
            thread.start()
            #######################################

            im.profile[1] = 'a'
            im.execute('presentation')
            time.sleep(10)
            new_user = im.robot.memory_service.getData('FakeRobot/ASR')

            print(new_user)
            new_user_s = new_user.split(' ')
            print(new_user_s)

            #da mettere nell'if new?

            #######################################
            thread = threading.Thread(target = lambda: im.robot.talkingfast1(age = "elementary")) 
            thread.start()
            #######################################

            im.executeModality('TEXT', 'How old are you?')
            im.executeModality('TTS', 'and, How old are you"')
            time.sleep(5)
            new_user_age = im.robot.memory_service.getData('FakeRobot/ASR')
            print(new_user_age)
           
            for elem in list_peoples:
                elem = elem.split(' ')
                print(elem)
                if elem[0] == new_user_s[0] and elem[1] == new_user_s[1]: 
                    new = False
                    print(elem[2])
                    old_user_school = elem[2]
                    break
                else: new = True 
            if new:
                open('/home/robot/playground/info_people.txt', 'a').write(new_user)
                age = 'timeout'
                im.profile[1] = 'new'
                #####
                if int(new_user_age) < 11:
                    im.profile[0] = 'elementary'
                    while(age == 'timeout'):

                        ##################
                        thread = threading.Thread(target = lambda: im.robot.talkingfast2(age = "elementary")) 
                        thread.start()
                        ##################

                        age = im.ask('welcome', timeout=15)      
                        if age == 'elementary': open('/home/robot/playground/info_people.txt', 'a').write(' elementary\n')
                        if(age == 'middle'):
                            open('/home/robot/playground/info_people.txt', 'a').write(' middle\n')
                            im.profile[0] = 'middle'
                            if DEBUG: print(im.profile)
                    #MODIFY PROFILE - lasciare solo vocale

                    #im.executeModality('TEXT', 'Hi '+new_user_s[0]+' '+new_user_s[1]+', what do you want to do?')

                    #################
                    thread = threading.Thread(target = lambda: im.robot.talking(age = im.profile[0])) 
                    thread.start()
                    #################

                    im.executeModality('TTS', 'Hi '+new_user_s[0]+' '+new_user_s[1]+'.')
                    im.execute('presentation')
                    time.sleep(5)
                    #inserire parte di presentation su quello che fa
                    #add gesture di saluto
                
                else: 
                    im.profile[0] = 'middle'
                    open('/home/robot/playground/info_people.txt', 'a').write(' middle\n')
                    im.profile[0] = 'middle'
                    if DEBUG: print(im.profile)
                    #################
                    thread = threading.Thread(target = lambda: im.robot.talking(age = 'middle')) 
                    thread.start()
                    #################
                    im.executeModality('TTS', 'Hi '+new_user_s[0]+' '+new_user_s[1]+'.')
                    im.execute('presentation')
                    time.sleep(5)
                

            else:
                if old_user_school ==  'elementary': im.profile[0] = 'elementary'
                else: im.profile[0] = 'middle'
                im.profile[1] = 'old'
                #MODIFY PROFILE - lasciare solo vocale
                #im.executeModality('TEXT', 'Welcom back '+new_user[0]+' 'new_user[1]+', what do you want to do?')

                #################
                thread = threading.Thread(target = lambda: im.robot.talkingfast(age = im.profile[0])) 
                thread.start()
                #################

                im.executeModality('TTS', 'Welcome back '+new_user_s[0]+' '+new_user_s[1]+'.')
                im.execute('presentation')
                time.sleep(5)
                #vedi testo
        
        
        #################
        thread = threading.Thread(target = lambda: im.robot.talkingfast1(age = im.profile[0])) 
        thread.start()
        #################

        activity = im.ask('activity', timeout = 25)
            
        if(activity == 'recycle'):
            im.profile[3] = 'recycle'

            if im.profile[1] == 'new':
                #################
                thread = threading.Thread(target = lambda: im.robot.talking(age = im.profile[0])) 
                thread.start()
                #################
            else: 
                #################
                thread = threading.Thread(target = lambda: im.robot.talkingfast2(age = im.profile[0])) 
                thread.start()
                #################
            
            im.ask('recycle', timeout = 15) #only asr answer
            ans_rec = im.robot.memory_service.getData('FakeRobot/ASR')
            print('ANS REC', ans_rec)
            ans_rec = ans_rec.split(' ')
            garbage_class = '' 
            
            for w in ans_rec:
                for k in key_words.keys():
                    if w in key_words[k]:
                        garbage_class = k
                        break

            print('GARBAGE KEY', garbage_class)
            
            if(garbage_class == ''):
                if(im.profile[0] == 'elementary'): im.executeModality('IMAGE', 'imgs/trash/walle.jpg')
                im.executeModality('TEXT', 'Let me see the object') #cambiare il text aggiungere tts
                img_path = "data/users_imgs/"+str(random.randint(1, 20))+".jpg"

                #### DA VEDERE SE INSERIRE UNA THINKING MENTRE RICONOSCE L'IMMAGINE
                #thread = threading.Thread(target = im.robot.thinking) 
                #thread.start()
                #thread = threading.Thread(target = im.robot.lookhere) 
                #thread.start()

                garbage_class, ris_img_path= im.detect_garbage(img_path)
                #ris_img_path = "../../../../playground/vision/garbage_detection/"+ris_img_path
                time.sleep(5)
                im.executeModality('IMAGE', 'vision/garbage_detection/'+ris_img_path)
                time.sleep(5)
            
            
            #################
            thread = threading.Thread(target = lambda: im.robot.talkingfast(age = im.profile[0])) 
            thread.start()
            #################

            im.executeModality('IMAGE', 'imgs/map/map.png')
            im.executeModality('TTS', 'This is the map of the school, these are the available bins in which you can throw your object')
            
            # bisogna provare a vedere quanto dura il finding dello shortest path 
            # (corrisponde a quanto tempo l'immagine verrà mostrata)
            map_goals_path, map_bestpath_path = im.shortest_path(garbage_class)
            map_goals_path = map_goals_path[3:]
            map_bestpath_path = map_bestpath_path[3:]

            # dovrebbe dire qualcosa in riferimento alla mappa con i goals (con gesture che indica il tablet)
            im.executeModality('IMAGE', map_goals_path)
            time.sleep(5)

            #### THINKING MENTRE FA FINTA DI CERCARE IL PATH
            #################
            thread = threading.Thread(target = lambda: im.robot.thinking(age = im.profile[0])) 
            thread.start()
            #################

            im.executeModality('TTS', 'Now I will show you the fastest path to reach the '+garbage_class+' bin')
            im.executeModality('IMAGE', 'imgs/loading/loading-25.gif')   
            time.sleep(5)

            #################
            thread = threading.Thread(target = lambda: im.robot.lookhere(age = im.profile[0])) 
            thread.start()
            #################

            im.executeModality('IMAGE', map_bestpath_path)
            im.executeModality('TTS', "Here's the path!")
            time.sleep(10)

            finished = True

        elif(activity == 'news'):
            im.profile[3] = 'news'
            
            im.display.display_image("imgs/paper.png", place='left')
            im.display.display_image("imgs/plastic.png")
            im.display.display_image("imgs/fashion.png", place='right')
            im.display.display_text("News ♻", "default")
            im.display.display_newsbuttons([["fashion", "Fashion pollution", "https://earth.org/fast-fashions-detrimental-effect-on-the-environment/"], 
                                            ["plastic", "Plastic in oceans", "https://oceanliteracy.unesco.org/plastic-pollution-ocean/"],
                                            ["paper", "Paper recycling" , "https://www.twosides.info/paper-packaging-is-recycled-more-than-any-other-material"]
                                            ])
            '''
            if qualcosa == fashion:
                im.executeModality('TTS', 'Did you know that "fashion production" comprises 10% of total global carbon emissions, as much as the European Union? And it dries up water sources and pollutes rivers and streams, while 85% of all textiles go to dumps each year? Take a look at this article to learn about "Fast Fashion and Its Environmental Impact".')
            elif qualcosa == plastic:
                im.executeModality('TTS', 'Did you know that plastic is one of the most enduring materials man has created? And it is possible that it does not even fully degrade, but becomes what we call microplastic? Take a look at this article to learn about the presence of plastic in our oceans.')
            else:
                im.executeModality('TTS', 'Did you know that paper packaging is the most recycled packaging material in Europe? Take a look at the article to deepen the topic.')
            '''

            while not finished:
                time.sleep(10)
                im.executeModality('TTS', 'Have you finished reading?')
                # qui a loop ogni tot secondi il robot chiede allo user se ha finito...
                # appena gli risponde di si --> si setta finished=True ed esce dal loop!
            
                ans_news = im.robot.memory_service.getData('FakeRobot/ASR')
                time.sleep(5)
                if ans_news == 'yes': finished = True
                

            im.display.remove_buttons()
            im.display.display_image("", place='left')
            im.display.display_image("")
            im.display.display_image("", place='right')
            im.display.display_text("", "default")
            '''
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
            '''

        elif(activity == 'play'):
            im.profile[3] = 'play'
            if DEBUG: print(im.profile)

            #################
            thread = threading.Thread(target = lambda: im.robot.lookhere(age = 'elementary')) 
            thread.start()
            #################

            st = im.ask('play_welcome', timeout = 15)
            if st == 'start':
                finished = im.super_recycling_game()

                ##########################
                thread = threading.Thread(target = lambda: im.robot.exultation(age = 'elementary')) 
                thread.start()
                ##########################

                im.executeModality('TEXT', 'Waiting...')
            else:
                finished = True
                im.executeModality('TEXT', 'Exiting...')
            time.sleep(5)
            
        if finished: 

            # Thread con hello 
            #################
            thread = threading.Thread(target = lambda: im.robot.hello(age = im.profile[0])) 
            thread.start()
            #################

            im.execute('goodbye')
            feed = im.ask('feedback', timeout = 20)

            # CREARE GESTURES 1-2 TRISTE, 3 MEZZO MEZZO, 4-5 FELICE 
            if feed == '1' or feed == '2':
                im.robot.happy(im.profile[0]) 
            elif feed == '3':
                im.robot.normal(im.profile[0])
            else: 
                im.robot.sad(im.profile[0])

            # robot deve avere una reazione diversa a seconda dello score rating

        ### mettere in attesa finche non si allontana (tramite laser e sonar)        

        anyTouch.signal.disconnect(idAnyTouch)    

        im.robot.memory_service.insertData('Device/SubDeviceList/Platform/Front/Sonar/Sensor/Value', 0.0)
        im.robot.memory_service.insertData('Device/SubDeviceList/Platform/Back/Sonar/Sensor/Value', 0.0)

        print(im.robot.sensorvalue())
        im.init() 


if __name__ == "__main__":

    mws = ModimWSClient() # $MODIM_HOME$/src/GUI/ws_client.py
    mws.setDemoPathAuto(__file__)
    mws.run_interaction(behaviour)