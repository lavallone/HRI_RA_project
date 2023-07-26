import numpy as np
import random
from tqdm import tqdm
import time
import wandb

def compute_reward_shaping(agent, old_state, new_state, goal, scale_factor=10, reward_shaping_gamma=1):
    # (PBRS function)
    # F = reward_shaping_gamma*phi_new - phi_old
    n = np.max([abs(g[0]-agent[0])+abs(g[1]-agent[1]) for g in goal])
    
    # first we compute phi (old state)
    min_manhattan_distance_old = np.min([abs(g[0]-old_state[0])+abs(g[1]-old_state[1]) for g in goal])
    phi_old = -scale_factor * (1 + (min_manhattan_distance_old / n))
    
    # then we compute phi_new (new state)
    min_manhattan_distance_new = np.min([abs(g[0]-new_state[0])+abs(g[1]-new_state[1]) for g in goal])
    phi_new = -scale_factor * (1 + (min_manhattan_distance_new / n))
    
    # if the state is the one of the goals --> we return 0!
    is_goal = False
    for g in goal:
        is_goal |= (g[0]==new_state[0] and g[1]==new_state[1])
    if is_goal:
        return 0
    
    return (reward_shaping_gamma*phi_new) - phi_old

# simple Q-LEARNING routine with epsilon-greedy strategy
def Q_learning(env, plot_stats, matrix, reward_shaping = False, alpha = 0.1, gamma = 0.9, eps_init = 0.1, eps_final = 0.0001, max_episodes = 500):
    
    Q_TABLE = np.zeros([600, 4])

    # generate epsilon values for epsilon-greedy strategy (exponential decay)
    eps_decay_factor = (eps_final/eps_init) ** (1/max_episodes)
    epsilons = []
    for _ in range(max_episodes):
        eps_init = max(eps_final, eps_init*eps_decay_factor)
        epsilons.append(eps_init)
    
    # start learning loop
    for i in tqdm(range(1, max_episodes+1)):
        cumulative_reward = 0
        _, agent, goal = env.reset() # each 'episode' we start over
        state = matrix[agent[0][0]][agent[0][1]]
        
        done = False
        start_time = time.time()
        while not done:
            # if the agent get stucked...
            if time.time()-start_time > 5:
                break
            
            if random.random() < epsilons[i-1]: # EXPLORE
                action = env.action_space.sample()
            else:
                action = np.argmax(Q_TABLE[state]) # EXPLOIT

            pos, reward, done, _, _ = env.step(action)
            cumulative_reward += reward
            old_state = matrix[pos[0][0]][pos[0][1]]
            new_state = matrix[pos[1][0]][pos[1][1]]
            
            # Q-TABLE UPDATE
            old_value = Q_TABLE[old_state, action]
            next_max = np.max(Q_TABLE[new_state])
            if reward_shaping:
                reward_shaping = compute_reward_shaping(agent[0], [pos[0][0], pos[0][1]], [pos[1][0], pos[1][1]], goal)
                reward += reward_shaping
            new_value = ((1 - alpha) * old_value) + (alpha * (reward + (gamma*next_max)))
            Q_TABLE[old_state, action] = new_value

            state = new_state

        if plot_stats:
            wandb.log({"cumulative_reward" : cumulative_reward})
    
    print("OPTIMAL POLICY computed.\n")
    return Q_TABLE