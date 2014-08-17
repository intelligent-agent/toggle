# Slicer

class Slicer:

    def __init__(self):
        pass
        
    
    
    def run(self):
        """ Start slicing the model using the 
        current settings """        
        subprocess.call(["CuraEngine", "-l"])
