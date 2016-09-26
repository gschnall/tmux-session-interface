#!python2
import subprocess
import os
import sys
import re
import time

# print os.path.realpath(__file__) # file path
# os.path.expanduser("~") # home dir

def main():
  class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

  # fetch scripts
  scriptDir = sys.path[0]
  scripts = os.listdir(scriptDir + '/session-scripts')
  # fetch sessions
  currentSessions = getSessions()
  sessions = generateAllSessions(currentSessions[1], scripts)
  userInSession = currentSessions[0]
  # print user menu
  prHeader(bcolors)
  prScripts(scripts, sessions, userInSession, bcolors)
  # handle user input
  if userInSession:
    handleActiveSession(currentSessions[2], sessions)
  else:
    handleInput(scriptDir, sessions, scripts)

  subprocess.call(['clear'])

# ::PRINTING FUNCTIONS
def prHeader(col):
  subprocess.call(['clear'])
  print ''
  print col.OKGREEN + '|:::::|::::|:::|:::::::::::|' + col.ENDC
  print col.OKBLUE  + '|--  -|-  -|-  |-- --  --  |' + col.ENDC
  print col.BOLD    + '|---| Tmux-Session-Manager |' + col.ENDC
  print col.OKBLUE  + '|--  -|-  -|-  |-- --  --  |' + col.ENDC
  print col.OKGREEN + '|:::::|::::|:::|:::::::::::|' + col.ENDC
  print ''

def getSessions():
  sessions = {}
  sessData = [False, [], False]
  # Get tmux ls output
  tmuxls = subprocess.Popen(["tmux","ls"], stdout=subprocess.PIPE)
  tls = tmuxls.communicate()
  tlsArr = map(str,tls)
  sessionArr = tlsArr[0].strip().split('\n')
  # Create Arr out with detached or attached sessions
  for sess in sessionArr:
    if re.search('\(attached\)', sess) > -1:
      sessionArr[sessionArr.index(sess)] = "a:" + sess
      sessData[0] = True
      sessData[2] = sess.split(":")[0]
    else:
      sessionArr[sessionArr.index(sess)] = "d:" + sess
  # return Session Aray
  sessData[1] = sessionArr
  return sessData

def color_text(color, text):
  endc = '\033[0m'
  colors = {
    "blue":'\033[94m',
    "green":'\033[92m',
    "yellow":'\033[93m',
    "red":'\033[91m',
  }
  if(color):
    return colors[color.lower()] + text + endc 
  else:
    return "Color must be in string for: " + text


# ||Basic return functions------||
def mapsessions(arr):
  return map(lambda a: a.split(':')[1], arr)

def mapstates(arr):
  return map(lambda a: a.split(':')[0], arr)

def mapscriptnames(arr): # s: for script
  return map(lambda a: "s:" + a.split('.')[0], arr)

def getState(session): # script, attached, detached
  if session == "d:":
    return False 
  else:
    return session.split(":")[0]

def getName(session):
  return session.split(":")[1]

def returnKillNumb(st):
  return int(re.findall(r'\d+', st)[0])

def stlowrmsp(inp): #str lower & remove spaces
  return str(inp).replace("  ","").lower()

def killText(col, n):
    return " (" + col.FAIL + "k" + str(n) + col.ENDC + ":kill)"
# ||---------------------------||

def generateAllSessions(sessions, scripts):
  scriptsArr = mapscriptnames(scripts)
  scriptCp = [] + scriptsArr
  allSessions = [] + scriptsArr
  for s in sessions:
    sessName = getName(s)
    if "s:"+sessName in scriptsArr:
        allSessions[scriptCp.index("s:"+sessName)] = s
    else:
      allSessions.insert(0, s)
      scriptCp.insert(0,'123*PlaceHolder*321')
  return allSessions

def selectAction(sessNumb, sessions, scripts, scriptDir):
  #:: Handle empty first session in session list 
  s_num = sessNumb-1 if a_session_is_alive(sessions) else sessNumb
  sessionName = getName(sessions[s_num])
  sessState = getState(sessions[s_num])
  if sessState == "a": 
    subprocess.call(["tmux", "detach", "-s" + sessionName])
  elif sessState == "d":
    subprocess.call(["tmux", "attach-session", "-t" + sessionName])
  else:
    subprocess.call(["sh", scriptDir+"/session-scripts/" + sessionName +'.sh'])

def startSession():
  sessionName = raw_input("Session Name: ")
  subprocess.call(["tmux", "new", "-s" + sessionName])

def killAllSessions():
  subprocess.call(["killall", "tmux"])

def killSession(sessions, sessNumb):
  if( sessions[sessNumb-1] > -1 ):
    subprocess.call(["tmux", "kill-session", "-t" + getName(sessions[sessNumb-1])])
  else:
    print "...Session number not found."
    print "Exiting..."
    time.sleep(2000)
    print "  "

def a_session_is_alive(sessions):
  return sessions[0] != "d:"

def is_attached(session):
  sessState = getState(session)
  if sessState == "a": 
    return "attached" 
  elif sessState == "d": 
    return "detached" 
  elif sessState == "s":
    return "script" 
  else:
    return False

def start_session_horizontal_split():
  scriptDir = sys.path[0] + '/.important-session-scripts/'
  subprocess.call(["sh", scriptDir+"horizontal.sh"])

def start_session_vertical_split():
  scriptDir = sys.path[0] + '/.important-session-scripts/'
  subprocess.call(["sh", scriptDir+"vertical.sh"])

def horizontally_split_window():
  subprocess.call(['tmux', 'split-window', '-v'])

def vertically_split_window():
  subprocess.call(['tmux', 'split-window', '-h'])

def switch_pane():
  OKBLUE = '\033[94m'
  ENDC = '\033[0m'
  subprocess.call(['tmux', 'display-panes'])
  subprocess.call(['clear'])
  print ""
  print color_text('blue', 'q') + ':' + 'Quit Tmux-Session-Manager' + OKBLUE + ' s' + ENDC + ':' + 'show pane numbers'
  paneNumb = raw_input("Switch to pane number: ")
  if paneNumb == "q" or paneNumb == "quit":
    print 'Exiting'
    print ''
  elif paneNumb == "s":
    subprocess.call(['tmux', 'display-panes'])
    switch_pane()
  elif paneNumb.isdigit():
    subprocess.call(['tmux', 'select-pane', '-t ' + str(paneNumb)])

def prNoneActive(col, scripts):
  for script in scripts:
    print col.OKBLUE + str(scripts.index(script)+1) + col.ENDC + ': ' + script.split('.')[0] + " (" + col.OKBLUE + str(scripts.index(script)+1) + col.ENDC + ":start" +  ")"

def prNoneAttached(col, sessions):
  for ind, s in enumerate(sessions): 
    sessName = getName(s)
    if is_attached(s) == "detached":
      print color_text('blue', str(ind+1)) + ': ' + sessName + " (" + color_text('green', str(ind+1)) + ":attach" + ")" + killText(col, ind+1)
    elif is_attached(s) == "script":
      print color_text('blue', str(ind+1)) + ': ' + sessName + " (" + color_text('blue', str(ind+1)) + ":start" +  ")"

def prSessionAttached(col, sessions):
  print "- " + col.OKBLUE + "You are in a session" + col.ENDC
  print '**************************'
  for ind, s in enumerate(sessions):
    sessName = getName(s)
    if is_attached(s) == "detached":
      print col.OKBLUE + str(ind+1) + col.ENDC + ': ' + sessName + " (" + col.WARNING + "Session-Detached" + col.ENDC + ")" + killText(col, ind+1)
    elif is_attached(s) == "attached":
        print col.OKBLUE + str(ind+1) + col.ENDC + ': ' + sessName + " (" + col.WARNING + "d" + col.ENDC + ":detach" +  ")" + killText(col, ind+1)
    elif is_attached(s) == "script":
      print col.OKBLUE + str(ind+1) + col.ENDC + ': ' + sessName

def printInSessionOptions(col):
  print col.OKBLUE + 'q' + col.ENDC + ':' + ' Quit Tmux-Session-Manager'
  print col.OKBLUE + 's' + col.ENDC + ':' + ' Switch Pane'
  print col.OKBLUE + 'vs' + col.ENDC + ':' + ' Vertical Split' + " | " + col.OKBLUE + 'hs' + col.ENDC + ':' + ' Horizontal Split'
  print col.FAIL + 'ka' + col.ENDC + ':' + ' Kill All Tmux Sessions'

def printDefaultOptions(col, sessions):
  print col.OKBLUE + 'q' + col.ENDC + ':' + ' Quit Tmux-Session-Manager'
  print col.OKBLUE + 'n' + col.ENDC + ':' + ' New Tmux Session'
  print col.OKBLUE + 'vs' + col.ENDC + ':' + ' Vertical Split' + " | " + col.OKBLUE + 'hs' + col.ENDC + ':' + ' Horizontal Split'
  if a_session_is_alive(sessions):
    print col.FAIL + 'ka' + col.ENDC + ':' + ' Kill All Sessions'

def printSessionInformation(col, sessions):
  if a_session_is_alive(sessions): 
    return
  else:
    print "- " + col.OKBLUE + "No current active sessions" + col.ENDC
    print '**************************'


def prScripts(scripts, sessions, userInSession, col):
  if userInSession:
    printInSessionOptions(col)
  else:
    printDefaultOptions(col, sessions)
  print '**************************'
  printSessionInformation(col, sessions)
  # Continue printing rest of program
  attachedSession = False
  activeSession = False
  # Check if a session is attached
  for s in sessions: 
    if is_attached(s) == "attached":
      attachedSession = True
    elif is_attached(s) == "detached":
     activeSession = True 
  # Print functions 
  if( attachedSession ):
    prSessionAttached(col, sessions)
  elif( activeSession ): 
    prNoneAttached(col, sessions)
  else:
    prNoneActive(col, scripts)
  # Print padding
  print ''

def handleInput(scriptDir, sessions, scripts):
  session = raw_input("What session would you like to start?\n")
  print sessions
  if session == "0" or session == "q" or session == "quit":
    print 'Exiting'
    print ''
  elif stlowrmsp(session) == "hs":
    start_session_horizontal_split()
  elif stlowrmsp(session) == "vs":
    start_session_vertical_split()
  elif stlowrmsp(session) == "n":
    startSession()
  elif stlowrmsp(session) == "ka" or stlowrmsp(session[0]) == "kall" or stlowrmsp(session[0]) == "killall":
    killAllSessions()
  elif stlowrmsp(session[0]) == "k" and re.findall(r'\d+', stlowrmsp(session)) != []:
    killSession(sessions, returnKillNumb(stlowrmsp(session)))
  elif session.isdigit() and int(session)-1 < len(sessions):
    selectAction(int(session), sessions, scripts, scriptDir)
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

def handleActiveSession(activeSessName, sessions):
  session = raw_input("Would you like to detach session, kill it, or quit? (d,k,q)\n")
  if session == "0" or session == "q" or session == "quit":
    print 'Exiting'
    print ''
  elif stlowrmsp(session) == "hs":
    horizontally_split_window()
  elif stlowrmsp(session) == "vs":
    vertically_split_window()
  elif stlowrmsp(session) == "s":
    switch_pane()
  elif stlowrmsp(session[0]) == "ka" or stlowrmsp(session[0]) == "kall" or stlowrmsp(session[0]) == "killall":
    killAllSessions()
  elif stlowrmsp(session[0]) == "k" and re.findall(r'\d+', stlowrmsp(session)) != []:
    killSession(sessions, returnKillNumb(stlowrmsp(session)))
  elif stlowrmsp(session[0]) == "k":
    subprocess.call(["tmux", "kill-session", "-t" + activeSessName])
  elif stlowrmsp(session[0]) == "d" or stlowrmsp(session.split(' ')[0]) == "detach":
    subprocess.call(["tmux", "detach", "-s" + activeSessName])
  else:
    print '' 
    print "...You are Currently in a Session"
    print '' 
    handleActiveSession(activeSessName, sessions)


# start
main()
