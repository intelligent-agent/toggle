CC?=gcc
C_INCLUDES=`pkg-config --cflags gobject-2.0 glib-2.0 clutter-1.0 mash-0.2 pango cairo mx-2.0`
CFLAGS+=$(C_INCLUDES) -g
LIBS=`pkg-config --libs gobject-2.0 glib-2.0 clutter-1.0 mash-0.2 pango cairo mx-2.0` -L/lib -L/usr/local/lib
LIBDIR=/usr/lib
LIBTOOL?=libtool

GIR_SCANNER_ARGS=

LALIB=libtoggle.la

OBJECTS=toggle-model.lo toggle-plate.lo
SOURCES=toggle-plate.c toggle-model.c toggle-plate.h toggle-model.h

NAMESPACE=Toggle
NSVERSION=0.1
GIR_FILE=$(NAMESPACE)-$(NSVERSION).gir
TYPELIB_FILE=$(NAMESPACE)-$(NSVERSION).typelib

all: $(LALIB) $(TYPELIB_FILE)

$(LALIB): $(OBJECTS)	
	$(LIBTOOL) link --tag=CC $(CC) $(LIBS) -rpath $(LIBDIR) $(OBJECTS) -o $@ 

$(TYPELIB_FILE): $(GIR_FILE)
	g-ir-compiler $(GIR_FILE) --output=$(TYPELIB_FILE)

$(GIR_FILE): $(SOURCES)
	g-ir-scanner --warn-all $^ --library=$(LALIB) $(C_INCLUDES) $(GIR_SCANNER_ARGS) --include=GObject-2.0 --include=Clutter-1.0 --include=Mash-0.2 --namespace=$(NAMESPACE) --nsversion=$(NSVERSION) --output=$@

toggle-plate.lo: toggle-plate.c toggle-plate.h
	$(LIBTOOL) compile --tag=CC $(CC) $(CFLAGS) -c $< -o $@

toggle-model.lo: toggle-model.c toggle-model.h
	$(LIBTOOL) compile --tag=CC $(CC) $(CFLAGS) -c $< -o $@

clean:
	-rm *.lo *.o $(LALIB) $(TYPELIB_FILE) $(GIR_FILE)
	-rm -rf .libs


install:
	cp $(TYPELIB_FILE) /usr/lib/girepository-1.0/
	cp $(GIR_FILE) /usr/share/gir-1.0/
	cp .libs/*.so* /usr/lib/
	cp .libs/*.so* /usr/lib/x86_64-linux-gnu/
