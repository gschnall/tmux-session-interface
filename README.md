## Table of contents
 [Description](#description)
 [Installation](#installation)
 [Usage](#usage)

## Description
Provides a terminal interface that makes manage sessions easy. You can create, switch, detach, kill, or rename sessions with a few keystrokes.

![Alt text](./screen_shots/screen_shot_1.png?raw=true "Screen Shot 1")

## Installation
#### 1. Run the following line in your terminal:
   ```bash 
   git clone git@github.com:gschnall/tmux-session-manager.git ~/.tmux-session-manager
   ```
#### 2. Place this in your bashrc or bashprofile:
    ```bash
    alias ms='python ~/.tmux-session-manager/session-manager.py
    ```
#### 3. Place this in your tmux.config 
    ```bash
    # Session Manager
    run-shell ~/.tmux-session-manager/manage.tmux
    ```
***Note***: the configs are typically created at `~/.tmux.conf` and `~/.bashr`

## Usage
#### From the command line:
`> ms`
***Note***: If a session is attached, you can't run this command outside of that session

#### While in a Tmux Session:
`Ctrl-b Ctrl-m`
or, if you use `Ctrl-a`
`Ctrl-a Ctrl-m`

![Alt text](./screen_shots/screen_shot_2.png?raw=true "Screen Shot 2")

## \\[o-o]/ - - Rad Stuff
