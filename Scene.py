from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
from OpenGL.raw.GLUT import glutSolidSphere
import Acs
#from Image import *
import Image
#===============================================================================
# import threading
#        
#        
# class Runner(threading.Thread):
#    def __init__(self,s,c):
#        threading.Thread.__init__(self)
#        self.scene = s
#        self.cities = c
#        
#    def run(self):
#        Acs.start(self.scene, self.cities)
#===============================================================================
        

class City(object):
    def __init__(self, x, y, z, cityId):
        self.id = cityId
        self.coordinate = [x,y,z]

        
def createCities(cities, citiesCoordinatesX, citiesCoordinatesY, citiesCoordinatesZ ):
    
    citiesFile = open("djibouti38_optimal6656.tsp","r")
    
    for i in range(0,38):
        line = citiesFile.readline()
        line = line.strip()
        line = line.split(" ")
        cities.append(City(float(line[1]), float(line[2]), float(line[3]), i))
        citiesCoordinatesX.append(float(line[1]))
        citiesCoordinatesY.append(float(line[2]))
        citiesCoordinatesZ.append(float(line[3]))
        
    citiesFile.close()

class Scene(object):
    
    def __init__(self, citiesX, citiesY, citiesZ):
        self.citiesX = citiesX
        self.citiesY = citiesY        
        self.citiesZ = citiesZ
        self.normalize_columns(self.citiesX, self.citiesY, self.citiesZ)
        
        self.tour = []
        
        # Viewpoint
        self.camera = [-1.8,1.4,-3.5]
        self.bakilannokta = [0.2,0.2,-0.5]
        self.runScene()
        
        
    def updateTour(self,newTour):
        self.tour = newTour
        self.DrawGLScene()
     
    
    def InitGL(self,Width, Height):  
        glClearColor(0.0, 0.0, 0.0, 0.0)    
        glClearDepth(1.0)                   
        glDepthFunc(GL_LESS)                
        glEnable(GL_DEPTH_TEST)                
        glShadeModel(GL_SMOOTH)                
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()                   
                                           
        gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    
        glMatrixMode(GL_MODELVIEW)
        
        # setup blending
        glBlendFunc(GL_SRC_ALPHA,GL_ONE)            # Set The Blending Function For Translucency
        glColor4f(1.0, 1.0, 1.0, 0.5)
        
        glEnable(GL_BLEND)            # Turn Blending On
        glDisable(GL_DEPTH_TEST)         # Turn Depth Testing Off
    
    
    def ReSizeGLScene(self,Width, Height):
        if Height == 0:                       
            Height = 1
    
        glViewport(0, 0, Width, Height)        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
    
     
    def DrawGLScene(self):
       
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()                   
        gluLookAt(self.camera[0],self.camera[1],self.camera[2], 
                  self.bakilannokta[0],self.bakilannokta[1],self.bakilannokta[2],
                  0.0,1,0.0)
        
        #=======================================================================
        # glColor3f(0,0,1)
        # glBegin(GL_QUADS)                  
        # glTexCoord2f(0.0, 0.0);glVertex3f(0, 1.0, 0.0)         
        # glTexCoord2f(1.0, 0.0);glVertex3f(1.0, 1.0, 0.0)           
        # glTexCoord2f(1.0, 1.0);glVertex3f(1.0, 0, 0.0)         
        # glTexCoord2f(0.0, 1.0);glVertex3f(0, 0, 0.0)         
        # glEnd()                            
        #=======================================================================
    
       
        glBegin(GL_QUADS);
        glColor3f(0.2,0.4,0.0);
        glVertex3f(1.0,1.0,-1.0);
        glVertex3f(-1.0,1.0,-1.0);
        glVertex3f(-1.0,1.0,1.0);
        glVertex3f(1.0,1.0,1.0);
                
        glColor3f(0.2,0.4,0.0);
        glVertex3f(1.0,-1.0,1.0);
        glVertex3f(-1.0,-1.0,1.0);
        glVertex3f(-1.0,-1.0,-1.0);
        glVertex3f(1.0,-1.0,-1.0);
                
        glColor3f(0.0,0.2,0.4);
        glVertex3f(1.0,1.0,1.0);
        glVertex3f(-1.0,1.0,1.0);
        glVertex3f(-1.0,-1.0,1.0);
        glVertex3f(1.0,-1.0,1.0);
                
        glColor3f(0.0,0.2,0.4);
        glVertex3f(1.0,-1.0,-1.0);
        glVertex3f(-1.0,-1.0,-1.0);
        glVertex3f(-1.0,1.0,-1.0);
        glVertex3f(1.0,1.0,-1.0);
                
        glColor3f(0.4,0.0,0.2);
        glVertex3f(-1.0,1.0,1.0);
        glVertex3f(-1.0,1.0,-1.0);
        glVertex3f(-1.0,-1.0,-1.0);
        glVertex3f(-1.0,-1.0,1.0);
                
        glColor3f(0.4,0.0,0.2);
        glVertex3f(1.0,1.0,-1.0);
        glVertex3f(1.0,1.0,1.0);
        glVertex3f(1.0,-1.0,1.0);
        glVertex3f(1.0,-1.0,-1.0);
        glEnd()
    
        # Cities
        glColor3f(1.0,1.0,1.0)
        for i in range(len(self.citiesX)):
            glPushMatrix()
            glTranslatef(self.citiesX[i]-0.5,self.citiesY[i]-0.5, self.citiesZ[i])
            glutSolidSphere(0.005,10,10)
            glPopMatrix()
            
        # Drawing the best tour
        if(self.tour!=[]):
            tour = self.tour
            cityCount = len(self.tour)
            glColor3f(0.5, 0.1 ,0.3)
            glLineWidth(3)
            glBegin(GL_LINES)
            for i in range(cityCount-1):
                currentCity = self.tour[i].id
                nextCity = self.tour[i+1].id
                glVertex3f(self.citiesX[currentCity]-0.5, self.citiesY[currentCity]-0.5, self.citiesZ[currentCity]) # origin of the line
                glVertex3f(self.citiesX[nextCity]-0.5, self.citiesY[nextCity]-0.5, self.citiesZ[nextCity]) # ending point of the line
            glVertex3f(self.citiesX[tour[cityCount-1].id]-0.5, self.citiesY[tour[cityCount-1].id]-0.5, self.citiesZ[tour[cityCount-1].id]) # origin of the line
            glVertex3f(self.citiesX[tour[0].id]-0.5, self.citiesY[tour[0].id]-0.5, self.citiesZ[tour[0].id]) # ending point of the line
            glEnd()

        glutSwapBuffers()
    
    def keyPressed(self,*args):
        if args[0] == '\033':
            sys.exit()
        if args[0] == 's':
            self.updateTour([])
            Acs.start(self, cities)
            #th = Runner(self, cities)
            #th.start()
            
    def specialKeyPressed(self,key, x, y):
        if key == GLUT_KEY_PAGE_UP: # tilt up
            self.camera[2] -= 0.1
    
        elif key == GLUT_KEY_PAGE_DOWN: # tilt down
            self.camera[2] += 0.1
            
        elif key == GLUT_KEY_UP: # walk forward (bob head)
            self.camera[1]+=0.1
    
        elif key ==GLUT_KEY_DOWN: # walk back (bob head)
            self.camera[1]-=0.1
            
        elif key == GLUT_KEY_LEFT: # look left
            self.camera[0]-=0.1
    
        elif key == GLUT_KEY_RIGHT: # look right
            self.camera[0]+=0.1
            
        glutPostRedisplay()
        
    def normalize_columns(self, X, Y, Z):
        
        minX = min(X)
        minY = min(Y)
        minZ = min(Z)
        maxX = max(X)-minX
        maxY = max(Y)-minY
        maxZ = max(Z)-minZ
        
        for i in range(0,len(X)):
            X[i] -= minX
            X[i] /= maxX
            Y[i] -= minY
            Y[i] /= maxY
            Z[i] -= minZ
            Z[i] /= maxZ
        
    
    def runScene(self):
        glutInit(())
    
        
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
        
        glutInitWindowSize(500, 500)
        
      
        glutInitWindowPosition(0, 0)
        
        glutCreateWindow("Ant Colony System for TSP")
    
        glutDisplayFunc (self.DrawGLScene)
       
        glutIdleFunc(self.DrawGLScene)
        
        glutReshapeFunc (self.ReSizeGLScene)
       
        glutKeyboardFunc (self.keyPressed)
        glutSpecialFunc(self.specialKeyPressed)
    
       
        self.InitGL(500, 500)
    
           
        glutMainLoop()
        
if __name__ == "__main__":
    
    cities = []
    citiesCoordinatesX = []
    citiesCoordinatesY = []
    citiesCoordinatesZ = []
    
    createCities(cities, citiesCoordinatesX, citiesCoordinatesY, citiesCoordinatesZ)
    scene = Scene(citiesCoordinatesX, citiesCoordinatesY, citiesCoordinatesZ)
    
        