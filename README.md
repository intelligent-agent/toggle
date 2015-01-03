:::python
    _/_/_/_/_/                              _/         
       _/      _/_/      _/_/_/    _/_/_/  _/    _/_/     
      _/    _/    _/  _/    _/  _/    _/  _/  _/_/_/_/    
     _/    _/    _/  _/    _/  _/    _/  _/  _/            
    _/      _/_/      _/_/_/    _/_/_/  _/    _/_/_/         
                         _/        _/                               
                    _/_/      _/_/                                  

Toggle is a 3D-printer front end for use with embedded devices. 
It's a perfect fit for the BeagleBone Black/Replicape/Manga Screen combo.

The program is built on a windowless BeagleBone Black (egl-null) using Clutter, 
Cogl, Mash and Mx with introspection for Python bindings. 

This makes it fast while keeping a nice Python structure on top for gluing the 
code together. 

This also runs on my Ubuntu 14.04 desktop for development. 

Right now, this is more of a demo/proof of concept, so help is welcome : )

Here is the wiki page: http://wiki.thing-printer.com/index.php?title=Toggle

Installation on Angstrom: 
`opkg install toggle`

Installation on debian:  
** NOTE: Work in progress **
The clutter version (1.10) in Sqeeze is outdated, so a lot needs compilation from source. 

  sudo apt-get install gnome-common gtk-doc-tools libffi-dev python-dev

** New Kernel and SGX modules **
  sudo apt-get install ti-sgx-es8-modules-3.18.0-rc7-bone1 
  sudo apt-get install libgles2-mesa-dev

**glib 2.42.1:**
  cd /usr/src
  wget  http://ftp.gnome.org/pub/gnome/sources/glib/2.42/glib-2.42.1.tar.xz
  tar xf glib-2.42.1.tar.xz
  cd glib-2.42.1
  ./configure --prefix=/usr
  make
  make install
OK

**glib 2.34.3:**
 ./configure --prefix=/usr PKG_CONFIG_PATH=/usr/lib/pkgconfig/
make
make install
OK 

**gobject-introspection-1.34.2:**
./configure --prefix=/usr PKG_CONFIG_PATH=/usr/lib/pkgconfig/
make
FAILS with undefined reference to `g_time_zone_get_type'

# This list is not complete! And it is probably the wrong way to do it, but I have not found a better way!
mv /usr/lib/arm-linux-gnueabihf/libgmodule-2.0.a /usr/lib/arm-linux-gnueabihf/libgmodule-2.0.a.old
mv /usr/lib/arm-linux-gnueabihf/pkgconfig/glib-2.0.pc /usr/lib/arm-linux-gnueabihf/pkgconfig/glib-2.0.pc.old
mv /usr/lib/arm-linux-gnueabihf/libgobject-2.0.a /usr/lib/arm-linux-gnueabihf/libgobject-2.0.a.old
mv /usr/lib/arm-linux-gnueabihf/libgobject-2.0.so /usr/lib/arm-linux-gnueabihf/libgobject-2.0.so.old


#gobject-introspection-1.42.0:
cd /usr/bin
ln -s python2.7-config python-config
cd /usr/src
wget ...
tar ...
export ACLOCAL_PATH=/usr/share/aclocal/
export PKG_CONFIG_PATH=/usr/lib/pkgconfig
export LD_LIBRARY_PATH=/usr/lib
export PATH=/usr/bin:$PATH
./configure --prefix=/usr PKG_CONFIG_PATH=/usr/lib/pkgconfig/ LIBS="-L/usr/lib"
make
#make install 


**cogl 1.18.2:**
./configure --prefix=/usr --enable-introspection --disable-gles1 --disable-cairo --disable-gl --enable-gles2 --enable-null-egl-platform --enable-cogl-pango
make 
make install 
OK

** Atk-2.14.0 **
wget ftp://ftp.gnome.org/pub/gnome/sources/atk/2.14/atk-2.14.0.tar.xz
tar xf atk-2.14.0.tar.xz


**clutter 1.21:**
wget ftp://ftp.gnome.org/pub/gnome/sources/clutter/1.21/clutter-1.21.2.tar.xz
./configure --prefix=/usr --disable-x11-backend  --enable-egl-backend --enable-evdev-input
make 
make install


sudo apt-get install libclutter-1.0-dev gir1.2-clutter-1.0 libmx-1.0-2 gir1.2-mx-1.0 gobject-introspection

**Mash **
git clone https://github.com/eliasbakken/mash.git /usr/src/mash
cd /usr/src/mash
./autogen.sh --prefix=/usr

**Mx**
git clone https://github.com/clutter-project/mx.git
./autogen.sh --prefix=/usr --disable-gtk-widgets --with-dbus --with-winsys=none --disable-gtk-doc
make
make install