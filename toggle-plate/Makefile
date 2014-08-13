#
# GOBject Introspection Tutorial 
# 
# Written in 2013 by Simon Kågedal Reimer <skagedal@gmail.com>
#
# To the extent possible under law, the author have dedicated all
# copyright and related and neighboring rights to this software to
# the public domain worldwide. This software is distributed without
# any warranty.
#
# CC0 Public Domain Dedication:
# http://creativecommons.org/publicdomain/zero/1.0/

CC=gcc
C_INCLUDES=`pkg-config --cflags gobject-2.0 clutter-1.0`
CFLAGS=$(C_INCLUDES) -g
LIBS=`pkg-config --libs gobject-2.0 clutter-1.0`
LIBDIR=/usr/lib

LALIB=libtoggleplate.la

OBJECTS=toggle-plate.lo
SOURCES=toggle-plate.c toggle-plate.h 

NAMESPACE=Toggle
NSVERSION=0.1
GIR_FILE=$(NAMESPACE)-$(NSVERSION).gir
TYPELIB_FILE=$(NAMESPACE)-$(NSVERSION).typelib

all: $(LALIB) $(TYPELIB_FILE)

$(LALIB): $(OBJECTS)	
	libtool link $(CC) $(LIBS) -rpath $(LIBDIR) $(OBJECTS) -o $@ 

$(TYPELIB_FILE): $(GIR_FILE)
	g-ir-compiler $(GIR_FILE) --output=$(TYPELIB_FILE)

$(GIR_FILE): $(SOURCES)
	libtool exec g-ir-scanner --warn-all $^ --library=$(LALIB) $(C_INCLUDES) --include=GObject-2.0 --include=Clutter-1.0  --namespace=$(NAMESPACE) --nsversion=$(NSVERSION) --output=$@

toggle-plate.lo: $(SOURCES)
	libtool compile $(CC) $(CFLAGS) -c $< -o $@

clean:
	-rm *.lo $(LALIB) $(TYPELIB_FILE) $(GIR_FILE)
	-rm -rf .libs


install:
	cp $(TYPELIB_FILE) /usr/lib/girepository-1.0/
	cp $(GIR_FILE) /usr/share/gir-1.0/
	cp .libs/*.so* /usr/lib/x86_64-linux-gnu/
