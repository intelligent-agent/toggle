SRC=toggle.c plate_actor.c
CC ?= gcc
CFLAGS+= `pkg-config --cflags clutter-1.0 mx-2.0 mash-0.2 pango cairo` 
CFLAGS+= -DCOGL_ENABLE_EXPERIMENTAL_2_0_API
LDFLAGS+= -pthread -lmx-2.0 -lmash-0.2 -lclutter-1.0 -lcairo-gobject -latk-1.0 -lpangocairo-1.0 -lcogl-pango -ljson-glib-1.0 
LDFLAGS+= -lgudev-1.0 -levdev -lxkbcommon -lcogl -lgmodule-2.0 -lgdk_pixbuf-2.0 -lEGL -lgio-2.0 -lpango-1.0 -lgobject-2.0 
LDFLAGS+= -lglib-2.0 -lcairo

all:
	$(CC) $(CFLAGS) $(SRC) -o toggle $(LDFLAGS)

clean: 
	rm -rf toggle
