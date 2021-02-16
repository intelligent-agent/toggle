import logging
import os
import json


# A Local update, when added to the queue, is executed by adding it
# with GLib.idle_add
class PushUpdate:
  def __init__(self, update_type, payload):
    self.update_type = update_type
    self.payload = payload
    # Set to True in the instance
    # to run a function in the queue thread first.
    self.has_thread_execution = False

  def execute(self, config):
    self.config = config
    if hasattr(self, self.update_type):
      #logging.debug("Got PushUpdate "+self.update_type+": "+str(self.payload))
      getattr(self, self.update_type)()
    else:
      print("missing function " + str(self.update_type))

  def execute_in_thread(self, config):
    self.config = config
    if hasattr(self, "thread_" + self.update_type):
      #logging.debug("Got PushUpdate with thread exeution "+self.update_type+": "+str(self.payload))
      getattr(self, "thread_" + self.update_type)()
    else:
      print("missing function thread_" + str(self.update_type))

  def connected(self):
    self.config.printer.set_status("Connected")
    self.config.splash.set_status("Connected!")
    self.config.tabs.to_side_2()

  def history(self):
    for temp in self.payload["temps"]:
      self.config.temp_graph.update_temperatures(temp)
    self.config.printer.update_printer_state(self.payload["state"])
    filename = self.payload["job"]["file"]["name"]
    if filename:
      self.config.loader.select_model_by_filename(filename)

  def timelapse(self):
    pass

  def plugin(self):
    plugin_name = self.payload["plugin"]
    if plugin_name == "redeem":
      plugin_type = self.payload["data"]["type"]
      if plugin_type == "filament_sensor":
        logging.warning("filament sensor has been disabled")
      elif plugin_type == "alarm_filament_jam":
        self.config.message.display("Alarm: Filament Jam!")
      elif plugin_type == "display_message":
        message = plugin_data["message"]
        self.config.message.display(message)
      elif plugin_type == "bed_probe_point":
        point = json.loads(plugin_data["message"])
        self.config.plate.add_probe_point(point)
        self.config.loader.select_none()
      elif plugin_type == "bed_probe_reset":
        self.config.plate.remove_probe_points()
        self.config.loader.model.show()
    elif plugin_name == "klipper":
      plugin_type = self.payload["data"]["type"]
      if plugin_type == "status":
        status = self.payload["data"]["payload"]
        logging.debug(f"Kipper status: {status}")
    else:
      logging.debug("Unknown plugin: " + str(plugin_name))

  def current(self):
    self.config.printer.update_printer_state(self.payload["state"])
    for temp in self.payload["temps"]:
      self.config.temp_graph.update_temperatures(temp)
      self.config.temp_graph.update_temperature_status(temp)
    self.config.printer.update_progress(self.payload["progress"])

  def event(self):
    evt_type = self.payload["type"]
    payload = self.payload["payload"]
    e = Event(self.config, evt_type, payload)

  def slicingProgress(self):
    prog = self.payload["progress"]
    self.config.message.update("Slicing progress: {}%".format(prog))

  def state(self):
    print("Got state!")

  def select_model(self):
    pass

  # Call the rest client function from the queue thread,
  # To enable the loading animation.
  def thread_select_model(self):
    self.config.rest_client.select_file(self.payload)


class Event:
  def __init__(self, config, evt_type, payload):
    self.config = config
    self.payload = payload
    if hasattr(self, evt_type):
      getattr(self, evt_type)()
    else:
      print("missing event function " + str(evt_type))

  def FileSelected(self):
    self.config.loader.select_model_by_filename(self.payload["name"])

  def FileDeselected(self):
    logging.debug("Deselected " + self.payload["name"])
    filename = os.path.splitext(self.payload["name"])[0] + ".stl"
    # config.loader.select_model(filename)

  def UpdatedFiles(self):
    logging.debug("Updated files")

  def Upload(self):
    logging.debug("Upload evt")
    self.config.loader.sync_models()

  def Disconnected(self):
    logging.debug("Printer Disconnected")

  def Connected(self):
    logging.debug("Printer Connected")

  def ClientOpened(self):
    logging.debug("Client Opened")

  def ClientClosed(self):
    logging.debug("Client Closed")

  def ClientAuthed(self):
    logging.debug("Client Authenticated")

  def SlicingStarted(self):
    self.config.message.display("Starting slicing!")

  def SlicingDone(self):
    self.config.message.display("Slicing done!")

  def ZChange(self):
    pass

  def MetadataStatisticsUpdated(self):
    pass

  def PrintDone(self):
    pass

  def PrintStarted(self):
    pass

  def PrintCancelled(self):
    pass

  def PrintFailed(self):
    pass

  def Home(self):
    pass

  def RegisteredMessageReceived(self):
    pass
