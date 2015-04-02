CC?=gcc
C_INCLUDES=`pkg-config --cflags gobject-2.0 glib-2.0 clutter-1.0 mash-0.2 pango cairo mx-1.0`
CFLAGS+=$(C_INCLUDES) -g
LIBS=`pkg-config --libs gobject-2.0 glib-2.0 clutter-1.0 mash-0.2 pango cairo mx-2.0` -L./.libs
LIBDIR=/usr/lib/arm-linux-gnueabihf
LIBTOOL?=/usr/src/mash/libtool
GILIB=/usr/lib/arm-linux-gnueabihf/girepository-1.0
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
	g-ir-scanner --warn-all $^ --library=toggle -L/usr/src/toggle/toggle-lib/.libs $(C_INCLUDES) $(GIR_SCANNER_ARGS) --include=GObject-2.0 --include=Clutter-1.0 --include=Mash-0.2 --namespace=$(NAMESPACE) --nsversion=$(NSVERSION) --output=$@

toggle-box.lo: toggle-box.c toggle-box.h
	$(LIBTOOL) compile --tag=CC $(CC) $(CFLAGS) -c $< -o $@

toggle-model.lo: toggle-model.c toggle-model.h
	$(LIBTOOL) compile --tag=CC $(CC) $(CFLAGS) -c $< -o $@

clean:
	-rm *.lo *.o $(LALIB) $(TYPELIB_FILE) $(GIR_FILE)
	-rm -rf .libs


install:
	cp $(TYPELIB_FILE) $(GILIB)
	cp $(GIR_FILE) /usr/share/gir-1.0/
	cp .libs/*.so.0.0.0 $(LIBDIR)	
	rm -f $(LIBDIR)/libtoggle.so
	rm -f $(LIBDIR)/libtoggle.so.0
	ln -s $(LIBDIR)/libtoggle.so.0.0.0 $(LIBDIR)/libtoggle.so.0
	ln -s $(LIBDIR)/libtoggle.so.0 $(LIBDIR)/libtoggle.so
