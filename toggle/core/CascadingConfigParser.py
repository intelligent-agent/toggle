"""
Author: Elias Bakken
email: elias(dot)bakken(at)gmail(dot)com
Website: http://www.thing-printer.com
License: GNU GPL v3: http://www.gnu.org/copyleft/gpl.html

 Redeem is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 Redeem is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with Redeem.  If not, see <http://www.gnu.org/licenses/>.
"""

import configparser
import os
import logging


class CascadingConfigParser(configparser.ConfigParser):
  def __init__(self, config_files):
    configparser.ConfigParser.__init__(self)
    self.config_files = []
    for config_file in config_files:
      self.config_files.append(os.path.realpath(config_file))
      self.config_location = os.path.dirname(os.path.realpath(config_file))
    for config_file in self.config_files:
      if os.path.isfile(config_file):
        logging.info("Using config file " + config_file)
        self.read_file(open(config_file))
      else:
        logging.warning("Missing config file " + config_file)

  def timestamp(self):
    """ Get the largest (newest) timestamp for all the config files. """
    ts = 0
    for config_file in self.config_files:
      if os.path.isfile(config_file):
        ts = max(ts, os.path.getmtime(config_file))
    return ts

  def check_file_valid(self, filename):
    default = configparser.ConfigParser()
    default.read_file(open(os.path.join(self.config_location, "default.cfg")))
    local = configparser.ConfigParser()
    local.read_file(open(filename))

    local_ok = True
    diff = set(local.sections()) - set(default.sections())
    for section in diff:
      logging.warning("Section {} does not exist in {}".format(section, "default.cfg"))
      local_ok = False
    for section in local.sections():
      if not default.has_section(section):
        continue
      diff = set(local.options(section)) - set(default.options(section))
      for option in diff:
        logging.warning("Option {} in section {} does not exist in {}".format(
            option, section, "default.cfg"))
        local_ok = False
    if local_ok:
      logging.info("{} is OK".format(filename))
    else:
      logging.warning("{} contains errors.".format(filename))
    return local_ok
