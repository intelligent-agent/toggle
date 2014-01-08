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

We hope to be able to use introspection and use Python as the programming language (PyGObject), 
but since the Cogl framework is not working good with introspection, the first demo is written in c. 
There is also a demo using Python, but shading of the 3D model is not working. 

Clutter as the toolkit used for the 2D layout, Cogl for 3D, MX for widgets and Mash for loading the model and lighting. 

Here is the wiki page: http://wiki.thing-printer.com/index.php?title=Toggle
