# MessageListener

import time
import os
import re
import logging
from gi.repository import Clutter, Mx, Mash, Toggle, GLib

from Message import Message

class MessageListener:
    def __init__(self, config):
        self.config = config
        filename = config.get("System", "message_fd")
        self.file = None
        # Dirty hack since After=toggle.path does not work... 
        for i in range(1):
            if not os.path.exists(filename):    
                time.sleep(1)
        if not os.path.exists(filename):
            logging.warning("No file in path: " + filename)
            return
        self.file = os.open(filename, os.O_RDWR)
        logging.info("MessageListener listening on "+filename)        
        self.watch = GLib.io_add_watch(self.file, GLib.IO_IN, self.on_message_received)
        self.message = Message(config)

    def on_message_received(self, actor, event):    
        ''' Callback when a message from Redeem is coming in '''
        try: 
            text = self.readline_custom()
            if len(text)>0:      
                self.process_message(text)          
        except Exception as e:
            return False
        return True

    def process_message(self, msg):
        if msg == "ok":
            pass
        elif msg == "Heating done.":
            self.message.display(msg)
            self.config.printer.preheat_done()            
        elif "T:" in msg:
            m = re.search('^.*(T\:\d+).*(B\:\d+).*', msg) 
            if m:
                stat = m.group(1)+"/"+m.group(2)
                self.config.printer.set_status(stat)
        else:
            logging.debug("Got message: "+msg)
            self.message.display(msg)

    def readline_custom(self):
        message = ""
        while True:
            cur_char = os.read(self.file, 1)
            #Check for newline char    
            if (cur_char == '\n' or cur_char == ""):
                return message;
            message = message + cur_char


    def send(self, message):
        ''' Send a message to Redeem '''
        if self.file:
            if message[-1] != "\n":
                message += "\n"
            logging.debug("Sending: "+message)
            os.write(self.file, message)
        else:
            logging.debug("Discarding: "+message)
            
