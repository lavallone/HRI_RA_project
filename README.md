# HRI_RA_project
Project for the **H**uman **R**obot **I**nteraction and **R**easoning **A**gents modules belonging to the *Elective in AI* course at Sapienza University.
* **docker** folder contains the scripts to *build* and *run* the ***pepper-hri*** image.
  ```
  cd docker/
  ./build.bash
  ./run.bash
  docker exec -it pepperhri tmux a
  ```
* **src** folder is a copy of what it's contained in our local machines in "*/home/user_name/src*" (***modim*** and ***pepper-tools*** ).
* finally **pepper_interaction** is the main folder in which we developed all the code to make the interaction happens.
## Set up ⚙
* Create a *python conda environment* to be able to run (outside the ***pepper-hri*** docker container), two *services* developed by us: the **garbage detector** based on YOLOv5 and the **shortest path** planner to indicate the nearest bin where to throw waste items. The latter consists of 3 different strategies (a classical PDDL planner, a Q-learning RL algorithm and a reward shaping method based on $LTL_f$ goal specifications). These two *services* are provided through *sockets* mechanism.
  ```
  # run this command in the following folders (within the created conda environment): 
  # pepper_interaction/RA/planning
  # pepper_interaction/RA/KR_RL
  # pepper_interaction/vision/garbage_detection
  # pepper_interaction/vision/garbage_detection/yolov5
  pip install -r requirements.txt
  ```
  Run to set up the socket servers:
  ```
  python pepper_interaction/vision/garbage_detection/GarbageDet_detect.py
  ```
  ```
  python pepper_interaction/RA/shortest_path.py
  ```
* In the *docker* container we first need to run the **modim server**:
  ```
  python ws_server.py -robotport <ROBOT_PORT_NUMBER>
  ```
  Then the script to simulate users behaviours:
  ```
  python human_interaction_fake.py -robotport <ROBOT_PORT_NUMBER>
  ```
  Finally the python code to run the actual interaction with Pepper robot:
  ```
  python main_beahaviour.py
  ```
  
  <img src="https://i.imgur.com/FDRb0dM.png"  width="300" height="60">
  
