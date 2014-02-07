SRC=toggle.c plate_actor.c
CC ?= gcc
CFLAGS+= -DCOGL_ENABLE_EXPERIMENTAL_2_0_API

all:
	$(CC) $(CFLAGS) $(SRC) -o toggle $(LDFLAGS) `pkg-config --cflags --libs clutter-1.0 mx-2.0 mash-0.2 pango cairo` 

clean: 
	rm -rf toggle
