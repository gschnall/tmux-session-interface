#!/usr/bin/env python2
import subprocess
import sys
import tmux_session_manager

def init():
  try:
    subprocess.call(["tmux", "kill-window", "-t", "TmUx-SessIoN-MaNaGer__"])
  except OSError as e:
    error = e

  if tmux_session_is_active():
    scriptCmd = "python2 " + sys.path[0] + "/start_session_manager.py"
    subprocess.call(["tmux", "new-window","-d", "-n", "TmUx-SessIoN-MaNaGer__"])
    subprocess.call(["tmux", "send-keys", "-t", "TmUx-SessIoN-MaNaGer__", "python2 " + sys.path[0] + "/start_session_manager.py", "ENTER"])
    # subprocess.call(["tmux", "send-keys", "-t", "TmUx-SessIoN-MaNaGer__", scriptCmd + "; tmux wait-for -S" + scriptCmd, "ENTER", "wait-for", scriptCmd])
    # subprocess.call(["tmux", "send-keys", "-t", "TmUx-SessIoN-MaNaGer__", "select-window -t TmUx-SessIoN-MaNaGer__"])
    subprocess.call(["tmux", "select-window", "-t", "TmUx-SessIoN-MaNaGer__"])
  else:
    tmux_session_manager.main()

def tmux_session_is_active():
  currentSessions = tmux_session_manager.getSessions()
  return currentSessions[0]

init();
