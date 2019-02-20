#!/usr/bin/env python2
import subprocess
import sys
import re
import tmux_session_manager

def init():
  title = "TmUx-SessIoN-MaNaGer__"

  if tmux_session_is_active():
    clearRemnants(title)
    scriptCmd = "python2 " + sys.path[0] + "/start_session_manager.py"
    subprocess.call(["tmux", "new-window","-d", "-n", title])
    subprocess.call(["tmux", "send-keys", "-t", title, "python2 " + sys.path[0] + "/start_session_manager.py", "ENTER"])
    subprocess.call(["tmux", "select-window", "-t", title])
  else:
    tmux_session_manager.main()

def tmux_session_is_active():
  currentSessions = tmux_session_manager.getSessions()
  return currentSessions[0]

def clearRemnants(sessionName):
  tmuxls = subprocess.Popen(["tmux","list-windows"], stdout=subprocess.PIPE)
  tls = tmuxls.communicate()
  tlsArr = map(str,tls)
  windowArr = tlsArr[0].strip().split(':')

  for window in windowArr:
    if re.search(sessionName, window) > -1:
      try:
        subprocess.call(["tmux", "kill-window", "-t", sessionName])
      except OSError as e:
        pass 
      break

init();
