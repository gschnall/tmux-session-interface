#!python2
import subprocess
import os
import sys

# print os.path.realpath(__file__) # file path
# os.path.expanduser("~") # home dir
    
def main():
    scriptDir = sys.path[0]
    scripts = os.listdir(scriptDir + '/session-scripts')
    print scripts
    prHeader()
    prScripts(scripts)
    handleInput(scriptDir, scripts)

def prHeader():
    print ''
    print '|:::::|::::|::::|::::::::::::|'
    print '|-->  -|-  -|-  -|- --  -->  |'
    print '|-----|Your|Tmux|Sessions----|'
    print '|-->  -|-  -|-  -|- --  -->  |'
    print '|:::::|::::|::::|::::::::::::|'
    print ''

def prScripts(scripts):
    print '0: Quit Your Tmux Sessions'
    print '**************************'
    for script in scripts:
        print str(scripts.index(script)+1) + ': ' + script.split('.')[0]
    print ''

def handleInput(scriptDir, scripts):
    session = raw_input("What session would you like to start?\n")
    if int(session) == 0:
        print 'Exiting'
        print ''
    elif session.isdigit() and (int(session)-1) < len(scripts):
        file = scripts[int(session)-1]
        subprocess.call(["sh", scriptDir+"/session-scripts/" + scripts[int(session)-1]])
    elif not (session.isdigit()):
        print '' 
        print "please enter a number"
        print '' 
        handleInput()
    else:
        print '' 
        print "...Session file not available"
        print '' 
        handleInput()


# start
main()
