wd="~/Documents/workspace/r-projects/express-react-easy-setup"
name="odev-tmux"
server='npm start'
t=tmux
et=enter
sk=send-keys

$t new-session -d -s $name -n server 
$t $sk -t 0 "cd "$wd $et
$t $sk -t 0 'npm start' $et 
$t split-window -d -t 0 -h
$t $sk -t 1 "cd "$wd $et

$t new-window -t $name:1 -n editor 
$t split-window -d -t 0 -h
$t split-window -d -t 1 -v

$t $sk -t 0 "cd "$wd $et
$t $sk -t 0 'vim' $et
$t $sk -t 2 "cd "$wd $et
$t $sk -t 2 "vim ." $et

$t $sk -t 1 "cd "$wd $et
$t $sk -t 1 "node" $et

$t select-pane -t 0

$t a 
