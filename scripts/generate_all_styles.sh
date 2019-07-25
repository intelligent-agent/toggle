#!/bin/bash
# Convert all svg files into PNGs
SCRIPT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
$SCRIPT/styles/generate_style.sh Dark --ui --png
$SCRIPT/styles/generate_style.sh Mixer --ui --png
$SCRIPT/styles/generate_style.sh Spitzy --ui --png
$SCRIPT/styles/generate_style.sh Plain --ui --png