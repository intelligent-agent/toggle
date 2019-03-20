# -*- coding: utf-8 -*-
"""
using an existing ui layout resize everything according to a new size
"""

import json


#==============================================================================
#
#==============================================================================
def linear_scale(old, new, x):
  """
    scale something that is in the range 0 <= x <= old
    to lie within the range 0 <= x <= new
    """

  return int((x / float(old)) * new)


def traverse(name, data, f, original=None, address=""):
  """
    given a json dictinary traverse to every leaf and perform a given function
    on that leaf
    """

  if type(data) is type([]):
    for i, element in enumerate(data):
      traverse(name, element, f, original, address + "[%i]" % i)
  elif type(data) is type({}):
    for attribute, value in data.iteritems():
      traverse(attribute, value, f, original, address + "['%s']" % attribute)
  else:
    f(name, data, original, address)

  return


def print_leaf(name, data, original, address):
  """
    print out stuff
    """
  print name, ": ", data


def scale(name, data, original, address):
  """
    resize selected integer values
    """

  global old_w, old_h, w, h

  if (name == "width"):
    if data == old_w:
      data = w
    else:
      linear_scale(old_w, w, data)
  elif (name == "height"):
    if data == old_h:
      data = h
    else:
      linear_scale(old_h, h, data)
  elif name == "x":
    data = linear_scale(old_w, w, data)
  elif name == "y":
    data = linear_scale(old_h, h, data)

  if type(data) == type(1):
    exec("original" + address + "=" + str(data))

  return


#==============================================================================
#
#==============================================================================

if __name__ == "__main__":

  # the name of the ui that we are using as a basis for resizing
  name = "ui_800x480.json"

  # the width and height of the original whose name we have given above
  old_w = 800
  old_h = 480

  # the size of the scaled (new) ui
  w = 1320
  h = 1080

  # load in the original
  js_f = open(name, "r")
  js = json.load(js_f)
  js_f.close()

  # go through the json data and operate on it
  traverse("head", js, scale, js)
  #traverse("head", js, print_leaf)

  # save out our new json file
  new_name = name.replace(str(old_w), str(w))
  new_name = new_name.replace(str(old_h), str(h))
  ns_f = open(new_name, 'w')

  json.dump(js, ns_f, indent=4)

  ns_f.close()

  print "DONE"

  # all done!
