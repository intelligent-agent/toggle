#!/bin/bash
SCRIPT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
STYLE=$1
SOURCE="$SCRIPT/$1"
DEST=$(realpath "$2/$1")

function usage {
  echo "convert.sh <style name> <dest dir>"
}

icons=( temperature arrow arrow_disabled cancel cancel_disabled \
heater_heating heater_hot heater_cold \
heater_bed_heating heater_bed_hot heater_bed_cold \
jog pause pause_disabled play \
play_disabled print home settings network  slicer wifi printer \
0.1 0.1_disabled 1 1_disabled 10 10_disabled 100 100_disabled loading e h z \
motor_off fan_on fan_off )
small_icons=( heartbeat connection connection_disabled running paused pointer)


function clean {
    rm -f $DEST/*.png
}

function convert_images {
    size=128
	for f in "${icons[@]}"
	do
		echo "Convert $f"
		convert  -background none -resize $sizex$size $SOURCE/$f.svg $DEST/$f\_$size.png
	done

    size=64
	for f in "${small_icons[@]}"
	do
		echo "Converting $f.svg"
		convert -background none -resize $sizex$size $SOURCE/$f.svg $DEST/$f\_$size.png
	done

  sizes=( 400 600 900 )
  for size in "${sizes[@]}"
  do
    echo "Convert logo $size"
	  convert -resize $sizex$size $SOURCE/logo.svg $DEST/logo_$size.png
  done
}


echo "Re-creating style"
echo "Generating from ${SOURCE} to ${DEST}"
#clean
convert_images
