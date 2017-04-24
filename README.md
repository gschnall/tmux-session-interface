## Table of contents
=================
  * [Description](#description)
  * [Installation](#installation)
  * [Usage](#usage)

## Description
A python wrapper for tmux. It provides users with  a terminal interface that makes working with multiple sessions simpler. Users can easily start, detach, kill, or switch sessions.

## Installation
- Clone this repository into your home directory
- In your bashrc include this: alias tsm='python ~/.tmux-scripts/session-manager.py'
  - Be sure you are using python 2
  - tsm stands for Tmux Session Manager
- restart your terminal application
- Start the program by typing 'tsm' followed by enter into your terminal
- Note: will be available via pip soon...

## Usage
- Start a new session by typing n, provide a name for the session or hit enter to leave it blank.
- Type 'd' to detach from your current session
- Type the associated number of a session to
- Use 'vs' and 'hs' to split the screen vertically or horizontally
  - If you aren't already in a session, this will automatically start one for you
- Type 'q' to quit
