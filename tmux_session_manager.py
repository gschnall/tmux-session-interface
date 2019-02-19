#!/usr/bin/env python2
import subprocess
import os
import sys
import readline
import glob
import re
import time
import atexit

# print os.path.realpath(__file__) # file path
# os.path.expanduser("~") # home dir

def main(error=""):

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
  # Register exit event
  if (len(atexit._exithandlers) == 0):
    atexit.register(onexit, userInSession)
  # Display any warnings/errors
  if error != "":
    prError(error)
  # handle user input
  if userInSession:
    handleActiveSession(currentSessions[2], sessions)
  else:
    handleInput(scriptDir, sessions, scripts)

  # subprocess.call(["sh", scriptDir+"/rebound-scripts/rebound.sh"])

def onexit(userInSession):
  if userInSession:
    subprocess.call(["tmux", "kill-window", "-t", "TmUx-SessIoN-MaNaGer__"])
  else:
    subprocess.call(['clear'])

# ::PRINTING FUNCTIONS
def prHeader():
  subprocess.call(['clear'])
  print getHeader()

def getHeader():
  class col:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
  return (
    '\n' +
    col.OKGREEN + '|:::::|::::|:::|:::::::::::::::::::|' + col.ENDC + '\n' +
    col.OKBLUE  + '|--  -|-  -|-  |-- |--  --  -- -- -|' + col.ENDC + '\n' + 
    col.BOLD    + '|---| Tmux-Session-Manager \[O-O]/ |' + col.ENDC + '\n' + 
    col.OKBLUE  + '|--  -|-  -|-  |-- |--  --  -- ----|' + col.ENDC + '\n' + 
    col.OKGREEN + '|:::::|::::|:::|:::::::::::::::::::|' + col.ENDC + '\n'
  )

def prError(err):
  print color_text("red", "!") + " " + color_text("yellow", err) + "\n"

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
    "underline": '\033[4m',
    "red":'\033[91m',
    "white": '\33[37m',
    "selected": '\33[7m',
    "greenbg": '\33[42m',
    "grey": '\33[90m',
    "offwhite": '\33[97m'
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

def validSessionName(n):
  return n != "" and not (re.search('\.', n) > -1) and not (re.search('\:', n) > -1)

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
  return col.FAIL + "k" + str(n) + col.ENDC + ":kill"

def renameText(col, n):
  return col.WARNING + "r" + str(n) + col.ENDC + ":rename"

def detachText(col, n):
  return col.WARNING + "d" + col.ENDC + ":detach"
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

def startSession():
  prHeader()
  sessionName = raw_input("\[O~O]/ --Session Name: ")
  subprocess.call(["tmux", "new", "-s", sessionName.strip()])

def killAllSessions():
  prHeader()
  prError("Every session will be destroyed")
  response = raw_input("\[ToT]/ --You really want to " + color_text("red", "Kill") + " " + color_text("underline", "ALL") + " Sessions? \n\n(y or n) > ")
  if stlowrmsp(response) == "y" or stlowrmsp(response) == "yes":
    subprocess.call(["killall", "tmux"])
  else:
    main()

def killSession(sessions, sessNumb):
  if( sessions[sessNumb-1] > -1 ):
    subprocess.call(["tmux", "kill-session", "-t", getName(sessions[sessNumb-1])])
  else:
    main("Session number not found")

def createNewSession():
  # - Get Session Name 
  sessionName = ""
  while (not validSessionName(sessionName.strip())):
    prHeader()
    if sessionName != "":
      prError("Names cannot contain colons or periods")
    sessionName = raw_input("/[O~O]\ --Session Name: ")
  # - Get Session Directory
  directoryPath = ""
  while (directoryPath == "" or not os.path.isdir(directoryPath)):
    prHeader()
    print "- Session Name: " + color_text("blue", sessionName.strip()) + "\n" 
    print color_text("underline", "Use tab completion") + "  " + color_text("underline", "Hit ENTER to select your directory") 

    if directoryPath != "":
      prError("You must select a Directory (not a file)")

    completer = tabCompleter()

    readline.set_completer_delims('\t')
    readline.parse_and_bind("tab: complete")
    readline.set_startup_hook(lambda: readline.insert_text(os.path.expanduser('~/'))) 
    readline.set_completer(completer.pathCompleter)
    
    directoryPath = raw_input("\n" + "[O~O]/ --Directory: ")
  # - Reset Readline and Create New Session 
  readline.set_startup_hook(lambda: readline.insert_text(''))
  subprocess.call(["tmux", "new", "-d", "-s", sessionName.strip(), "-c", directoryPath])

def renameSession(sessions, sessNumb):
  if( sessions[sessNumb-1] > -1 ):
    sessionName = getName(sessions[sessNumb-1])
    # - Get Session Name 
    newSessionName = ""
    while (not validSessionName(newSessionName.strip())):
      prHeader()
      if newSessionName != "":
        prError("Names cannot contain colons or periods") 
      newSessionName = raw_input("\[O~O]/ --Rename " + color_text("blue", sessionName) + " to: \n\n> ")
    subprocess.call(["tmux", "rename-session", "-t", sessionName, newSessionName])
  else:
    main("Session number not found")

def detachSession(sessions, sessNumb):
  if( sessions[sessNumb-1] > -1 ):
    sessionName = getName(sessions[sessNumb-1])
    subprocess.call(["tmux", "detach", "-s", sessionName])
  else:
    main("Session number not found")

def switchSessionTo(sessName):
  subprocess.call(["tmux", "switch-client", "-t", sessName + ":"])

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

def printAsColumn(text, delimiter): 
  p1 = subprocess.Popen(["echo", text], stdout=subprocess.PIPE)
  p2 = subprocess.Popen(["column", "-s", delimiter, "-t"], stdin=p1.stdout)
  p2.communicate()

def prNoneActive(col, scripts):
  for script in scripts:
    print col.OKBLUE + str(scripts.index(script)+1) + col.ENDC + ': ' + script.split('.')[0] + " (" + col.OKBLUE + str(scripts.index(script)+1) + col.ENDC + ":start" +  ")"

def prNoneAttached(col, sessions, sessionNameLength, maxSessionNameLength):
  printText = "";

  for ind, s in enumerate(sessions):
    sessName = truncateSessionName(getName(s), maxSessionNameLength)
    snl = getLenOfSessionName(s)
    spaces = (" " * (sessionNameLength - snl))
    if is_attached(s) == "detached":
      printText += color_text('blue', str(ind+1)) + ':' + sessName + "|" + color_text('green', str(ind+1)) + ":attach" + "|" + renameText(col, ind+1) + "|" + killText(col, ind+1) + "\n"
    elif is_attached(s) == "script":
      printText += color_text('blue', str(ind+1)) + ':' + sessName + "|" + color_text('blue', str(ind+1)) + ":start" +  "\n"
  printAsColumn(printText, "|")

def prSessionAttached(col, sessions, sessionNameLength, maxSessionNameLength, sessionName):
  print "in " + col.OKGREEN + sessionName + col.ENDC
  print ''
  printText = ""

  for ind, s in enumerate(sessions):
    sessName = truncateSessionName(getName(s), maxSessionNameLength)
    snl = getLenOfSessionName(s)
    spaces = (" " * (sessionNameLength - snl))
    if is_attached(s) == "detached":
      printText += color_text("blue", str(ind+1)) + '.' + "|" + color_text("white", sessName) + "|" + color_text('green', str(ind+1)) + ":switch" + "|" + renameText(col, ind+1) + "|" + killText(col, ind+1) + "\n"
    elif is_attached(s) == "attached":
      printText += color_text("blue", str(ind+1)) + '.' + "|" + color_text("green", sessName) + "|" + detachText(col, ind+1) + "|" + renameText(col, ind+1) + "|" + killText(col, ind+1) + "\n"
    elif is_attached(s) == "script":
      printText += ccolor_text("blue", str(ind+1)) + '.' + "|" + sessName + "\n"
  printAsColumn(printText, "|")

def printInSessionOptions(col):
  print col.OKBLUE + 'q' + col.ENDC + ':' + '  Quit'
  print col.OKBLUE + 'n' + col.ENDC + ':' + '  New Tmux Session'
  print col.OKBLUE + 'c' + col.ENDC + ':' + '  View Cheat Sheet'
  print col.FAIL + 'ka' + col.ENDC + ':' + ' Kill All Sessions'
  # print col.OKBLUE + 's' + col.ENDC + ':' + ' Switch Pane'
  # print col.OKBLUE + 'vs' + col.ENDC + ':' + ' Vertical Split' + " | " + col.OKBLUE + 'hs' + col.ENDC + ':' + ' Horizontal Split'

def printDefaultOptions(col, sessions):
  print col.OKBLUE + 'q' + col.ENDC + ':' + '  Quit'
  print col.OKBLUE + 'n' + col.ENDC + ':' + '  New Tmux Session'
  print col.OKBLUE + 'c' + col.ENDC + ':' + '  View Cheat Sheet'
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
    print 'Exiting'
    print ''
  elif stlowrmsp(session) == "c" or stlowrmsp(session) == "cs" or stlowrmsp(session) == "cheat":
    subprocess.call(['less', sys.path[0] + "/resources/cheat_sheet.txt"])
    main()
  elif stlowrmsp(session) == "hs":
    start_session_horizontal_split()
  elif stlowrmsp(session) == "vs":
    start_session_vertical_split()
  elif stlowrmsp(session) == "n" or stlowrmsp(session) == "new":
    createNewSession()
    main()
  elif stlowrmsp(session) == "ka" or stlowrmsp(session) == "kall" or stlowrmsp(session) == "killall":
    killAllSessions()
    main()
  elif stlowrmsp(session[0]) == "k" and re.findall(r'\d+', stlowrmsp(session)) != []:
    killSession(sessions, returnSessionNumber(stlowrmsp(session)))
    main()
  elif stlowrmsp(session[0]) == "d" and re.findall(r'\d+', stlowrmsp(session)) != []:
    detachSession(sessions, returnSessionNumber(stlowrmsp(session)))
    main()
  elif stlowrmsp(session[0]) == "r" and re.findall(r'\d+', stlowrmsp(session)) != []:
    renameSession(sessions, returnSessionNumber(stlowrmsp(session)))
    main()
  elif session.isdigit() and int(session)-1 < len(sessions):
    selectAction(int(session), sessions, scripts, scriptDir)
  else:
    main("Input option not recognized")

def handleActiveSession(activeSessName, sessions):
  session = raw_input("/[O~O]\ --What would you like to do?\n\n> ")
  if session == "0" or session == "q" or session == "quit":
    print 'Exiting'
    print ''
  elif stlowrmsp(session) == "c" or stlowrmsp(session) == "cs" or stlowrmsp(session) == "cheat":
    subprocess.call(['less', sys.path[0] + "/resources/cheat_sheet.txt"])
    main()
  elif stlowrmsp(session) == "n" or stlowrmsp(session) == "new":
    createNewSession()
    main()
  # elif stlowrmsp(session) == "s":
  #   switch_pane()
  elif stlowrmsp(session) == "ka" or stlowrmsp(session) == "kall" or stlowrmsp(session) == "killall":
    killAllSessions()
  elif stlowrmsp(session[0]) == "k" and re.findall(r'\d+', stlowrmsp(session)) != []:
    killSession(sessions, returnSessionNumber(stlowrmsp(session)))
    main()
  elif stlowrmsp(session[0]) == "r" and re.findall(r'\d+', stlowrmsp(session)) != []:
    renameSession(sessions, returnSessionNumber(stlowrmsp(session)))
    main()
  elif stlowrmsp(session[0]) == "d" and re.findall(r'\d+', stlowrmsp(session)) != []:
    detachSession(sessions, returnSessionNumber(stlowrmsp(session)))
    main()
  elif stlowrmsp(session[0]) == "d" or stlowrmsp(session.split(' ')[0]) == "detach":
    subprocess.call(["tmux", "detach", "-s", activeSessName])
  elif session.isdigit() and int(session)-1 < len(sessions):
    switchSessionTo(getName(sessions[int(session)-1]))
  else:
    main("Input option not recognized")
    # handleActiveSession(activeSessName, sessions)

def warnUserThatTmuxIsNotInstaled():
  subprocess.call(['clear'])
  print ""
  print "--- You must install tmux in order to use Tmux Session Manager --- \n" 
  print "To install for Mac use: 'sudo brew install tmux'"
  print "To install for ubuntu use: 'sudo apt-get install tmux'"
  print ""
  print "------------------------------------------------------------------- \n" 
  time.sleep(3000)

class tabCompleter(object):
  """ 
  A tab completer that can either complete from
  the filesystem or from a list.
  """

  def pathCompleter(self, text, state):
    """ 
    This is the tab completer for systems paths.
    Only tested on *nix systems
    """
    line = readline.get_line_buffer().split()
    
    # replace ~ with the user's home dir. See https://docs.python.org/2/library/os.path.html
    if '~' in text:
      text = os.path.expanduser('~')

    # autocomplete directories with having a trailing slash
    if os.path.isdir(text):
      text += '/'

    return [x for x in glob.glob(text + '*')][state]

  def createListCompleter(self,ll):
    """ 
    This is a closure that creates a method that autocompletes from
    the given list.
    
    Since the autocomplete function can't be given a list to complete from
    a closure is used to create the listCompleter function with a list to complete
    from.
    """
    def listCompleter(text,state):
        line   = readline.get_line_buffer()

        if not line:
            return [c + " " for c in ll][state]

        else:
            return [c + " " for c in ll if c.startswith(line)][state]

    self.listCompleter = listCompleter

# start
# main()
