PKGFLAGS=`pkg-config --cflags --libs clutter-1.0 mx-2.0 mash-0.2 pango cairo` -DCOGL_ENABLE_EXPERIMENTAL_2_0_API

SRC=toggle.c plate_actor.c

all:
	gcc $(PKGFLAGS) $(SRC) -o toggle

clean: 
	rm -rf toggle
