# name of session
session='sample-session'
# Main Directory
wd="~/Documents"
# Command to start a server
server=''
# -Variables for quicker composition-
t=tmux
et=enter
sk=send-keys

# Start session + name window 0 'server'
$t new-session -d -s $session -n server 
# Enter change directory to working direcotry
$t $sk -t 0 "cd "$wd $et
# Enter commane to start our server
$t $sk -t 0 'npm start' $et 
# Split window vertically
$t split-window -d -t 0 -h
$t $sk -t 1 "cd "$wd $et

# create new window named 'editor'
$t new-window -t $session:1 -n editor 
$t split-window -d -t 0 -h
$t split-window -d -t 1 -v

$t $sk -t 0 "cd "$wd $et
$t $sk -t 0 'vim' $et
$t $sk -t 2 "cd "$wd $et
$t $sk -t 2 "vim ." $et

$t $sk -t 1 "cd "$wd $et
$t $sk -t 1 "node" $et

# Go back to first pane in window 1
$t select-pane -t 0

# Append Session/start
$t a 
