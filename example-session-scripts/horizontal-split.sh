#__________________________________________________
# This is a sample script that demonstrates how to 
# create your own custom sessions
#___________________________________________________
# Place this file in the session-scripts folder to
# see it appear in Tmux-Session-Manager
#TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT

t=tmux

# Start session + name window 0 'server'
$t new-session -d
# Split window horizontally 
$t split-window -d -t 0 -v

# Go back to first pane in window 1
$t select-pane -t 0

# Append Session/start
$t a 
