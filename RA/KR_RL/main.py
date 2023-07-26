import random
import numpy as np
import matplotlib.pyplot as plt
from school_map import create_map
import gym
from q_learning import Q_learning
import wandb

global trash_cans, fullness
trash_cans = {'plastic': [(16,1),(18,27),(2,28)], 'paper': [(18,7),(18,26),(7,28)], 'general': [(15,12),(1,20)], 'edible': [(1,1),(11,6),(12,28)]}
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
    plot_stats = False
    if plot_stats:
        random.seed(30)
    
    goals = define_goals('paper')
    doors_closed = random_closed(3)
    
    # create the environment
    x = generate_matrix((15,17), goals, doors_closed)
    my_map = create_map(x, trash_cans, window_size_x=3000, window_size_y=2000)
    plt.imshow(my_map)
    plt.savefig('../imgs/my_map_goals.png')

    # initialize gym environment
    gym.envs.register(id='my_env', entry_point="environments:MyEnv", kwargs={'x': x}, max_episode_steps=200)
    env = gym.make('my_env')
    
    matrix = [[row * 30 + col for col in range(30)] for row in range(20)]
    if plot_stats:
        wandb.login()
        with wandb.init(entity="lavallone", project="HRI_RA", name="LTLf shaping", mode="online"):
            Q_TABLE = Q_learning(env, plot_stats, matrix, reward_shaping=True)
        wandb.finish()
    else:
        Q_TABLE = Q_learning(env, plot_stats, matrix, reward_shaping=True)
    
    # compute the BEST PATH according to the best policy
    _, agent, goal = env.reset()
    state = matrix[agent[0][0]][agent[0][1]]
    best_steps = [state]
    done = False
    while not done:
        action = np.argmax(Q_TABLE[state])
        pos, _, done, _, _ = env.step(action)
        state = matrix[pos[1][0]][pos[1][1]]
        best_steps.append(state)
    
    # update bins
    i,j = find_value(matrix, best_steps[-1])
    update_fullness((i,j))
    
    # show the path computed by Q-Learning algorithm
    for s in best_steps[:-1]:
        i,j = find_value(matrix, s)
        x[i,j] = 2
    my_map_path = create_map(x, trash_cans, window_size_x=3000, window_size_y=2000)
    plt.imshow(my_map_path)
    plt.savefig('../imgs/my_map_path.png')