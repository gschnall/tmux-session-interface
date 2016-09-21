t=tmux

# Start session + name window 0 'server'
$t new-session -d
# Split window vertically 
$t split-window -d -t 0 -h

# Go back to first pane in window 1
$t select-pane -t 0

# Append Session/start
$t a 
