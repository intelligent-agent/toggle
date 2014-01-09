PKGFLAGS=`pkg-config --cflags --libs clutter-1.0 mx-2.0 mash-0.2 pango cairo` -DCOGL_ENABLE_EXPERIMENTAL_2_0_API


all:
	gcc $(PKGFLAGS) main.c plate_actor.c -o main

clean: 
	rm -rf main
