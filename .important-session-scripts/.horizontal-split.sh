#---- !!!DO NOT DELETE OR EDIT ----
#---- !!!THIS SCRIPT IS USED IN THE SESSION MANAGER -----

t=tmux

# Start session + name window 0 'server'
$t new-session -d
# Split window horizontally 
$t split-window -d -t 0 -v

# Go back to first pane in window 1
$t select-pane -t 0

# Append Session/start
$t a 
