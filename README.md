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


##Debian Jessie install instructions:
Jessie has a lot more updated packages, 
so more can be installed with apt-get. 

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


**cogl 1.22.0:**
```
cd /usr/src
wget http://ftp.gnome.org/pub/GNOME/sources/cogl/1.22/cogl-1.22.2.tar.xz
tar xf cogl-1.22.2.tar.xz
cd cogl-1.22.2/
./configure --prefix=/usr --libdir=/usr/lib/arm-linux-gnueabihf/ --enable-introspection --disable-gles1 --disable-cairo --disable-gl --enable-gles2 --enable-null-egl-platform --enable-cogl-pango
sed -i 's/#if COGL_HAS_WAYLAND_EGL_SERVER_SUPPORT/#ifdef COGL_HAS_WAYLAND_EGL_SERVER_SUPPORT/' cogl/winsys/cogl-winsys-egl.c 
make
make install 
```

**libinput-1.0.0**
```
cd /usr/src
wget http://www.freedesktop.org/software/libinput/libinput-1.0.0.tar.xz
./configure --prefix=/usr --libdir=/usr/lib/arm-linux-gnueabihf/
make
make install
```

**glib-2.48.2**
Glib from apt gets installed in /lib, so library path must be set from here on. 
```
cd /usr/src
wget http://ftp.gnome.org/pub/gnome/sources/glib/2.48/glib-2.48.2.tar.xz
tar xf glib-2.48.2.tar.xz
cd glib-2.48.2/
./configure --prefix=/usr --libdir=/usr/lib/arm-linux-gnueabihf/
make
make install
export LD_LIBRARY_PATH=/usr/lib/arm-linux-gnueabihf/
```

**Clutter 1.26**
Note: Clutter 1.26 requires Glib >=2.44 which is not installed on Debian Jessie. 
```
cd /usr/src
wget http://ftp.acc.umu.se/pub/GNOME/sources/clutter/1.26/clutter-1.26.0.tar.xz
tar xf clutter-1.26.0.tar.xz
cd clutter-1.26.0
LD_LIBRARY_PATH=/usr/lib/arm-linux-gnueabihf/ ./configure --prefix=/usr --libdir=/usr/lib/arm-linux-gnueabihf/ --disable-x11-backend  --enable-egl-backend --enable-evdev-input --disable-gdk-backend
make
make install
```

**Mx**
Note: the pkg-config files were installed in the standard 
```
cd /usr/src
git clone https://github.com/clutter-project/mx.git
 ./autogen.sh --prefix=/usr --libdir=/usr/lib/arm-linux-gnueabihf/ --with-winsys=none --disable-gtk-doc --enable-introspection 
make
make install
```

**Mash (with STL-import)**
Note: Disable compiling the examples and 
use the right --library format for the g-ir-scanner
```
cd /usr/src/
git clone https://github.com/eliasbakken/mash.git
cd /usr/src/mash
./autogen.sh --prefix=/usr --libdir=/usr/lib/arm-linux-gnueabihf/ --enable-introspection
sed -i 's/--library=mash-@MASH_API_VERSION@/--library=mash-@MASH_API_VERSION@/ --library-path=/usr/src/mash/mash/.libs/' mash/Makefile.am
make
make install
```

**Toggle**
```
cd /usr/src
git clone https://intelligentagent@bitbucket.org/intelligentagent/toggle.git
cd toggle
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



## Ubuntu Xenial 
**Mash**
```
apt install autogen gnome-common gtk-doc gtk-doc-tools libglib2.0-dev gobject-introspection libmx-dev python-gobject-dev libgirepository1.0-dev
```

```
git clone https://github.com/eliasbakken/mash.git
cd /usr/src/mash
./autogen.sh --prefix=/usr --enable-introspection
make
make install
```
**Install Toggle**
```
apt install python-setuptools python-gi python-requests python-tornado
```

```
cd /usr/src
git clone https://bitbucket.org/intelligentagent/toggle
cd toggle
sudo make install
```



