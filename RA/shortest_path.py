import warnings
warnings.filterwarnings("ignore")
import sys
sys.path.append("KR_RL/mazelab")
sys.path.append("planning/unified_planning")

import random
import json
import numpy as np
import matplotlib.pyplot as plt
import gym
import wandb
from KR_RL.school_map import create_map
from KR_RL.q_learning import Q_learning
from planning.unified_planning.HRI_RA_planner import plan

# mapping between positions for PDDL planning visualization
global states2cells
states2cells = json.load(open("planning/states2cells.json","r"))

global trash_cans, fullness
trash_cans = {'plastic': [(16,1),(18,27),(2,28)], 'paper': [(18,7),(18,26),(7,28)], 'trash': [(15,12),(1,20)], 'compost': [(1,1),(11,6),(12,28)]}
fullness = {(16,1): 0, (18,27): 0, (2,28): 0, (18,7): 0, (18,26): 0, (7,28): 0, (15,12): 0, (1,20): 0, (1,1): 0, (11,6): 0, (12,28): 0}

##################################################################################################################################
####################################################### UTILITY FUNCTIONS ########################################################
def update_fullness(coords):
    fullness[coords] += 1

def is_full(coords):
    n = fullness[coords]
    if n == 3: 
        return True
    else: 
        return False

def random_closed(n):
    doors = [(13,3), (2,7), (9,7), (13,9), (14,21), (12,22), (7,22), (2,22), (5,26)]
    random_closed = random.sample(doors, n)
    return random_closed

def define_goals(trash_can):
    goals = []
    for i in trash_cans[trash_can]:
        if not is_full(i):
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

if __name__ == "__main__":
    plot_stats = False # variable to set if we want to plot "cumulative rewards" for RL algorithms
    if plot_stats:
        random.seed(30) # for reproducibility
    
    garbage_type = "plastic" # given by the 'application' --> we need to take it from somewhere :)
    
    goals = define_goals(garbage_type) # we set the goals
    doors_closed = random_closed(3) # we randomly close 3 dooors of the school map
    
    # create the environment
    agent_start_pos = (15,17)
    x = generate_matrix(agent_start_pos, goals, doors_closed)
    my_map = create_map(x, trash_cans, window_size_x=3000, window_size_y=2000)
    problem_id = int(random.random()*100)
    plt.imshow(my_map)
    plt.savefig(f'../imgs/map/map_goals_{problem_id}.png')
    matrix = [[row * 30 + col for col in range(30)] for row in range(20)]
    
    ###############################################################################################
    # now we can solve the problem of finding the shortest route to the bins in 3 different ways: #
    # - PDDL solver                                                                               #
    # - Q-learning with epsilon-greedy                                                            #
    # - LTLf-based reward shaping                                                                 #
    ###############################################################################################
    
    shortest_path, bin_to_update = [], (0,0) # the two values we need to return
    # we choose randomly which technique to use...
    which_method = random.randint(1,3)
    if which_method == 1: # planning
        print("PDDL PLANNING")
        ris_plan, bin_to_update = plan(garbage_type, fullness, doors_closed)
        if ris_plan is not None: # a plan exists 
            # convert plan from STATES to CELLS (for visualization purposes)
            for i in range(len(ris_plan)):
                ris_plan[i] = states2cells[ris_plan[i]]
        else:
            ris_plan = "<NO PLAN FOUND>"
        
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
        _, agent, goal = env.reset()
        state = matrix[agent[0][0]][agent[0][1]]
        shortest_path = [state]
        done = False
        while not done:
            action = np.argmax(Q_TABLE[state])
            pos, _, done, _, _ = env.step(action)
            state = matrix[pos[1][0]][pos[1][1]]
            shortest_path.append(state)
    
        # update bins
        bin_to_update = find_value(matrix, shortest_path[-1])
        update_fullness(bin_to_update)
    
    # show the path computed
    for s in shortest_path[:-1]:
        i,j = find_value(matrix, s)
        x[i,j] = 2
    my_map_path = create_map(x, trash_cans, window_size_x=3000, window_size_y=2000)
    plt.imshow(my_map_path)
    plt.savefig(f'../imgs/map/map_path_{problem_id}.png')