CC?=gcc
C_INCLUDES=`pkg-config --cflags gobject-2.0 glib-2.0 clutter-1.0 mash-0.2 pango cairo mx-1.0`
CFLAGS+=$(C_INCLUDES) -g
LIBS=`pkg-config --libs gobject-2.0 glib-2.0 clutter-1.0 mash-0.2 pango cairo mx-1.0` -L/lib -L./.libs
LIBDIR=/usr/lib
LIBTOOL?=libtool

GIR_SCANNER_ARGS=

LALIB=libtoggle.la

OBJECTS=toggle-model.lo toggle-box.lo
SOURCES=toggle-model.h toggle-model.c toggle-box.c toggle-box.h

NAMESPACE=Toggle
NSVERSION?=0.4
GIR_FILE=$(NAMESPACE)-$(NSVERSION).gir
TYPELIB_FILE=$(NAMESPACE)-$(NSVERSION).typelib

all: $(LALIB) $(TYPELIB_FILE)

$(LALIB): $(OBJECTS)	
	$(LIBTOOL) link --tag=CC $(CC) $(LIBS) -rpath $(LIBDIR) $(OBJECTS) -o $@ 

$(TYPELIB_FILE): $(GIR_FILE)
	g-ir-compiler $(GIR_FILE) --output=$(TYPELIB_FILE)

$(GIR_FILE): $(SOURCES)
	g-ir-scanner --warn-all $^ --library=$(LALIB) $(C_INCLUDES) $(GIR_SCANNER_ARGS) --include=GObject-2.0 --include=Clutter-1.0 --include=Mash-0.2 --namespace=$(NAMESPACE) --nsversion=$(NSVERSION) --output=$@

toggle-box.lo: toggle-box.c toggle-box.h
	$(LIBTOOL) compile --tag=CC $(CC) $(CFLAGS) -c $< -o $@

toggle-model.lo: toggle-model.c toggle-model.h
	$(LIBTOOL) compile --tag=CC $(CC) $(CFLAGS) -c $< -o $@

clean:
	-rm *.lo *.o $(LALIB) $(TYPELIB_FILE) $(GIR_FILE)
	-rm -rf .libs


install:
	cp $(TYPELIB_FILE) /usr/lib/girepository-1.0/
	cp $(GIR_FILE) /usr/share/gir-1.0/
	cp .libs/*.so.0.0.0 /usr/lib/	
	rm -f /usr/lib/libtoggle.so
	rm -f /usr/lib/libtoggle.so.0
	ln -s /usr/lib/libtoggle.so.0.0.0 /usr/lib/libtoggle.so.0
	ln -s /usr/lib/libtoggle.so.0 /usr/lib/libtoggle.so
	cp .libs/*.so.0.0.0 /usr/lib/x86_64-linux-gnu/
	rm -f /usr/lib/x86_64-linux-gnu/libtoggle.so
	rm -f /usr/lib/x86_64-linux-gnu/libtoggle.so.0
	ln -s /usr/lib/x86_64-linux-gnu/libtoggle.so.0.0.0 /usr/lib/x86_64-linux-gnu/libtoggle.so.0
	ln -s /usr/lib/x86_64-linux-gnu/libtoggle.so.0 /usr/lib/x86_64-linux-gnu/libtoggle.so 
