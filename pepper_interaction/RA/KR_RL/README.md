# Reasoning and Learning (KR+RL)

First of all, to have all the necessary libraries and packages you need to run:
```
pip install -r requirements.txt
%cd mazelab
pip install -e .
```
We implemented two *Reinforcement Learning* based algorithms. The first one is the standard **Q-learning** with $\epsilon$-greedy strategy. The second one is a novel approach which combines RL with *Knowledge Representation* (in particular $LTL_f$ formulas). The method is explained in the paper [LTLf-based Reward Shaping for Reinforcement Learning](https://cris.vub.be/ws/portalfiles/portal/67480798/ltlf_reward_shaping.pdf) and we compared the *cumulative rewards* of the two methods in [wandb](https://wandb.ai/lavallone/HRI_RA?workspace=user-lavallone).

> This is the environment where we made for our experiments. Its the school in which the students ask our **EnvironMate** robot where to throw garbage. In fact the colored circles in the map represents the bins (*plastic*, *paper*, *compost* and *trash*). This is of course the same grid world where also the *PDDL planner* has been executed.

<img src="map.png" width=540 height=380>