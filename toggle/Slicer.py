# Slicer

class Slicer:

    def __init__(self, stl_filename):
        self.stl_filename = stl_filename
    
    def run(self):
        """ Start slicing the model using the 
        current settings """
        cura_path = "/usr/src/cura/cura.sh"
        cura_config = "/etc/cura/CuraConfig.ini"
        stl_path = "/usr/share/models/stl/"+self.stl_filename
        gcode_path = "/usr/share/models/stl/"+self.stl_filename.replace(".stl", ".gcode")
        args = [cura_path, '-i', cura_config, '-s', stl_path, '-o', gcode_path]
        try:
            subprocess.check_call(args)
        except IOError as e:
            print e

