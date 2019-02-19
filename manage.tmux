#!/usr/bin/env bash

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

set_key_bindings() {
  tmux bind-key C-m run-shell "python $CURRENT_DIR/session-manager.py"
}

main() {
 set_key_bindings
}
main
