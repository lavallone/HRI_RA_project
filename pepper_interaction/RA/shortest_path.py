import warnings
warnings.filterwarnings("ignore")
import sys
sys.path.append("KR_RL/mazelab")
sys.path.append("planning/unified_planning")

import random
import json
import socket
import threading
import numpy as np
import matplotlib.pyplot as plt
import gym
import wandb
from KR_RL.school_map import create_map
from KR_RL.q_learning import Q_learning
from planning.unified_planning.HRI_RA_planner import plan

states2cells = json.load(open("planning/states2cells.json","r")) # mapping between positions for PDDL planning visualization
trash_cans = {'plastic': [(16,1),(18,27),(2,28)], 'paper': [(18,7),(18,26),(7,28)], 'trash': [(15,12),(1,20)], 'compost': [(1,1),(11,6),(12,28)]}

##################################################################################################################################
####################################################### UTILITY FUNCTIONS ########################################################
def update_fullness(fullness, coords):
    fullness[str(coords)] += 1
    # we update the json file
    json.dump(fullness, open("fullness.json", "w"))

def is_full(fullness, coords):
    n = fullness[str(coords)]
    if n == 3: 
        return True
    else: 
        return False

def random_closed(n):
    doors = [(13,3), (2,7), (9,7), (13,9), (14,21), (12,22), (7,22), (2,22), (5,26)]
    random_closed = random.sample(doors, n)
    return random_closed

def define_goals(fullness, trash_can):
    goals = []
    for i in trash_cans[trash_can]:
        if not is_full(fullness, i):
            goals.append(i)
    return goals

def generate_matrix(agent, goals, random_closed):
    x = np.array([[1, 1, 1, 1, 1, 1 ,1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 4, 0, 0, 0, 0, 0, 1, 0, 0, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 5, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 6, 1],
                    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1 ,1, 1, 0, 0, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 7, 1],
                    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1 ,1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1],
                    [1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 5, 0, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 6, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 1, 0, 7, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 7, 6, 0, 1],
                    [1, 1, 1, 1, 1, 1 ,1, 1, 1, 1, 1, 1, 1, 9, 9, 9, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]], dtype=np.uint8)

    x[agent[0], agent[1]] = 2
    for i in goals:
        x[i[0], i[1]] = 8
    for i in random_closed:
        x[i[0], i[1]] = 9
    return x

def find_value(matrix, value):
    rows = len(matrix)
    cols = len(matrix[0])
    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] == value:
                return i, j
    # Value not found
    return -1, -1
##################################################################################################################################

def handle_client(client_socket, client_address):
    try:
        print("Connected to:", client_address)
        while True:
            plot_stats = False # variable to set if we want to plot "cumulative rewards" for RL algorithms
            if plot_stats:
                random.seed(30) # for reproducibility
                
            # receive data from the client --> (garbage class)
            garbage_type = client_socket.recv(1024).decode('utf-8')
            if not garbage_type:
                break
            print("Received:", garbage_type)
            fullness = json.load(open("fullness.json", "r"))
            
            goals = define_goals(fullness, garbage_type) # we set the goals
            doors_closed = random_closed(3) # we randomly close 3 dooors of the school map
            # create the environment
            agent_start_pos = (15,17)
            x = generate_matrix(agent_start_pos, goals, doors_closed)
            my_map = create_map(x, trash_cans, window_size_x=3000, window_size_y=2000)
            problem_id = int(random.random()*100)
            plt.imshow(my_map)
            map_goals_path = f'../imgs/map/map_goals_{problem_id}.png'
            plt.savefig(map_goals_path)
            matrix = [[row * 30 + col for col in range(30)] for row in range(20)]
            
            ###############################################################################################
            # now we can solve the problem of finding the shortest route to the bins in 3 different ways: #
            # - PDDL solver                                                                               #
            # - Q-learning with epsilon-greedy                                                            #
            # - LTLf-based reward shaping                                                                 #
            ###############################################################################################
            
            shortest_path, bin_to_update = [], (0,0) # the two values we need to return (if there exist the path)
            is_path = 1
            # we choose randomly which technique to use...
            which_method = random.randint(1,3)
            if which_method == 1: # planning
                print("PDDL PLANNING")
                ris_plan, bin_to_update = plan(garbage_type, fullness, doors_closed)
                # a plan exists
                if ris_plan is not None: 
                    # convert plan from STATES to CELLS (for visualization purposes)
                    for i in range(len(ris_plan)):
                        ris_plan[i] = states2cells[ris_plan[i]]
                
                    # the fact is that the plan generated by the planner doesn't consider the cells occupied by doors,
                    # so to display correctly the path to reach the goal we need to overcome this little problem...
                    cells_adj_doors = [363, 423, 66, 68, 276, 278, 429, 369, 471, 411, 383, 381, 233, 231, 83, 81, 206, 146]
                    cells_adj_doors = set(cells_adj_doors)
                    states2cells_doors = {363 : 393, 423 : 393, 66 : 67, 68 : 67, 276 : 277, 278 : 277, 429 : 399, 369 : 399, 471 : 441, 411 : 441, 381 : 382, 383 : 382, 233 : 232, 231 : 232, 83 : 82, 81 : 82, 206 : 176, 146 : 176}
                    shortest_path = []
                    for i in range(len(ris_plan)):
                        shortest_path.append(ris_plan[i])
                        if ris_plan[i] in cells_adj_doors:
                            if ris_plan[i+1] in cells_adj_doors:
                                shortest_path.append(states2cells_doors[ris_plan[i]])
                        else:
                            continue
                # if a plan doesn't exist
                else:
                    is_path = 0
                
            elif which_method == 2 or which_method == 3: # RL
                if which_method == 2:
                    print("SIMPLE Q-LEARNING")
                    reward_shaping = False
                else:
                    print("REWARD SHAPING")
                    reward_shaping = True
                
                # initialize gym environment
                gym.envs.register(id='my_env', entry_point="KR_RL.environments:MyEnv", kwargs={'x': x}, max_episode_steps=200)
                env = gym.make('my_env')
                
                if plot_stats:
                    wandb.login()
                    with wandb.init(entity="lavallone", project="HRI_RA", name="LTLf shaping", mode="online"):
                        Q_TABLE = Q_learning(env, plot_stats, matrix, reward_shaping=reward_shaping)
                    wandb.finish()
                else:
                    Q_TABLE = Q_learning(env, plot_stats, matrix, reward_shaping=reward_shaping)
                
                # compute the BEST PATH according to the best policy
                _, agent, _ = env.reset()
                state = matrix[agent[0][0]][agent[0][1]]
                shortest_path = [state]
                done = False
                counter = 0
                while not done:
                    if counter > 100:
                        break
                    action = np.argmax(Q_TABLE[state])
                    pos, _, done, _, _ = env.step(action)
                    state = matrix[pos[1][0]][pos[1][1]]
                    shortest_path.append(state)
                    counter += 1
                
                # this means we didn't find a path 
                if not done:
                    shortest_path =  []
                    is_path = 0
                else:
                    bin_to_update = find_value(matrix, shortest_path[-1])
            
            # update bins only if the path exists
            if is_path == 1:
                update_fullness(fullness, bin_to_update)
            
            # show the path computed
            for s in shortest_path[:-1]:
                i,j = find_value(matrix, s)
                x[i,j] = 2
            my_map_path = create_map(x, trash_cans, window_size_x=3000, window_size_y=2000)
            plt.imshow(my_map_path)
            map_bestpath_path = f'../imgs/map/map_path_{problem_id}.png'
            plt.savefig(map_bestpath_path)
            
            ris = str(map_goals_path)+","+str(map_bestpath_path)+","+str(is_path)
            # send the modified data back to the client
            client_socket.sendall(ris.encode("utf-8"))
    
    except Exception as e:
        print("Error:", e)
    finally:
        client_socket.close()
        print("Connection closed with:", client_address)
 
    
if __name__ == "__main__":
    # create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind the socket to a specific address and port
    server_address = ('127.0.0.1', 3031)
    server_socket.bind(server_address)
    # listen for incoming connections (max 1 pending connection)
    server_socket.listen(5)
    print("Waiting for a connection...") 
    try:
        while True:
            # accept a connection
            client_socket, client_address = server_socket.accept()
            # start a new thread to handle the client connection
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
    except KeyboardInterrupt:
        print("Server is shutting down...")
    finally:
        # clean up the server socket
        server_socket.close()