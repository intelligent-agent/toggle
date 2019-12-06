```python
_/_/_/_/_/                              _/
   _/      _/_/      _/_/_/    _/_/_/  _/    _/_/
  _/    _/    _/  _/    _/  _/    _/  _/  _/_/_/_/
 _/    _/    _/  _/    _/  _/    _/  _/  _/
_/      _/_/      _/_/_/    _/_/_/  _/    _/_/_/
                     _/        _/
                _/_/      _/_/
```

[![Build Status](https://travis-ci.org/intelligent-agent/toggle.svg?branch=dev)](https://travis-ci.org/intelligent-agent/toggle)

Toggle is a 3D-printer front end for use with embedded devices.
It's a perfect fit for the BeagleBone Black/Replicape/Manga Screen combo.

The program is built on a windowless BeagleBone Black (egl-null) using Clutter,
Cogl, Mash and Mx with introspection for Python bindings.

This makes it fast while keeping a nice Python structure on top for gluing the
code together.

This also runs on Ubuntu/Debian desktops for development.

Here is the wiki page: http://wiki.thing-printer.com/index.php?title=Toggle

## Environment

- Toggle is Python3 compatible.
- Code is formatted using YAPF, check the setup.cfg for style.
- Travis is set up to check formatting. Use yapf3.

**Install Toggle**

Required Packages

```
apt install python3-setuptools python3-gi python3-pip python3-dev libdbus-1-dev libglib2.0-dev python3-cairo python3-gi-cairo
pip3 install wheel
```

Install actual program

```
git clone https://github.com/intelligent-agent/toggle
cd toggle
git checkout dev
pip3 install -e . -r requirements.txt
python3 setup.py install_data
```

## Other packages for a Debian Stretch/Buster desktop:

Standard packages in Stretch:
libinput-1.2.2-1
Cogl-1.22.0-2
Clutter-1.26.0-2

On Debian Stretch and older:
libmx-1.0-2 (1.4.7-1 and others)

On Debian Buster, libmx is no longer maintained, so it needs to be installed from source:
https://github.com/eliasbakken/mx

Also needed is Mash, install from this repository:
https://github.com/eliasbakken/mash
