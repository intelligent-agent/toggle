SRC=toggle.c plate_actor.c
CC ?= gcc
CFLAGS+= -DCOGL_ENABLE_EXPERIMENTAL_2_0_API

all:
	$(CC)  $(CFLAGS) $(SRC) -o toggle $(LDFLAGS) `pkg-config --cflags --libs clutter-1.0  mash-0.2 pango cairo mx-1.0`

install: 
	mkdir -p /etc/toggle/style
	cp style/* /etc/toggle/style/
	cp ui.json /etc/toggle/
	mkdir -p /usr/share/models/
	cp models/*.ply /usr/share/models

clean: 
	rm -rf toggle
