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
  # scripts = os.listdir(scriptDir + '/session-scripts')
  scripts = []
  # fetch sessions
  currentSessions = getSessions()
  sessions = generateAllSessions(currentSessions[1], scripts)
  userInSession = currentSessions[0]
  # print user menu
  prHeader()
  prScripts(scripts, sessions, userInSession, bcolors)
  # handle user input
  if userInSession:
    handleActiveSession(currentSessions[2], sessions)
  else:
    handleInput(scriptDir, sessions, scripts)

  subprocess.call(["sh", scriptDir+"/rebound-scripts/rebound.sh"])

# ::PRINTING FUNCTIONS
def prHeader():
  class col:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
  subprocess.call(['clear'])
  print ''
  print col.OKGREEN + '|:::::|::::|:::|:::::::::::::::::::|' + col.ENDC
  print col.OKBLUE  + '|--  -|-  -|-  |-- |--  --  -- -- -|' + col.ENDC
  print col.BOLD    + '|---| Tmux-Session-Manager \[O-O]/ |' + col.ENDC
  print col.OKBLUE  + '|--  -|-  -|-  |-- |--  --  -- ----|' + col.ENDC
  print col.OKGREEN + '|:::::|::::|:::|:::::::::::::::::::|' + col.ENDC
  print ''

def getSessions():
  sessions = {}
  sessData = [False, [], False]
  # -- Get tmux ls output --
  try:
    tmuxls = subprocess.Popen(["tmux","ls"], stdout=subprocess.PIPE)
    tls = tmuxls.communicate()
  except OSError as e:
    if e.errno == os.errno.ENOENT:
      warnUserThatTmuxIsNotInstaled() 
    else:
      raise
  # -- ------------------ --
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

# ||Rebound functions-----------||
def writeReboundScript(script):
  script = script + "&&clear" if script else "clear"
  f = open(sys.path[0] + "/rebound-scripts/rebound.sh", "w")
  f.write(script)
  f.close()

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

def getLenOfSessionName(session):
  return len(getName(session))

def truncateSessionName(sn, maxLength):
  return (sn[:maxLength-2] + '..') if len(sn) > maxLength else sn

def returnSessionNumber(st):
  return int(re.findall(r'\d+', st)[0])

def stlowrmsp(inp): #str lower & remove spaces
  return str(inp).replace("  ","").lower()

def killText(col, n):
  return " (" + col.FAIL + "k" + str(n) + col.ENDC + ":kill)"

def renameText(col, n):
  return " (" + col.WARNING + "r" + str(n) + col.ENDC + ":rename)"

def detachText(col, n):
  return " (" + col.WARNING + "d" + str(n) + col.ENDC + ":detach)"
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
    subprocess.call(["tmux", "detach", "-s " + sessionName])
  elif sessState == "d":
    subprocess.call(["tmux", "attach-session", "-t", sessionName])
  else:
    subprocess.call(["sh", scriptDir+"/session-scripts/" + sessionName +'.sh'])

def switchToSession(sessNumb, activeSessName, sessions):
  s_num = sessNumb-1 if a_session_is_alive(sessions) else sessNumb
  sessionName = getName(sessions[s_num])
  writeReboundScript("tmux attach-session -t " + sessionName)
  subprocess.call(["clear"])
  subprocess.call(["tmux", "detach", "-s", activeSessName])

def startSession():
  prHeader()
  sessionName = raw_input("\[O~O]/ --Session Name: ")
  subprocess.call(["tmux", "new", "-s", sessionName.strip()])

def killAllSessions():
  subprocess.call(["killall", "tmux"])

def killSession(sessions, sessNumb):
  if( sessions[sessNumb-1] > -1 ):
    subprocess.call(["tmux", "kill-session", "-t", getName(sessions[sessNumb-1])])
  else:
    print "...Session number not found."
    print "Exiting..."
    time.sleep(2000)
    print "  "

def renameSession(sessions, sessNumb):
  if( sessions[sessNumb-1] > -1 ):
    prHeader()
    sessionName = getName(sessions[sessNumb-1])
    newSessionName = raw_input("\[O~O]/ --Rename " + sessionName + " to: ")
    subprocess.call(["tmux", "rename-session", "-t", sessionName, newSessionName])
  else:
    print "...Session number not found."
    print "Exiting..."
    time.sleep(2000)
    print "  "

def detachSession(sessions, sessNumb):
  if( sessions[sessNumb-1] > -1 ):
    sessionName = getName(sessions[sessNumb-1])
    subprocess.call(["tmux", "detach", "-s", sessionName])
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
  prHeader()
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

def prNoneAttached(col, sessions, sessionNameLength, maxSessionNameLength):
  for ind, s in enumerate(sessions):
    sessName = truncateSessionName(getName(s), maxSessionNameLength)
    snl = getLenOfSessionName(s)
    spaces = (" " * (sessionNameLength - snl))
    if is_attached(s) == "detached":
      print color_text('blue', str(ind+1)) + ': ' + sessName + spaces + " (" + color_text('green', str(ind+1)) + ":attach" + ")" + renameText(col, ind+1) + killText(col, ind+1)
    elif is_attached(s) == "script":
      print color_text('blue', str(ind+1)) + ': ' + sessName + spaces + " (" + color_text('blue', str(ind+1)) + ":start" +  ")"

def prSessionAttached(col, sessions, sessionNameLength, maxSessionNameLength, sessionName):
  print "- " + col.OKBLUE + "in session " + col.OKGREEN + sessionName + col.ENDC
  print ''
  for ind, s in enumerate(sessions):
    sessName = truncateSessionName(getName(s), maxSessionNameLength)
    snl = getLenOfSessionName(s)
    spaces = (" " * (sessionNameLength - snl))
    if is_attached(s) == "detached":
      print col.OKBLUE + str(ind+1) + col.ENDC + ': ' + sessName + spaces + " (" + col.WARNING + "Detached" + col.ENDC + ") " + renameText(col, ind+1) + killText(col, ind+1)
    elif is_attached(s) == "attached":
        print col.OKBLUE + str(ind+1) + col.ENDC + ': ' + col.OKGREEN + sessName + col.ENDC + spaces + detachText(col, ind+1) + renameText(col, ind+1) + killText(col, ind+1)
    elif is_attached(s) == "script":
      print col.OKBLUE + str(ind+1) + col.ENDC + ': ' + sessName

def printInSessionOptions(col):
  print col.OKBLUE + 'q' + col.ENDC + ':' + ' Quit'
  print col.OKBLUE + 'n' + col.ENDC + ':' + ' New Tmux Session'
  print col.OKBLUE + 's' + col.ENDC + ':' + ' Switch Pane'
  print col.OKBLUE + 'vs' + col.ENDC + ':' + ' Vertical Split' + " | " + col.OKBLUE + 'hs' + col.ENDC + ':' + ' Horizontal Split'
  # print col.FAIL + 'ka' + col.ENDC + ':' + ' Kill All Tmux Sessions'

def printDefaultOptions(col, sessions):
  print col.OKBLUE + 'q' + col.ENDC + ':' + ' Quit'
  print col.OKBLUE + 'n' + col.ENDC + ':' + ' New Tmux Session'
  print col.OKBLUE + 'vs' + col.ENDC + ':' + ' Vertical Split' + " | " + col.OKBLUE + 'hs' + col.ENDC + ':' + ' Horizontal Split'
  if a_session_is_alive(sessions):
    print col.FAIL + 'ka' + col.ENDC + ':' + ' Kill All Sessions'

def printSessionInformation(col, sessions):
  if a_session_is_alive(sessions): 
    return
  else:
    print "- " + col.OKBLUE + "No current active sessions" + col.ENDC

def prScripts(scripts, sessions, userInSession, col):
  if userInSession:
    printInSessionOptions(col)
  else:
    printDefaultOptions(col, sessions)
  print ''
  printSessionInformation(col, sessions)
  # Continue printing rest of program
  attachedSession = False
  activeSession = False
  # Max Length of Session Name in Column
  maxSessionNameLength = 22
  sessionNameLength = 0
  # Get Session Name Length for columns and Check if a session is attached
  for s in sessions:
    snl = getLenOfSessionName(s)
    if snl > sessionNameLength:
      sessionNameLength = snl if snl <= maxSessionNameLength else maxSessionNameLength
    if is_attached(s) == "attached":
      attachedSession = True
      attachedSessionName = getName(s)
    elif is_attached(s) == "detached":
     activeSession = True 
  # Print functions 
  if( attachedSession ):
    prSessionAttached(col, sessions, sessionNameLength, maxSessionNameLength, attachedSessionName)
  elif( activeSession ):
    prNoneAttached(col, sessions, sessionNameLength, maxSessionNameLength)
  else:
    prNoneActive(col, scripts)
  # Print padding
  print ''

def handleInput(scriptDir, sessions, scripts):
  session = raw_input("/[o_o]\ --What would you like to do?\n\n> ")
  if session == "0" or session == "q" or session == "quit":
    writeReboundScript(False)
    print 'Exiting'
    print ''
  elif stlowrmsp(session) == "hs":
    writeReboundScript(False)
    start_session_horizontal_split()
  elif stlowrmsp(session) == "vs":
    writeReboundScript(False)
    start_session_vertical_split()
  elif stlowrmsp(session) == "n":
    writeReboundScript(False)
    startSession()
  elif stlowrmsp(session) == "ka" or stlowrmsp(session[0]) == "kall" or stlowrmsp(session[0]) == "killall":
    writeReboundScript(False)
    killAllSessions()
    main()
  elif stlowrmsp(session[0]) == "k" and re.findall(r'\d+', stlowrmsp(session)) != []:
    writeReboundScript(False)
    killSession(sessions, returnSessionNumber(stlowrmsp(session)))
    main()
  elif stlowrmsp(session[0]) == "d" and re.findall(r'\d+', stlowrmsp(session)) != []:
    writeReboundScript(False)
    detachSession(sessions, returnSessionNumber(stlowrmsp(session)))
    main()
  elif stlowrmsp(session[0]) == "r" and re.findall(r'\d+', stlowrmsp(session)) != []:
    writeReboundScript(False)
    renameSession(sessions, returnSessionNumber(stlowrmsp(session)))
    main()
  elif session.isdigit() and int(session)-1 < len(sessions):
    writeReboundScript(False)
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
  session = raw_input("/[O~O]\ --What would you like to do?\n\n> ")
  if session == "0" or session == "q" or session == "quit":
    writeReboundScript(False)
    print 'Exiting'
    print ''
  elif stlowrmsp(session) == "hs":
    horizontally_split_window()
  elif stlowrmsp(session) == "vs":
    vertically_split_window()
  elif stlowrmsp(session) == "n":
    prHeader()
    sessionName = raw_input("/[O~O]\ --Session Name: ")
    writeReboundScript(False)
    # writeReboundScript("tmux attach-session -t \"" + sessionName.strip() + "\"")
    subprocess.call(["tmux", "new", "-d", "-s", sessionName.strip()])
    #subprocess.call(["tmux", "detach", "-s", activeSessName])
    main()
  elif stlowrmsp(session) == "s":
    writeReboundScript(False)
    switch_pane()
  elif stlowrmsp(session[0]) == "ka" or stlowrmsp(session[0]) == "kall" or stlowrmsp(session[0]) == "killall":
    writeReboundScript(False)
    killAllSessions()
    main()
  elif stlowrmsp(session[0]) == "k" and re.findall(r'\d+', stlowrmsp(session)) != []:
    writeReboundScript(False)
    killSession(sessions, returnSessionNumber(stlowrmsp(session)))
    main()
  elif stlowrmsp(session[0]) == "r" and re.findall(r'\d+', stlowrmsp(session)) != []:
    writeReboundScript(False)
    renameSession(sessions, returnSessionNumber(stlowrmsp(session)))
    main()
  elif stlowrmsp(session[0]) == "d" and re.findall(r'\d+', stlowrmsp(session)) != []:
    writeReboundScript(False)
    detachSession(sessions, returnSessionNumber(stlowrmsp(session)))
    main()
  elif stlowrmsp(session[0]) == "d" or stlowrmsp(session.split(' ')[0]) == "detach":
    writeReboundScript(False)
    subprocess.call(["tmux", "detach", "-s", activeSessName])
  # elif session.isdigit() and int(session)-1 < len(sessions):
  #   switchToSession(int(session), activeSessName, sessions)
  else:
    print '' 
    print "...You are Currently in a Session"
    print '' 
    handleActiveSession(activeSessName, sessions)

def warnUserThatTmuxIsNotInstaled():
  subprocess.call(['clear'])
  print ""
  print "--- You must install tmux in order to use Tmux Session Manager --- \n" 
  print "To install for Mac use: 'sudo brew install tmux'"
  print "To install for ubuntu use: 'sudo apt-get install tmux'"
  print ""
  print "------------------------------------------------------------------- \n" 

# start
main()
