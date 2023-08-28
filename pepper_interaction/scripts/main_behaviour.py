# coding=utf-8
import sys
import time
import os
import random
import threading

# set MODIM_IP to connnect to remote MODIM server
try:
    sys.path.insert(0, os.getenv('MODIM_HOME')+'/src/GUI')
except Exception as e:
    print("Please set MODIM_HOME environment variable to MODIM folder.")
    sys.exit(1)

from ws_client import *
sys.path.append(os.getenv('PEPPER_TOOLS_HOME')+'/cmd_server')


def behaviour():
    
    def onTouched(value):
        print('ON-TOUCHED', value)
        ########## GESTURE ##########
        thread = threading.Thread(target = lambda: im.robot.notouch(age = "elementary")) 
        thread.start()
        #############################
        im.executeModality('TTS', 'Hey Do not touch me!')
        time.sleep(2)

    key_words = {'plastic': ['bottle', 'coke', 'can', 'water'], 
                 'paper': ['notebook','sheet', 'copybook', 'newspaper', 'paper', 'mail'], 
                 'trash':['snack', 'dirty', 'coffee'], 
                 'compost':['apple', 'banana', 'fruit', 'bread', 'food', 'sandwich']}
    finished = False
    p_back = False # True if there is a people behind pepper
    new_user = ''
    
    im.init()
    anyTouch = im.robot.memory_service.subscriber("TouchChanged")
    
    # main loop
    while True:

        finished = False
        someone = False

        # we read users database
        read = open('/home/robot/playground/info_people.txt', 'r').read()
        list_peoples = []
        list_peoples = read.split('\n')

        im.robot.startSensorMonitor()
        idAnyTouch = anyTouch.signal.connect(onTouched)
        
        # we wait for people to interact with
        while(not someone): 
            sensor = im.robot.sensorvalue() # 0-->laser, 1-->sonar_front, 2-->sonar_back, 3-->touch_head, 4-->touch_rhand, 5-->touch_lhand
            time.sleep(2)
            
            # if someone is back to the robot
            if sensor[2] > 0.0 and sensor[2] < 1.5:
                p_back = True
                im.executeModality('IMAGE', 'imgs/pepper/9.png')
                im.executeModality('TEXT', '♻️ <br> Do you need help? Come in front of me!')
                #time.sleep(20)
                # we keep asking to the user back to the robot to come in front to start the interaction
                while (p_back):
                    sensor = im.robot.sensorvalue()
                    time.sleep(2)
                    ########## GESTURE ##########
                    thread = threading.Thread(target = im.robot.turnHead) 
                    thread.start()
                    #############################
                    im.executeModality('TTS', 'Do you need help? Come in front of me!')
                    time.sleep(5)
                    # if someone comes in front of the robot we start the interaction
                    if sensor[1] > 0.0 and sensor[1] < 1.5:
                        someone = True
                        p_back = False
                        print('One people stood in front of the robot for at least 5 seconds')
                    # if there's nobody back anymore we exit the loop and we keep waiting for a user
                    elif sensor[2] == 0.0 or sensor[2] > 1.5: 
                        p_back = False
                        im.executeModality('IMAGE', 'imgs/pepper/1.png')
                        im.executeModality('TEXT', "♻️ <br> Welcome! <br> I'm <b>EnviroMate</b>, your green school advisor!")
            
            # if someone is in front of the robot for at least 5 seconds we start the interaction
            elif sensor[1] > 0.0 and sensor[1] < 1.5:
                time.sleep(5)
                if sensor[1] > 0.0 and sensor[1] < 1.5: 
                    someone = True
                    
            else: print("There's nobody to start an interaction with!")
        
        # we stop the liste to proximity sensors
        im.robot.stopSensorMonitor()
        
        # start interaction
        if someone:
            ########## GESTURE ##########
            im.robot.hello('elementary')
            thread = threading.Thread(target = lambda: im.robot.talkingfast(age = "elementary")) 
            thread.start()
            #############################

            im.profile[1] = 'a'
            im.execute('welcome_01')
            time.sleep(8)
            new_user = im.robot.memory_service.getData('FakeRobot/ASR')
            new_user_s = new_user.split(' ')

            ########## GESTURE ##########
            thread = threading.Thread(target = lambda: im.robot.talkingfast1(age = "elementary")) 
            thread.start()
            #############################

            im.executeModality('IMAGE', 'imgs/pepper/5.png')
            im.executeModality('TEXT', '♻️ <br> How old are you?')
            im.executeModality('TTS', 'and, How old are you?')
            time.sleep(8)
            new_user_age = im.robot.memory_service.getData('FakeRobot/ASR')
           
            for elem in list_peoples:
                elem = elem.split(' ')
                if elem[0] == new_user_s[0] and elem[1] == new_user_s[1]: 
                    new = False
                    old_user_school = elem[2]
                    break
                else: new = True 
            
            # new user
            if new:
                open('/home/robot/playground/info_people.txt', 'a').write(new_user)
                age = 'timeout'
                im.profile[1] = 'new'
                # age user differentiation
                # elementary school case
                if int(new_user_age) < 11:
                    im.profile[0] = 'elementary'
                    while(age == 'timeout'):
                        ########## GESTURE ##########
                        thread = threading.Thread(target = lambda: im.robot.talkingfast2(age = "elementary")) 
                        thread.start()
                        #############################
                        # we want to be sure that the user is a student from the elementary school
                        age = im.ask('welcome_02', timeout=15)
                        if age == 'elementary': open('/home/robot/playground/info_people.txt', 'a').write(' elementary\n')
                        if(age == 'middle'):
                            open('/home/robot/playground/info_people.txt', 'a').write(' middle\n')
                            im.profile[0] = 'middle'
                    ########## GESTURE ##########
                    thread = threading.Thread(target = lambda: im.robot.talking(age = im.profile[0])) 
                    thread.start()
                    #############################
                # middle school case
                else: 
                    im.executeModality('TTS', 'Ok great, you therefore go to secondary school!')
                    im.profile[0] = 'middle'
                    open('/home/robot/playground/info_people.txt', 'a').write(' middle\n')
                    im.profile[0] = 'middle'
                    ########## GESTURE ##########
                    thread = threading.Thread(target = lambda: im.robot.talking(age = 'middle')) 
                    thread.start()
                    #############################
                im.executeModality('TTS', 'Hi '+new_user_s[0]+' '+new_user_s[1]+'.')
                im.execute('welcome_01')
                time.sleep(5)
                
            # old user
            else:
                if old_user_school ==  'elementary': im.profile[0] = 'elementary'
                else: im.profile[0] = 'middle'
                im.profile[1] = 'old'
                ########## GESTURE ##########
                thread = threading.Thread(target = lambda: im.robot.talkingfast2(age = im.profile[0])) 
                thread.start()
                #############################
                im.executeModality('TTS', 'Welcome back '+new_user_s[0]+' '+new_user_s[1]+'!')
                im.execute('welcome_01')
                time.sleep(5)
        
        
        # let's start the activity which the user can experience
        ########## GESTURE ##########
        thread = threading.Thread(target = lambda: im.robot.talkingfast1(age = im.profile[0])) 
        thread.start()
        #############################
        activity = im.ask('activity', timeout = 25)
            
        if(activity == 'recycle'):
            im.executeModality('IMAGE', 'imgs/pepper/2.png')
            im.executeModality('TEXT', "♻️ <br> Let's recycle!")
            im.executeModality('TTS', "Let's recycle!")
            time.sleep(3)
            im.profile[3] = 'recycle'
            if im.profile[1] == 'new':
                ########## GESTURE ##########
                thread = threading.Thread(target = lambda: im.robot.talking(age = im.profile[0])) 
                thread.start()
                #############################
            else: 
                ########## GESTURE ##########
                thread = threading.Thread(target = lambda: im.robot.talkingfast2(age = im.profile[0])) 
                thread.start()
                #############################
            
            im.ask('recycle', timeout = 15) # we accept only asr answer
            ans_rec = im.robot.memory_service.getData('FakeRobot/ASR')
            ans_rec = ans_rec.split(' ')
            garbage_class = '' 
            # the user will try to tell the robot which object wants to recycle...
            for w in ans_rec:
                for k in key_words.keys():
                    if w in key_words[k]:
                        garbage_class = k
                        break
            print('GARBAGE KEY', garbage_class)
            # but if the robot cannot understand it, it will see the object and detect it thanks to 'garbage detector' neural network!
            if(garbage_class == ''):
                im.execute('see_object')
                time.sleep(3)
                im.executeModality('TEXT', 'Brings the object closer...')
                time.sleep(3)
                im.executeModality('IMAGE', 'imgs/recycle/camera_flash.gif')
                time.sleep(1)

                ########## GESTURE ##########
                thread = threading.Thread(target = lambda: im.robot.thinking(age = im.profile[0])) 
                thread.start()
                #############################
                # we take one random picure of a garbage object from our database...
                img_path = "data/users_imgs/"+str(random.randint(1, 20))+".jpg"
                # and we classify it
                garbage_class, ris_img_path= im.detect_garbage(img_path)
                im.executeModality('IMAGE', 'imgs/loading/3.gif')
                im.executeModality('TEXT', 'Processing image...')
                time.sleep(5)

                ########## GESTURE ##########
                thread = threading.Thread(target = lambda: im.robot.lookhere(age = im.profile[0])) 
                thread.start()
                #############################

                im.executeModality('IMAGE', 'vision/garbage_detection/'+ris_img_path)
                im.executeModality('TEXT', 'This is the detected object!')
                time.sleep(4)
            
            im.executeModality('IMAGE', 'imgs/recycle/'+garbage_class+'.png')
            im.executeModality('TEXT', "It's "+garbage_class+"!")
            time.sleep(3)
            
            ########## GESTURE ##########
            thread = threading.Thread(target = lambda: im.robot.talkingfast(age = im.profile[0])) 
            thread.start()
            #############################

            im.executeModality('IMAGE', 'imgs/map/map.png')
            im.executeModality('TEXT', "This is the school map. <br> The red square is where we are!")
            im.executeModality('TTS', 'This is the map of the school. The circles are the bins and the red square is where we are!')
            time.sleep(3)
            im.executeModality('TEXT', "I will now show you the shortest path to a not empty "+garbage_class+" bin!")
            im.executeModality('TTS', "I will now show you the shortest path to a not empty "+garbage_class+" bin!")
            time.sleep(3)
            
            # shortest path computation
            ########## GESTURE ##########
            thread = threading.Thread(target = lambda: im.robot.thinking(age = im.profile[0])) 
            thread.start()
            #############################
            im.executeModality('IMAGE', 'imgs/loading/3.gif')
            im.executeModality('TEXT', "Computing shortest path...")
            map_goals_path, map_bestpath_path, is_path = im.shortest_path(garbage_class)
            im.executeModality('IMAGE', 'imgs/pepper/7.png')
            im.executeModality('TEXT', "Last seconds...")
            time.sleep(3)
            # if there's no solution
            if int(is_path) == 0:
                print("NO PLAN FOUND")
                im.executeModality('IMAGE', 'imgs/recycle/no_plan.png')
                im.executeModality('TEXT', "There's no bin available!")
                time.sleep(3)
                im.executeModality('IMAGE', 'imgs/pepper/10.png')
                im.executeModality('TEXT', "I'm sorry... but you can come another time 😅")
                im.executeModality('TTS', "I'm sorry but there's no bin available, come another time.")
                time.sleep(3)
                finished = True
            # if there is a solution
            else:
                map_goals_path = map_goals_path[3:]
                map_bestpath_path = map_bestpath_path[3:]
                
                ########## GESTURE ##########
                thread = threading.Thread(target = lambda: im.robot.lookhere(age = im.profile[0])) 
                thread.start()
                #############################
                im.executeModality('IMAGE', map_goals_path)
                if garbage_class == 'compost': garbage_class = 'organic waste'
                if garbage_class == 'trash': garbage_class = 'general waste'
                im.executeModality('TEXT', 'The '+garbage_class+' bins which are not empty are now highlighted...')
                im.executeModality('TTS', 'The '+garbage_class+' bins which are not empty are now highlighted...')
                time.sleep(5)

                ########## GESTURE ##########
                thread = threading.Thread(target = lambda: im.robot.lookhere(age = im.profile[0])) 
                thread.start()
                #############################

                im.executeModality('IMAGE', map_bestpath_path)
                im.executeModality('TEXT', "And this is the best path! <br> Follow it and correctly recycle your waste!")
                im.executeModality('TTS', "And this is the best path!")
                time.sleep(10)
                finished = True

        elif(activity == 'news'):
            im.profile[3] = 'news'
            
            im.executeModality('IMAGE', 'imgs/pepper/3.png')
            im.executeModality('TEXT', "♻️ <br> Now I'll show you some environmental articles!")
            im.executeModality('TTS', "Now I'll show you some environmental articles! Feel free to read them all. Enjoy!")
            time.sleep(3)
            
            im.display.display_image("imgs/web_pages/paper.png", place='left')
            im.display.display_image("imgs/web_pages/plastic.png")
            im.display.display_image("imgs/web_pages/fashion.png", place='right')
            im.display.display_text("News ♻️", "default")

            while not finished:
                buttons = im.display.ask_newsb([["fashion", "Fashion pollution", "https://earth.org/fast-fashions-detrimental-effect-on-the-environment/"], 
                                    ["plastic", "Plastic in oceans", "https://oceanliteracy.unesco.org/plastic-pollution-ocean/"],
                                    ["paper", "Paper recycling" , "https://www.twosides.info/paper-packaging-is-recycled-more-than-any-other-material"]
                                    ], timeout = 20)
                if buttons == 'fashion':
                    im.executeModality('TTS', 'Did you know that "fashion production" comprises 10% of total global carbon emissions, as much as the European Union? And it dries up water sources and pollutes rivers and streams, while 85% of all textiles go to dumps each year? Take a look at this article to learn about "Fast Fashion and Its Environmental Impact".')
                elif buttons == 'plastic':
                    im.executeModality('TTS', 'Did you know that plastic is one of the most enduring materials man has created? And it is possible that it does not even fully degrade, but becomes what we call microplastic? Take a look at this article to learn about the presence of plastic in our oceans.')
                elif buttons == 'paper':
                    im.executeModality('TTS', 'Did you know that paper packaging is the most recycled packaging material in Europe? Take a look at the article to deepen the topic.')
                
                reading = True
                while reading:
                    # each 10 seconds the robot asks the user if it finished to read the articles
                    time.sleep(10)
                    im.executeModality('TTS', 'Have you finished reading?')
                    time.sleep(5)
                    ans_news_1 = im.robot.memory_service.getData('FakeRobot/ASR')
                    if ans_news_1 == 'yes': reading = False
                
                im.executeModality('TTS', 'Do you want to read another article?')
                time.sleep(5)
                ans_news_2 = im.robot.memory_service.getData('FakeRobot/ASR')
                if ans_news_2 == 'no': finished = True

            im.display.remove_buttons()
            im.display.display_image("", place='left')
            im.display.display_image("")
            im.display.display_image("", place='right')
            im.display.display_text("", "default")

        elif(activity == 'play'):
            im.profile[3] = 'play'
            im.executeModality('IMAGE', 'imgs/pepper/4.png')
            im.executeModality('TEXT', "♻️ <br> Now we'll play a quiz about recycling!")
            im.executeModality('TTS', "Now we'll play a quiz about recycling.! I hope you can guess all the answers. Enjoy!")
            time.sleep(3)

            ########## GESTURE ##########
            thread = threading.Thread(target = lambda: im.robot.lookhere(age = 'elementary')) 
            thread.start()
            #############################

            st = im.ask('play_welcome', timeout = 15)
            if st == 'start':
                finished = im.super_recycling_game()

                ########## GESTURE ##########
                thread = threading.Thread(target = lambda: im.robot.exultation(age = 'elementary')) 
                thread.start()
                #############################
                im.executeModality('TEXT', 'Waiting...')
            else:
                finished = True
                im.executeModality('TEXT', 'Exiting...')
            time.sleep(5)
        
        # when the activity is finished
        if finished: 

            ########## GESTURE ##########
            thread = threading.Thread(target = lambda: im.robot.hello(age = im.profile[0])) 
            thread.start()
            #############################

            if (activity == 'recycle' and int(is_path) == 1) or activity == 'news' or activity == 'play':
                im.execute('goodbye')
                time.sleep(4)
            feed = im.ask('feedback', timeout = 20)

            # GESTURES 1-2 SAD, 3 NORMAL, 4-5 HAPPY
            # the robot reacts to user feedback
            if feed == '1' or feed == '2':
                im.robot.sad(im.profile[0]) 
            elif feed == '3':
                im.robot.normal(im.profile[0])
            else: 
                im.robot.happy(im.profile[0])   
                im.executeModality('TTS', 'Thank you !')    

        anyTouch.signal.disconnect(idAnyTouch)    
        # setting manually the simualted absence of a person
        im.robot.memory_service.insertData('Device/SubDeviceList/Platform/Front/Sonar/Sensor/Value', 0.0)
        im.robot.memory_service.insertData('Device/SubDeviceList/Platform/Back/Sonar/Sensor/Value', 0.0)
        im.executeModality('IMAGE', "imgs/pepper/1.png")
        im.executeModality('TEXT', "Waiting for a human...")


if __name__ == "__main__":

    mws = ModimWSClient()
    mws.setDemoPathAuto(__file__)
    mws.run_interaction(behaviour)