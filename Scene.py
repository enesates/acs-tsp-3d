from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
from OpenGL.raw.GLUT import glutSolidSphere
import Acs

import threading
        
class Runner(threading.Thread):
    def __init__(self,s,c):
        threading.Thread.__init__(self)
        self.scene = s
        self.cities = c
        
    def run(self):
        Acs.start(self.scene, self.cities)
        

class City(object):
    def __init__(self, x, y, cityId):
        self.id = cityId
        self.coordinate = [x,y]

        
def createCities(cities, citiesCoordinatesX, citiesCoordinatesY ):
    citiesFile = open("djibouti38_optimal6656.tsp","r")
    
    for i in range(0,38):
        line = citiesFile.readline()
        line = line.strip()
        line = line.split(" ")
        cities.append(City(float(line[1]), float(line[2]), i))
        citiesCoordinatesX.append(float(line[1]))
        citiesCoordinatesY.append(float(line[2]))
        
    citiesFile.close()

class Scene(object):
    
    def __init__(self, citiesX, citiesY):
        self.citiesX = citiesX
        self.citiesY = citiesY
        self.normalize_columns(self.citiesX, self.citiesY)
        self.tour = []
        # Viewpoint
        self.camera = [0.5,0.5,1.5]
        self.bakilannokta = [0.5,0.5,-1.0]
        self.runScene()
        
    def updateTour(self,newTour):
        self.tour = newTour
        self.DrawGLScene()
    
    
    def LoadTextures(self):
       #global texture
       image = open("Data/lesson06/NeHe.bmp","r")
       
       ix = image.size[0]
       iy = image.size[1]
       image = image.tostring("raw", "RGBX", 0, -1)
       
      
       glPixelStorei(GL_UNPACK_ALIGNMENT,1)
       glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
       glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
       glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
       glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
       glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
       glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
       glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
       glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        
    
    def InitGL(self,Width, Height):        
        #self.LoadTextures()        
        glClearColor(0.0, 0.0, 0.0, 0.0)    
        glClearDepth(1.0)                   
        glDepthFunc(GL_LESS)                
        glEnable(GL_DEPTH_TEST)                
        glShadeModel(GL_SMOOTH)                
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()                   
                                           
        gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    
        glMatrixMode(GL_MODELVIEW)
    
    
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
        
        glColor3f(0,0,1)
        glBegin(GL_QUADS)                  
        glTexCoord2f(0.0, 0.0);glVertex3f(0, 1.0, 0.0)         
        glTexCoord2f(1.0, 0.0);glVertex3f(1.0, 1.0, 0.0)           
        glTexCoord2f(1.0, 1.0);glVertex3f(1.0, 0, 0.0)         
        glTexCoord2f(0.0, 1.0);glVertex3f(0, 0, 0.0)         
        glEnd()                            
    
    
        # Cities
        glColor3f(1,0.5,0)
        for i in range(len(self.citiesX)):
            glPushMatrix()
            glTranslatef(self.citiesX[i],self.citiesY[i],0)
            glutSolidSphere(0.005,10,10)
            glPopMatrix()
            
        # Drawing the best tour
        if(self.tour!=[]):
            tour = self.tour
            cityCount = len(self.tour)
            glColor3f(1,0,0)
            glLineWidth(3)
            glBegin(GL_LINES)
            for i in range(cityCount-1):
                currentCity = self.tour[i].id
                nextCity = self.tour[i+1].id
                glVertex3f(self.citiesX[currentCity], self.citiesY[currentCity], 0.01) # origin of the line
                glVertex3f(self.citiesX[nextCity], self.citiesY[nextCity], 0.01) # ending point of the line
            glVertex3f(self.citiesX[tour[cityCount-1].id], self.citiesY[tour[cityCount-1].id], 0.01) # origin of the line
            glVertex3f(self.citiesX[tour[0].id], self.citiesY[tour[0].id], 0.01) # ending point of the line
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
        
    def normalize_columns(self,X,Y):
        
        minX = min(X)
        minY = min(Y)
        maxX = max(X)-minX
        maxY = max(Y)-minY
        for i in range(0,len(X)):
            X[i] -= minX
            X[i] /= maxX
            Y[i] -= minY
            Y[i] /= maxY
        
    
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
    createCities(cities, citiesCoordinatesX, citiesCoordinatesY)
    scene = Scene(citiesCoordinatesX,citiesCoordinatesY)