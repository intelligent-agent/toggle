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

This also runs on Ubuntu/Debian desktops for development.

Here is the wiki page: http://wiki.thing-printer.com/index.php?title=Toggle

## Environment

Toggle is Python3 compatible.

**Install Toggle**

```
apt install python-setuptools python-gi
```

```
git clone https://github.com/intelligent-agent/toggle
cd toggle
pip3 install -e . -r requirements
```

## Other packages for a Debian Stretch desktop:

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
