#!/usr/bin/env python

import os
import subprocess

service_name = 'toggle'


def switch_to_src_directory():
  # assemble the path to the source directory
  this_dir = os.path.dirname(os.path.realpath(os.path.abspath(__file__)))
  source_location = os.path.normpath(os.path.join(this_dir, "."))
  os.chdir(source_location)


def is_service_running(name):
  with open(os.devnull, 'wb') as hide_output:
    exit_code = subprocess.Popen(['sudo', 'service', name, 'status'],
                                 stdout=hide_output,
                                 stderr=hide_output).wait()
    return exit_code == 0


def start_service(name):
  print("Start the {} service".format(name))
  with open(os.devnull, 'wb') as hide_output:
    exit_code = subprocess.Popen(['sudo', 'service', name, 'start'],
                                 stdout=hide_output,
                                 stderr=hide_output).wait()
    return exit_code == 0


def stop_service(name):
  print("Stop the {} service".format(name))
  with open(os.devnull, 'wb') as hide_output:
    exit_code = subprocess.Popen(['sudo', 'service', name, 'stop'],
                                 stdout=hide_output,
                                 stderr=hide_output).wait()
    return exit_code == 0


def perform_git_update():
  print("Do git update here")
  with open(os.devnull, 'wb') as hide_output:
    exit_code = subprocess.Popen(['git', 'pull'], stdout=hide_output, stderr=hide_output).wait()
    return exit_code == 0


def reinstall():
  print("Run setup")
  with open(os.devnull, 'wb') as hide_output:
    exit_code = subprocess.Popen(['python', 'setup.py', 'develop'],
                                 stdout=hide_output,
                                 stderr=hide_output).wait()
    return exit_code == 0


def perform_update():
  switch_to_src_directory()
  service_was_running = is_service_running(service_name)
  if service_was_running:
    stop_service(service_name)
  perform_git_update()
  reinstall()
  if service_was_running:
    start_service(service_name)
  print("Update complete")


if __name__ == '__main__':
  perform_update()
