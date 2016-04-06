```python
_/_/_/_/_/                              _/         
   _/      _/_/      _/_/_/    _/_/_/  _/    _/_/     
  _/    _/    _/  _/    _/  _/    _/  _/  _/_/_/_/    
 _/    _/    _/  _/    _/  _/    _/  _/  _/            
_/      _/_/      _/_/_/    _/_/_/  _/    _/_/_/         
                     _/        _/                               
                _/_/      _/_/                                  
```

Toggle is a 3D-printer front end for use with embedded devices. 
It's a perfect fit for the BeagleBone Black/Replicape/Manga Screen combo.

The program is built on a windowless BeagleBone Black (egl-null) using Clutter, 
Cogl, Mash and Mx with introspection for Python bindings. 

This makes it fast while keeping a nice Python structure on top for gluing the 
code together. 

This also runs on my Ubuntu 14.04 desktop for development. 

Right now, this is more of a demo/proof of concept, so help is welcome : )

Here is the wiki page: http://wiki.thing-printer.com/index.php?title=Toggle

## Installation on Angstrom:  
```
opkg install toggle
```
It comes pre-installed on the [Thing image](http://wiki.thing-printer.com/index.php?title=Thing_image)

## Installation on debian Wheezy:  
** NOTE: Work in progress **  
The clutter version (1.10) in Sqeeze is outdated, so a lot needs compilation from source.   
```
sudo apt-get install gnome-common gtk-doc-tools libffi-dev python-dev
```

**New Kernel and SGX modules**
```
sudo apt-get install ti-sgx-es8-modules-3.18.0-rc7-bone1
sudo apt-get install libgles2-mesa-dev
```

**SGX SDK**
```
cd /usr/src
wget https://bitbucket.org/intelligentagent/toggle/downloads/GFX_5.01.01.01.tar.gz
tar xfv GFX_5.01.01.01.tar.gz -C /
cd /opt/gfxinstall
./sgx-install.sh
sync
reboot
```

**glib 2.42.1:**
```
  cd /usr/src
  wget  http://ftp.gnome.org/pub/gnome/sources/glib/2.42/glib-2.42.1.tar.xz
  tar xf glib-2.42.1.tar.xz
  cd glib-2.42.1
  ./configure --prefix=/usr
  make
  make install
```
** Use the new Glib instead of the pre installed **
This list is not complete! And it is probably the wrong way to do it, but I have not found a better way!
```
mv /usr/lib/arm-linux-gnueabihf/libgmodule-2.0.a /usr/lib/arm-linux-gnueabihf/libgmodule-2.0.a.old
mv /usr/lib/arm-linux-gnueabihf/pkgconfig/glib-2.0.pc /usr/lib/arm-linux-gnueabihf/pkgconfig/glib-2.0.pc.old
mv /usr/lib/arm-linux-gnueabihf/libgobject-2.0.a /usr/lib/arm-linux-gnueabihf/libgobject-2.0.a.old
mv /usr/lib/arm-linux-gnueabihf/libgobject-2.0.so /usr/lib/arm-linux-gnueabihf/libgobject-2.0.so.old

export ACLOCAL_PATH=/usr/share/aclocal/
export PKG_CONFIG_PATH=/usr/lib/pkgconfig
export LD_LIBRARY_PATH=/usr/lib
export PATH=/usr/bin:$PATH
```

**gobject-introspection-1.42.0:**
```
cd /usr/bin
ln -s python2.7-config python-config
cd /usr/src
wget http://ftp.gnome.org/pub/gnome/sources/gobject-introspection/1.42/gobject-introspection-1.42.0.tar.xz
tar xf gobject-introspection-1.42.0.tar.xz
cd gobject-introspection-1.42.0
./configure --prefix=/usr PKG_CONFIG_PATH=/usr/lib/pkgconfig/ LIBS="-L/usr/lib"
make
make install 
```

**cogl 1.18.2:**
```
cd /usr/src
wget http://ftp.gnome.org/pub/gnome/sources/cogl/1.20/cogl-1.20.0.tar.xz
tar xf cogl-1.20.0.tar.xz
cd cogl-1.20.0/
./configure --prefix=/usr --enable-introspection --disable-gles1 --disable-cairo --disable-gl --enable-gles2 --enable-null-egl-platform --enable-cogl-pango
make 
make install 
```

** Atk-2.14.0 **
```
wget ftp://ftp.gnome.org/pub/gnome/sources/atk/2.14/atk-2.14.0.tar.xz
tar xf atk-2.14.0.tar.xz
...
```
**mtdev and udev**
```
sudo apt-get install libmtdev-dev
sudo apt-get install libudev-dev
sudo apt-get install libgudev-1.0-dev
```

**xkbcommon-0.5.0**
```
wget http://xkbcommon.org/download/libxkbcommon-0.5.0.tar.xz
tar xf libxkbcommon-0.5.0.tar.xz
./configure --prefix=/usr --disable-x11
make
make install
```

**libinput-0.7.0**
```
cd /usr/src
wget http://www.freedesktop.org/software/libinput/libinput-0.7.0.tar.xz
./configure --prefix=/usr
make
```

**clutter 1.21:**
```
wget ftp://ftp.gnome.org/pub/gnome/sources/clutter/1.21/clutter-1.21.2.tar.xz
./configure --prefix=/usr --disable-x11-backend  --enable-egl-backend --enable-evdev-input
make 
make install
```
```
sudo apt-get install gir1.2-clutter-1.0 gir1.2-mx-1.0 gobject-introspection
```

**Mash **
```
git clone https://github.com/eliasbakken/mash.git /usr/src/mash
cd /usr/src/mash
./autogen.sh --prefix=/usr
make
make install
```

**Mx**
```
git clone https://github.com/clutter-project/mx.git
./autogen.sh --prefix=/usr --disable-gtk-widgets --with-dbus --with-winsys=none --disable-gtk-doc
make
make install
```

**Toggle**
```
cd /usr/src
git clone https://intelligentagent@bitbucket.org/intelligentagent/toggle.git
cd toggle
python setup.py install 
cd toggle-lib
make 
make install
```
** Running Toggle from the command line**
```
systemctl stop lightdm.service
toggle
```
** Making Toggle start by default **
```
cd /usr/src/toggle/
cp systemd/toggle.service /etc/systemd/system
systemctl enable toggle.service
systemctl mask lightdm.service
```
The library path needs to be set on scriopt startup, so edit the systemd script:
```
nano /etc/systemd/system/toggle.service
```
Add:
```
Environment="LD_LIBRARY_PATH=/usr/lib"
```
to the service section




##Debian Jessie install instructions:
Jessie has a lot more updated packages, 
so more can be installed with Aptitude. 

WIP!

**New kernel and sgx modules**
```
sudo apt-get install ti-sgx-es8-modules-4.0.0-rc6-bone0
```
Packages that need to be installed:
```
sudo apt-get install libglib2.0-dev pkg-config libpango1.0-dev gobject-introspection libgirepository1.0-dev 
libgdk-pixbuf2.0-dev libatk1.0-dev libevdev-dev libxkbcommon-dev libinput-dev libmtdev-dev 
libjson-glib-dev libgudev-1.0-dev autogen python-gobject
```

**SGX SDK**
```
cd /usr/src
wget https://bitbucket.org/intelligentagent/toggle/downloads/GFX_5.01.01.01.tar.gz
tar xfv GFX_5.01.01.01.tar.gz -C /
cd /opt/gfxinstall
./sgx-install.sh
sed -i 's:/sys/devices/ocp*/56000000.sgx:/sys/devices/platform/ocp*/56000000.sgx:' /etc/init.d/sgx-startup.sh
```
pvrsrvkm should now be shown in lsmod


**cogl 1.18.0:**
```
cd /usr/src
wget http://ftp.gnome.org/pub/gnome/sources/cogl/1.18/cogl-1.18.2.tar.xz
tar xf cogl-1.18.2.tar.xz
cd cogl-1.18.2/
./configure --prefix=/usr --libdir=/usr/lib/arm-linux-gnueabihf/ --enable-introspection --disable-gles1 --disable-cairo --disable-gl --enable-gles2 --enable-null-egl-platform --enable-cogl-pango
make 
make install 
```

**libinput-0.7.0**
```
cd /usr/src
wget http://www.freedesktop.org/software/libinput/libinput-0.7.0.tar.xz
tar xf libinput-0.7.0.tar.xz
cd libinput-0.7.0
./configure --prefix=/usr --libdir=/usr/lib/arm-linux-gnueabihf/
make
make install
```

**clutter 1.22:**
```
cd /usr/src
wget ftp://ftp.gnome.org/pub/gnome/sources/clutter/1.22/clutter-1.22.0.tar.xz
tar xf clutter-1.22.0.tar.xz
cd clutter-1.22.0
./configure --prefix=/usr --libdir=/usr/lib/arm-linux-gnueabihf/ --disable-x11-backend  --enable-egl-backend --enable-evdev-input
make 
make install
```

wget ftp://ftp.gnome.org/pub/gnome/sources/clutter/1.21/clutter-1.21.2.tar.xz


**Mx**
Note: the pkg-config files were installed in the standard 
```
cd /usr/src
git clone https://github.com/clutter-project/mx.git
./autogen.sh --prefix=/usr --libdir=/usr/lib/arm-linux-gnueabihf/ --disable-gtk-widgets --with-dbus --with-winsys=none --disable-gtk-doc
make
make install
cp /usr/lib/arm-linux-gnueabihf/pkgconfig/mx-2.0.pc /usr/lib/arm-linux-gnueabihf/pkgconfig/mx-1.0.pc
```

**Mash (with STL-import)**
Note: Disable compiling the examples and 
use the right --library format for the g-ir-scanner
```
cd /usr/src/
git clone https://github.com/eliasbakken/mash.git
cd /usr/src/mash
./autogen.sh --prefix=/usr --libdir=/usr/lib/arm-linux-gnueabihf/ --enable-introspection
sed -i 's/SUBDIRS = mash examples docs/SUBDIRS = mash docs/' Makefile
sed -i 's/--library=libmash-@MASH_API_VERSION@.la/--library=mash-@MASH_API_VERSION@/ --library-path=/usr/src/mash/mash/.libs/' mash/Makefile.am
make
make install
```

**Toggle**
Note: On Debian Jessie, the only way I could compile the gir/typelib was to link to the library 
by full path. Adding this to the /usr/src/toggle/toggle-lib/Makefile:
-L /usr/src/toggle/toggle-lib/.libs
in the target for $(GIR_FILE)
```
cd /usr/src
git clone https://intelligentagent@bitbucket.org/intelligentagent/toggle.git
cd toggle
python setup.py install 
cd toggle-lib
sed -i 's:LIBTOOL?=libtool:LIBTOOL?=/usr/src/mash/libtool:' Makefile
sed -i 's:--library=$(LALIB):--library=toggle -L/usr/src/toggle/toggle-lib/.libs:' Makefile
make 
make install
```


CLUTTER_BACKEND=eglnative toggle



##Debian Stretch install instructions:


Standard packages in Stretch:
libinput-1.2.2-1
Cogl-1.22.0-2
Clutter-1.26.0-2
libmx-1.0-2 (1.4.7-1 and others)

**Mash (with STL-import)**
Note: Disable compiling the examples and 
use the right --library format for the g-ir-scanner
```
cd /usr/src/
git clone https://github.com/eliasbakken/mash.git
cd /usr/src/mash
./autogen.sh --prefix=/usr --libdir=/usr/lib/arm-linux-gnueabihf/ --enable-introspection
sed -i 's/SUBDIRS = mash examples docs/SUBDIRS = mash docs/' Makefile
sed -i 's/--library=libmash-@MASH_API_VERSION@.la/--library=mash-@MASH_API_VERSION@/ --library-path=/usr/src/mash/mash/.libs/' mash/Makefile.am
make
make install
```

