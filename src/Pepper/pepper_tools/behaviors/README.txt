How to save behavior and run it outside Coreographe

1. Start Coreograph, load and run the behavior you want to save.


2. In Robot Applications Tab, click "Package and install current project to the robot"


3. On the robot, go to pepper_tools/behaviors folder and run

python behavior.py --list

Check the name of the behavior that has been installed on the robot (it starts with the name of the project usually).


4. Start/stop the behavior with

python behavior.py --start <behaviorname>

python behavior.py --stop <behaviorname>


