import pepper_cmd
from pepper_cmd import *


begin()

pepper_cmd.robot.setAlive(True)
pepper_cmd.robot.showurl('index.html')
pepper_cmd.robot.setLanguage('Italian')
pepper_cmd.robot.setVolume(50)
pepper_cmd.robot.say('Ciao.')

end()

