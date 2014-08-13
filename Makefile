SRC=toggle.c
CC ?= gcc
CFLAGS+=`pkg-config --cflags --libs clutter-1.0  mash-0.2 pango cairo mx-2.0`

all: toggle.o toggle-plate
	$(CC)  $(CFLAGS) toggle.o -o toggle $(LDFLAGS) 

toggle.o:
	$(CC)  $(CFLAGS) toggle.c -o toggle.o

install: 
	mkdir -p /etc/toggle/style
	cp style/* /etc/toggle/style/
	cp ui.json /etc/toggle/
	mkdir -p /usr/share/models/
	cp models/*.ply /usr/share/models

clean: 
	rm -rf toggle
