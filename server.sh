#!/usr/bin/env bash

# This script is used for launching server and configuration scripts from Admin/ directory.
# See Admin/help or README.md for further details.

#   * no args - start
#   * start
#   * config
#   * help
#   * backup - run backup
#       - set
#       - retrieve
#   * help

if [ "$#" = 0 ]; then
    bash Admin/Start.sh
fi