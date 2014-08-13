SRC=toggle.c toggle/toggle-model.c toggle/toggle-plate.c
CC?=cc
CFLAGS+= -DCOGL_ENABLE_EXPERIMENTAL_2_0_API -Itoggle
LDFLAGS+=-Ltoggle

all:
	$(CC)  $(CFLAGS) $(SRC) -o run $(LDFLAGS) `pkg-config --cflags --libs clutter-1.0  mash-0.2 pango cairo mx-2.0` 

install: 
	mkdir -p /etc/toggle/style
	cp style/* /etc/toggle/style/
	cp ui.json /etc/toggle/
	mkdir -p /usr/share/models/
	cp models/*.ply /usr/share/models
	cp run /usr/bin/toggle

clean:
	rm run
