#!/bin/bash
# This scipt grabs SVG icons from an Inkscape template and
# converts the files to PNG icons for use in Toggle.

icons=( temperature arrow arrow_disabled cancel cancel_disabled \
heater_heating heater_hot heater_cold \
heater_bed_heating heater_bed_hot heater_bed_cold \
jog pause pause_disabled play \
play_disabled print home settings network  slicer wifi printer \
0.1 0.1_disabled 1 1_disabled 10 10_disabled 100 100_disabled loading e h z \
motor_off fan_on fan_off )
small_icons=( heartbeat connection connection_disabled running paused pointer)
colors=( background-color-side default-text-color plate-color model-color stage-color \
menu-header-color menu-header-text-color menu-body-text-color menu-body-color menu-header-color \
splash-text-color progress-bar-color)

function clean {
    rm -f $DEST/*.png
}

function export_image {
		echo "Exporting $f"
		inkscape $SOURCE/template.svg --export-id=$f  --export-filename=$DEST/$f\_$size.png -j 1>/dev/null
}

function create_images {
	size=128
	for f in "${icons[@]}"
	do
		export_image
	done

	size=64
	for f in "${small_icons[@]}"
	do
		export_image
	done

  f=logo
	sizes=( 400 600 900 )
	for size in "${sizes[@]}"
	do
	  export_image
	  echo $size
      inkscape $SOURCE/template.svg -w ${size} -h ${size} --export-id=$f  --export-filename=$DEST/$f\_$size.png -j 1>/dev/null
	done
}

function get_colors {
	i=0
	size=10
	for replace in "${colors[@]}"
	do
		f=$replace
		export_image
		replacement_colors[$i]=$(convert $DEST/$replace\_$size.png -crop '1x1+1+1' txt:- | tail -n1 | awk -F "#" '{print substr($NF, 0, 6)}')
		rm -f $DEST/$replace\_$size.png
	  i=$(($i+1))
	done
}

function convert_ui {
	ui_files=( ui_800x480.json ui_1280x720.json ui_1920x1080.json)
	for FILE in "${ui_files[@]}"
	do
	  echo "Converting $FILE"
		cp "$SCRIPT/templates/$FILE" $DEST
    i=0
		for tag in "${colors[@]}"
		do
			color="${replacement_colors[$i]}"
			echo "Replacing $tag with #$color in file $DEST/$FILE"
			sed -i "s/$tag/\#$color/g" $DEST/$FILE
			i=$(($i+1))
		done
	done
	cp "$SCRIPT/templates/style.css" $DEST
}


function usage {
  echo "generate_style.sh <style name>"
  echo "where style name: Plain, Dark, Mixer, Spitzy, Black"
  echo "--ui generate ui layout files"
  echo "--png generate PNG files from the SVG template"
}

if [ "x$1" == "x" ]; then
	usage
	exit 1
fi

SCRIPT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
STYLE=$1
SOURCE="$SCRIPT/$1"
DEST=$(realpath "$SCRIPT/../../styles/$1")


echo "Re-create ui and PNGs"
echo "Generating from ${SOURCE} to ${DEST}"

shift

while test $# -gt 0
do
    case "$1" in
        --ui) get_colors; convert_ui
            ;;
        --png) create_images
            ;;
        --*) echo "bad option $1"; usage
            ;;
        *) echo "argument $1"
            ;;
    esac
    shift
done
