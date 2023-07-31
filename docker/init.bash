#!/bin/bash

SESSION=init

tmux -2 new-session -d -s $SESSION

tmux rename-window -t $SESSION:0 'naoqi'
tmux new-window -t $SESSION:1 -n 'human_simulation'
tmux new-window -t $SESSION:2 -n 'pepper_interaction'
tmux new-window -t $SESSION:3 -n 'modim_server'

tmux send-keys -t $SESSION:0 "cd /opt/Aldebaran/naoqi-sdk-2.5.5.5-linux64" C-m
tmux send-keys -t $SESSION:1 "cd ~/playground/scripts" C-m
tmux send-keys -t $SESSION:2 "cd ~/playground/scripts" C-m
tmux send-keys -t $SESSION:3 "cd src/modim/src/GUI" C-m


while [ 1 ]; do
  sleep 60;
done


