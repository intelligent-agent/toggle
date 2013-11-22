import wx
import sys
import time
from wx import glcanvas
from OpenGL.GL import *
from OpenGL.GLU import *
#from OpenGL.GLUT import *

#----------------------------------------------------------------------

buttonDefs = {
    wx.NewId() : ('CubeCanvas',      'Cube'),
    wx.NewId() : ('ConeCanvas',      'Cone'),
    }

class TextPanel1(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.SetBackgroundColour('white')
        self.SetSize((375, 50))
        
    def OnPaint(self, e):
        dc = wx.PaintDC(self)
        dc.SetPen(wx.Pen('#000000', 2, wx.SOLID))
        #dc.SetBrush(wx.Brush('#000000', 2, wx.SOLID))
        dc.DrawPolygon( [(10, 35), (10, 25), (5, 25), (15, 15), (25, 25), (20, 25), (20, 35), (16,35), (16,30), (14,30), (14,35)] )
        #dc.DrawPolygon( [(0, 20), (0, 10), (10, 10), (10, 20)] )
        dc.DrawText('Browse', 60, 15)
        dc.DrawText('Prepare', 160, 15)
        dc.DrawText('Operate', 270, 15)

class TextPanel2(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
      
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.SetBackgroundColour('white')
        self.SetSize((375, 50))
        
    def OnPaint(self, e):
        dc = wx.PaintDC(self)
        dc.SetPen(wx.Pen('#000000', 2, wx.SOLID))
        dc.DrawText('Tinker', 310, 10)
        

class TextPanel3(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
      
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.SetBackgroundColour('white')
        self.SetSize((375, 50))
        
    def OnPaint(self, e):
        dc = wx.PaintDC(self)
        dc.SetPen(wx.Pen('#000000', 2, wx.SOLID))
        dc.DrawText('Place', 40, 15)
        dc.DrawText('Rig', 120, 15)
        dc.DrawText('Slice', 200, 15)
        dc.DrawText('Print', 280, 15)


class ButtonPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
      
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftMouseUp)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftMouseDown)
        
        self.SetBackgroundColour('white')
        self.SetSize((375, 300))
        
    def OnPaint(self, e):
        dc = wx.PaintDC(self)
        dc.SetPen(wx.Pen('#000000', 1, wx.SOLID))
        dc.DrawRectangle(40, 210, 130, 40)
        dc.DrawRectangle(180, 210, 130, 40)
        dc.DrawRectangle(40, 260, 130, 40)
        dc.DrawRectangle(180, 260, 130, 40)
        
        dc.DrawText('Top View', 50, 220)
        dc.DrawText('Side View', 190, 220)
        dc.DrawText('Auto place: Off', 50, 270)
        dc.DrawText('Snap to grid: On', 190, 270)

    def OnLeftMouseDown(self, e):   
        pass

    def OnLeftMouseUp(self, e):
        x, y = e.GetPositionTuple()
        print "Mouse up on x:" + str(x) + " and y: " + str(y)
        
        
class MainPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)

        self.mainbox = wx.BoxSizer(wx.HORIZONTAL)
        self.box1 = wx.BoxSizer(wx.VERTICAL)
        self.box2 = wx.BoxSizer(wx.VERTICAL)
        
        txtpanel1 = TextPanel1(self)
        self.box1.Add(txtpanel1, 0, wx.ALIGN_CENTER|wx.ALL, 15)
        
        txtpanel2 = TextPanel2(self)
        self.box2.Add(txtpanel2, 0, wx.ALIGN_CENTER|wx.ALL, 15)
        
        txtpanel3 = TextPanel3(self)
        self.box2.Add(txtpanel3, 0, wx.ALIGN_CENTER|wx.ALL, 15)

        
        btnpanel = ButtonPanel(self)
        self.box2.Add(btnpanel, 0, wx.ALIGN_CENTER|wx.ALL, 15)
        
        self.SetBackgroundColour('white')
        
        #Create OpenGL canvas
        self.c = CubeCanvas(self)
        self.c.SetSize((375,375))
        #c.SetMinSize((200, 200))
        self.box1.Add(self.c, 0, wx.ALIGN_CENTER|wx.ALL, 15)

        self.SetAutoLayout(True)
        
        self.mainbox.Add(self.box1, 0, wx.ALIGN_CENTER|wx.ALL, 0)
        self.mainbox.Add(self.box2, 0, wx.ALIGN_CENTER|wx.ALL, 0)
        self.SetSizer(self.mainbox)


class MyCanvasBase(glcanvas.GLCanvas):
    zoomsteps = 0;
    
    def __init__(self, parent):
        #glcanvas.GLCanvas.__init__(self, parent, -1)
        glcanvas.GLCanvas.__init__(self, parent,-1, attribList=[wx.glcanvas.WX_GL_DOUBLEBUFFER])
        self.init = False
        self.context = glcanvas.GLContext(self)
        
        # initial mouse position
        self.lastx = self.x = 30
        self.lasty = self.y = 30
        self.size = self.GetSize()
        
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)
        self.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)
        

    def OnEraseBackground(self, event):
        pass # Do nothing, to avoid flashing on MSW.

    def OnSize(self, event):
        wx.CallAfter(self.DoSetViewport)
        event.Skip()

    def DoSetViewport(self):
        size = self.size = self.GetSize()
        self.SetCurrent(self.context)
        #self.SetCurrent()
        glViewport(0, 0, size.width, size.height)
        
    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        #self.SetCurrent(self.context)
        self.SetCurrent()
        if not self.init:
            self.InitGL()
            self.init = True
        self.OnDraw()

    def OnMouseDown(self, evt):
        self.CaptureMouse()
        self.x, self.y = self.lastx, self.lasty = evt.GetPosition()

    def OnMouseUp(self, evt):
        self.ReleaseMouse()

    def OnMouseMotion(self, evt):
        if evt.Dragging() and evt.LeftIsDown():
            self.lastx, self.lasty = self.x, self.y
            self.x, self.y = evt.GetPosition()
            self.Refresh(False)
    
    def OnMouseWheel(self, evt):
        self.zoomsteps += evt.GetWheelRotation() / evt.GetWheelDelta()
        #print self.zoomsteps
        self.Refresh(False)
        

class CubeCanvas(MyCanvasBase):
    xrot = 0.0
    yrot = 0.0 
    
    def InitGL(self):
    
        #Setup light
        LightAmbient = [ 0.7, 0.7, 0.7, 1.0]                # Ambient Light Values ( NEW )
        LightDiffuse = [ 1.0, 1.0, 1.0, 1.0]                # Diffuse Light Values ( NEW )
        LightPosition = [ 0.0, 0.0, 1.0, 1.0]               # Light Position ( NEW )
        glLightfv(GL_LIGHT1, GL_AMBIENT, LightAmbient)      # Setup The Ambient Light
        glLightfv(GL_LIGHT1, GL_DIFFUSE, LightDiffuse)      # Setup The Diffuse Light
        glLightfv(GL_LIGHT1, GL_POSITION,LightPosition)     # Position The Light
        glEnable(GL_LIGHT1)                                 # Enable Light One
        glEnable(GL_LIGHTING)                               # Enable Lighting In General

        glClearColor(1.0, 1.0, 1.0, 1.0)	# This Will Clear The Background Color To White
        glClearDepth(1.0)					# Enables Clearing Of The Depth Buffer
        glDepthFunc(GL_LESS)				# The Type Of Depth Test To Do
        glEnable(GL_DEPTH_TEST)				# Enables Depth Testing
        glShadeModel(GL_SMOOTH)				# Enables Smooth Color Shading

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()					# Reset The Projection Matrix
        
        # Calculate The Aspect Ratio Of The Window
        gluPerspective(45.0, 1.0, 0.1, 300.0)

        glMatrixMode(GL_MODELVIEW)

        # LOAD OBJECT
        self.obj = OBJ('Moose_thin.obj', swapyz=True)
       
        
        

    def OnDraw(self):
	    # Clear The Screen And The Depth Buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()					# Reset The View 

        glTranslatef(0.0, 0.0, self.zoomsteps*10 - 100.0)
        glRotate(-90, 1, 0, 0)
        #glRotate(45, 0, 1, 1)
        
        width, height = self.GetSize()
        self.xrot += float(self.x - self.lastx) / width
        self.yrot += float(self.y - self.lasty) / height
        
        #Rotate
        glRotate(self.xrot * 90, 0, 0, 1)
        glRotate(self.yrot * 90, 1, 0, 0)	
        
                
        glCallList(self.obj.gl_list)

        glFlush()
        #  since this is double buffered, swap the buffers to display what just got drawn. 
        self.SwapBuffers()



#----------------------------------------------------------------------
def MTL(filename):
    contents = {}
    mtl = None
    for line in open(filename, "r"):
        if line.startswith('#'): continue
        values = line.split()
        if not values: continue
        if values[0] == 'newmtl':
            mtl = contents[values[1]] = {}
        elif mtl is None:
            raise ValueError, "mtl file doesn't start with newmtl stmt"
        elif values[0] == 'map_Kd':
            # load the texture referred to by this declaration
            mtl[values[0]] = values[1]
            surf = pygame.image.load(mtl['map_Kd'])
            image = pygame.image.tostring(surf, 'RGBA', 1)
            ix, iy = surf.get_rect().size
            texid = mtl['texture_Kd'] = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texid)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
                GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
                GL_LINEAR)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA,
                GL_UNSIGNED_BYTE, image)
        else:
            mtl[values[0]] = map(float, values[1:])
    return contents
    

class OBJ:
    def __init__(self, filename, swapyz=False):
        """Loads a Wavefront OBJ file. """
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []
 
        material = None
        for line in open(filename, "r"):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue
            if values[0] == 'v':
                v = map(float, values[1:4])
                if swapyz:
                    v = v[0], v[2], v[1]
                self.vertices.append(v)
            elif values[0] == 'vn':
                v = map(float, values[1:4])
                if swapyz:
                    v = v[0], v[2], v[1]
                self.normals.append(v)
            elif values[0] == 'vt':
                self.texcoords.append(map(float, values[1:3]))
            elif values[0] in ('usemtl', 'usemat'):
                material = values[1]
            elif values[0] == 'mtllib':
                self.mtl = MTL(values[1])
            elif values[0] == 'f':
                face = []
                texcoords = []
                norms = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        texcoords.append(int(w[1]))
                    else:
                        texcoords.append(0)
                    if len(w) >= 3 and len(w[2]) > 0:
                        norms.append(int(w[2]))
                    else:
                        norms.append(0)
                self.faces.append((face, norms, texcoords, material))
 
        self.gl_list = glGenLists(1)
        glNewList(self.gl_list, GL_COMPILE)
        glEnable(GL_TEXTURE_2D)
        glFrontFace(GL_CCW)
        for face in self.faces:
            vertices, normals, texture_coords, material = face
 
            mtl = self.mtl[material]
            if 'texture_Kd' in mtl:
                # use diffuse texmap
                glBindTexture(GL_TEXTURE_2D, mtl['texture_Kd'])
            else:
                # just use diffuse colour
                glColor3f(1.0, 0.0, 0.0)
 
            glBegin(GL_POLYGON)
            for i in range(len(vertices)):
                if normals[i] > 0:
                    glNormal3fv(self.normals[normals[i] - 1])
                if texture_coords[i] > 0:
                    glTexCoord2fv(self.texcoords[texture_coords[i] - 1])
                glVertex3fv(self.vertices[vertices[i] - 1])
            glEnd()
        glDisable(GL_TEXTURE_2D)
        glEndList()
        
        
        
        
#----------------------------------------------------------------------
class RunDemoApp(wx.App):
    
    def __init__(self):
        wx.App.__init__(self, redirect=False)

    def OnInit(self):
        self.frame = wx.Frame(None, -1, "Toggler", style=wx.DEFAULT_FRAME_STYLE, name="Toggler", size=(800, 480))

        self.frame.Show(True)
        self.frame.Bind(wx.EVT_CLOSE, self.OnCloseFrame)

        #Add content to app
        win = MainPanel(self.frame)
        self.SetTopWindow(self.frame)
        self.frame.Maximize(True)
        return True

        
    def OnExitApp(self, evt):
        self.frame.Close(True)

    def OnCloseFrame(self, evt):
        if hasattr(self, "window") and hasattr(self.window, "ShutdownDemo"):
            self.window.ShutdownDemo()
        evt.Skip()
    
    def Refresh(self):
        self.frame.Refresh()

app = RunDemoApp()
app.MainLoop()
