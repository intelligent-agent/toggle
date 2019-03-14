#!/bin/bash


DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

icons=( temperature arrow arrow_disabled cancel cancel_disabled \
heater_heating heater_hot heater_cold \
heater_bed_heating heater_bed_hot heater_bed_cold \
jog pause pause_disabled play \
play_disabled print home settings network  slicer wifi 
0.1 0.1_disabled 1 1_disabled 10 10_disabled 100 100_disabled loading e h z \
motor_off fan_on fan_off )
small_icons=( heartbeat connection connection_disabled running paused pointer)

function clean {
    rm $DIR/*.png
}

function images {
    size=128
	for f in "${icons[@]}"
	do
		echo "Convert $f"
		convert  -background none -resize $sizex$size $DIR/svg/$f.svg $DIR/$f\_$size.png
	done

    size=64
	for f in "${small_icons[@]}"
	do
		echo "Convert $f"
		convert -background none -resize $sizex$size $DIR/svg/$f.svg $DIR/$f\_$size.png
	done

    size=600
	echo "Convert logo"
	convert -resize $sizex$size $DIR/svg/logo.svg $DIR/logo_$size.png
}

clean
images
