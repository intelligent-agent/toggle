#!/bin/bash


DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

icons=( temperature arrow cancel heat jog pause play print travel home settings network )
small_icons=( heartbeat connection connection_disabled play pause)


icon_enabled=110950FF
icon_disabled=11095080

small_icon_enabled=C5FFF1FF

function clean {
    rm *.png

}

function images {
    size=128
	for f in "${icons[@]}"
	do
		echo "Convert $f to #$icon_enabled"
		convert  -fuzz 60% -background none -fill "#$icon_enabled" -opaque black -resize $sizex$size $DIR/../svg/$f.svg $f\_$size.png
		convert  -fuzz 60% -background none -channel RGBA -fill "#$icon_disabled" -opaque black -resize $sizex$size $DIR/../svg/$f.svg $f\_disabled\_$size.png
	done

    size=64
	for f in "${small_icons[@]}"
	do
		echo "Convert $f to #$icon_enabled"
		convert  -fuzz 60% -background none -fill "#$small_icon_enabled" -opaque black -resize $sizex$size $DIR/../svg/$f.svg $f\_$size.png
		convert  -fuzz 60% -background none -channel RGBA -fill "#$icon_disabled" -opaque black -resize $sizex$size $DIR/../svg/$f.svg $f\_disabled\_$size.png
	done


}

clean
images
