## Table of contents
=================
  * [Description](#description)
  * [Installation](#installation)
  * [Usage](#usage)

## Description
A python wrapper for tmux. It provides users with  a terminal interface that makes working with multiple sessions simpler. Users can easily start, detach, kill, or switch sessions.

![Alt text](./screen_shots/screen_shot_1.png?raw=true "Screen Shot 1")

## Installation
- Clone this repository into your home directory
  - git clone git@github.com:gschnall/tmux-session-manager.git
- In your bashrc include this: alias tsm='python ~/.tmux-scripts/session-manager.py'
  - Be sure you are using python 2
- restart your terminal application
- Start the program by typing 'tsm' and hitting enter
- Note: This will be available via pip soon.

## Basic Usage
- Start a new session by typing 'n', provide a name for the session or hit enter to leave it blank.
- Use 'vs' and 'hs' to split the screen vertically or horizontally
  - If you aren't already in a session, this will automatically start one for you
- Type 'd' to detach from your current session
- Type the prefix k and the associated number of your session to kill it ('k1' for example)
- Type 'ka' to kill all sessions
- Type 'q' to quit at any time
- Though not very useful, you can type 's' to see the pane numbers and switch to a specific pane. It might be useful if you have a complex pane setup.

![Alt text](./screen_shots/screen_shot_2.png?raw=true "Screen Shot 2")

## Advanced Usage
- You can also use Tmux-Session-Manager to display and start your own custom tmux scripts.
- Create a bash script that sets up a tmux session and place it in the session-scripts directory
- Example scripts can be found in the example-script-directory
