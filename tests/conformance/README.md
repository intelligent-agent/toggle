# Unit Testing

This test platform supports execution outside of a physical Beagle Bone Black, say on a local Linux ia64 or whatever.

A virtual environment is recommended. Example set-up for testing only ...

```
$ pip3 install -r requirements.txt
$ python3 -m pytest
==== test session starts ====
platform linux -- Python 3.7.3, pytest-5.0.1, py-1.8.0, pluggy-0.12.0
rootdir: /home/elias/workspace/toggle, inifile: setup.cfg
plugins: requests-mock-1.6.0
collected 9 items
```

If running tests on the BeagleBone, which has limited storage, it's probably best to skip the virtual environment and go straight to `pip3 install -r tests/requirements.txt`.
