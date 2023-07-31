* Run websocket server on port 9000

python websocket_pepper.py


* Run HTML/JavaScript GUI from a browser

Option 1 (external PC)

http://<IP_ROBOT>/apps/spqrel/blockly/blockly_robot.html

Option 2 (Pepper tablet)

cd pepper_tools/tablet
python show_web.py --url blockly/blockly_robot.html


* Connect to robot

Use IP of the robot or 198.18.0.1 from the robot tablet.


* Enjoy Pepper-Blockly programming.


### Command server/client

* Server:

    python pepper_cmd_server.py 

* Client:

    python pepper_send_program.py --program test.py


