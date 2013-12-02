    :::python
    _/_/_/_/_/                              _/         
       _/      _/_/      _/_/_/    _/_/_/  _/    _/_/     
      _/    _/    _/  _/    _/  _/    _/  _/  _/_/_/_/    
     _/    _/    _/  _/    _/  _/    _/  _/  _/            
    _/      _/_/      _/_/_/    _/_/_/  _/    _/_/_/         
                         _/        _/                               
                    _/_/      _/_/                                  

Toggle is a 3D-printer front end for use with embedded devices. It's a perfect fit for the BeagleBone Black/Replicape/Manga Screen combo.

The current implementation relies on wxpython and OpenGL. Since it will run on embedded platforms, 
this is being ported to OpenGL ES 2. To keep things fast, we want to use Wayland as a protocol with Weston as compositor, 
and Clutter as the toolkit with Python as the language binding (PyClutter). Suggestions for other approaches are welcome : )

Here is the wiki page: http://wiki.thing-printer.com/index.php?title=Toggle
