#!/usr/bin/env python
'''
This provides a scripted update of a core service of the 3D Printer

It is meant to be executed from the command line as "update-toggle"
By doing so, the command will transfer into the appropriate virtual environment
and perform its actions there.

 *** Attempting to run the command by other methods such as executing `python updater.py`    ***
 *** is highly discouraged. Doing so, without following proper virtual environment protocols ***
 *** will not produce the desired result and is VERY LIKELY to CREATE AN NON-WORKING SYSTEM  ***
'''

import os
import subprocess
import getopt
import sys
from six import PY3

# the_service_name = 'toggle'


def switch_to_source_directory():
  # We assume that this file is located in the top level of the repository
  # and located within ${VIRTUAL_ENV}/src/${service_name}/
  # virtual env is two directories up
  this_dir = os.path.dirname(os.path.realpath(os.path.abspath(__file__)))
  venv_base = os.path.normpath(os.path.join(this_dir, "..", '..'))
  bin_dir = os.path.join(venv_base, 'bin')
  os.environ["PATH"] = os.pathsep.join([bin_dir] + os.environ.get("PATH", "").split(os.pathsep))
  os.environ["VIRTUAL_ENV"] = venv_base
  os.chdir(this_dir)
  the_service_name = os.path.basename(this_dir)
  print("Working in virtual environment {}".format(os.path.basename(venv_base)))
  return the_service_name


def is_service_running(name):
  with open(os.devnull, 'wb') as hide_output:
    exit_code = subprocess.Popen(['sudo', 'service', name, 'status'],
                                 stdout=hide_output,
                                 stderr=hide_output).wait()
    return exit_code == 0


def start_service(name):
  print("Start the {} service".format(name))
  command = ["sudo", "/bin/systemctl", "restart", name]
  with open(os.devnull, 'wb') as hide_output:
    try:
      p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=hide_output)
    except:
      print("Error restarting")

  stdout = p.communicate()[0].strip()
  if PY3:
    stdout = stdout.decode()
  exit_code = p.returncode
  if exit_code != 0:
    print("Restart of %s failed with return code %d" % (name, p.returncode))
  print(stdout)
  return exit_code == 0


def stop_service(name):
  print("Stop the {} service".format(name))
  command = ["sudo", "/bin/systemctl", "stop", name]
  with open(os.devnull, 'wb') as hide_output:
    try:
      p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=hide_output)
    except:
      print("Error stopping")

  stdout = p.communicate()[0].strip()
  if PY3:
    stdout = stdout.decode()
  exit_code = p.returncode
  if exit_code != 0:
    print("Stop of %s failed with return code %d" % (name, p.returncode))
  print(stdout)
  return exit_code == 0


def perform_git_command(command):
  command_str = " ".join(command)
  print("Performing " + command_str)

  with open(os.devnull, 'wb') as hide_output:
    try:
      p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=hide_output)
    except:
      print("Error running \"{}\"".format(command_str))

  stdout = p.communicate()[0].strip()
  if PY3:
    stdout = stdout.decode()
  exit_code = p.returncode
  if exit_code != 0:
    print("\"{}\" failed with return code {}".format(command_str, p.returncode))
  print(stdout)
  return exit_code == 0


def reinstall(name):
  print("Run setup")
  command = ['python', 'setup.py', 'develop']
  with open(os.devnull, 'wb') as hide_output:
    try:
      p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=hide_output)
    except:
      print("Error running \"setup\"")

  stdout = p.communicate()[0].strip()
  if PY3:
    stdout = stdout.decode()
  exit_code = p.returncode
  if exit_code != 0:
    print("Installation of %s failed with return code %d" % (name, p.returncode))
  print(stdout)
  return exit_code == 0


def perform_update():
  try:
    opts, args = getopt.getopt(sys.argv[1:], '-t', ['tag'])
  except getopt.GetoptError as err:
    print(str(err))
    print("./updater.py [--tag <tag name>]")
    sys.exit(2)
  service_name = switch_to_source_directory()
  service_was_running = is_service_running(service_name)
  if service_was_running:
    stop_service(service_name)
  if len(args) == 1:
    tag = args[0]
    perform_git_command(["git", "fetch", "--tags"])
    perform_git_command(["git", "checkout", "-b", "version-" + tag, "tags/" + tag])
  else:
    perform_git_command(["git", "pull"])
  reinstall(service_name)
  if service_was_running:
    start_service(service_name)
  print("Update of %s complete" % (service_name))


if __name__ == '__main__':
  perform_update()
