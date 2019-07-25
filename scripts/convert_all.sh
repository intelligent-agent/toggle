#!/bin/bash
# Convert all svg files into PNGs

./styles/grab.sh Dark ../styles
./styles/grab.sh Mixer ../styles
./styles/grab.sh Spitzy ../styles
./styles/grab.sh Plain ../styles

# Some styles have not yet been converted to the new setup
./styles/convert.sh Mixer ../styles
