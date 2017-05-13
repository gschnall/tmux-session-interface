t=tmux
wd="~/Documents/workspace/r-projects/express-react-easy-setup"
et=enter

$t new-session -d 
$t split-window -d -t 0 -h
$t split-window -d -t 1 -v
$t split-window -d -t 1 -v

$t send-keys -t 0 "cd "$wd $et
$t send-keys -t 0 'vim' $et
$t send-keys -t 3 "cd "$wd $et
$t send-keys -t 3 "vim ." $et

$t send-keys -t 2 "cd "$wd $et
$t send-keys -t 2 "node" $et
$t send-keys -t 1 "cd "$wd $et

$t a 
$t select-pane -t 0
