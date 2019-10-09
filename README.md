## Table of contents
- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)

## Description
Provides a terminal interface that makes managing sessions easy. You can create, switch to, detach, kill, or rename sessions with a few keystrokes. 

- ***If you're a Tmux noob***, this will act as a cheat code for instant tmux productivity 🕹️  
- ***If you're a Tmux ninja***, this will add another deadly weapon to your agile arsenal  ⚔️  

![Alt text](./screen_shots/screen_shot_1.png?raw=true "Screen Shot 1")

## Installation
#### 1. Run the following line in your terminal
```bash 
git clone git@github.com:gschnall/tmux-session-interface.git ~/.tmux-session-interface
```
#### 2. Place this in your bashrc or bashprofile
```bash
alias ms='python ~/.tmux-session-interface/session-manager.py'
```
#### 3. Place this in your tmux.config 
```
run-shell ~/.tmux-session-interface/manage.tmux
```
***Note***: the configs are typically created at `~/.tmux.conf` and `~/.bashrc`

## Usage
#### From the command line:
`> ms`

***Note***: if a session is attached, you can't run this command outside of that session 

#### While in a Tmux Session
`Ctrl-b Ctrl-m`
or, if you use Ctrl-a,
`Ctrl-a Ctrl-m`

![Alt text](./screen_shots/screen_shot_2.png?raw=true "Screen Shot 2")

## \\[o~o]/ -- Rad Stuff
