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

    size=400
	echo "Convert logo 400"
	convert -resize $sizex$size $DIR/svg/logo.svg $DIR/logo_$size.png
    size=600
	echo "Convert logo 600"
	convert -resize $sizex$size $DIR/svg/logo.svg $DIR/logo_$size.png
    size=900
	echo "Convert logo 900"
	convert -resize $sizex$size $DIR/svg/logo.svg $DIR/logo_$size.png
}

function convert_ui {
  ui_files=( ui_800x480.json ui_1280x720.json ui_1920x1080.json)
  for FILE in "${ui_files[@]}"
	do
		echo "Convert $FILE"
    cp "$DIR/../Plain/$FILE" $DIR
    # Background color
  	sed -i 's/#FFF/#63C7AF/g' $DIR/$FILE
    # Menu headers etc.
  	sed -i 's/#c9c3c3/#26322f/g' $DIR/$FILE
    # Scroll pane
  	sed -i 's/#EEE/#63C7AF/g' $DIR/$FILE
    # Plate color
    sed -i 's/#DDD/#a8caba/g' $DIR/$FILE
	done
}

#clean
#images
convert_ui
