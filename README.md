## Table of contents
=================
  * [Description](#description)
  * [Installation](#installation)
  * [Usage](#usage)

## Description
A simple python wrapper for tmux. It provides users with a terminal interface that makes it easy to manage multiple sessions. Start, detach, kill, or rename sessions with a few keystrokes.

![Alt text](./screen_shots/screen_shot_1.png?raw=true "Screen Shot 1")

## Installation
1. Run the following line your terminal:
   git clone git@github.com:gschnall/tmux-session-manager.git ~/.tmux-session-manager`
2. In your bashrc include the following line:
   alias ts='python ~/.tmux-session-manager/session-manager.py'
3. Be sure that it's being run with python 2
4. Restart your terminal application or source your bashrc 
5. Start the program by typing 'ts' and hitting enter

## Usage
- Start a new session by typing 'n', provide a name for the session or hit enter to leave it blank.
- Use 'vs' and 'hs' to split the screen vertically or horizontally
  - If you aren't already in a session, this will automatically start one for you
- Type 'd' to detach from your current session or 'k' to kill it
- Type the prefix k and the associated session number to kill it   ( for example: 'k1')
- Type the prefix d and the associated session number to detach it ( for example: 'd1')
- Type the prefix r and the associated session number to rename it ( for example: 'r1')
- Type the prefix a and the associated session number to attach it ( for example: 'a1')
- Type 'ka' to kill all sessions (Note: for your own safety, 'ka' will only work outside of a session)
- Type 'q' to quit at any time
- It's a pretty useless feature but you can type 's' to see the pane numbers and switch to a specific pane

![Alt text](./screen_shots/screen_shot_2.png?raw=true "Screen Shot 2")
