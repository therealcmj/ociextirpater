#!/bin/bash

# Variables
EXT_DIR=/usr/local/ociextirpater
VENV=$EXT_DIR/.venv
CURRENT_DT=$(date +%Y-%m-%d)

git -C $EXT_DIR pull origin main
$VENV/bin/python $EXT_DIR/ociextirpate.py -ip -force -c $1 \
-skip_delete_compartment -log $2/$CURRENT_DT.log
