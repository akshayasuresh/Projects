from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from yt.mods import *
from PIL import Image as im
import numpy as na
import h5py as h5
import sys, time
from Image import *
from _colormap_data import *
import random
angle = 0
spin = 0
ESCAPE = '\033'
GL_TEXTURE_RECTANGLE_ARB = 34037
#sets up initial camera position
camx, camy, camz = (0.0, 0.0, 0.0)
window = 0
#loads the data and stores it in different variables
fp = h5.File("enzo_tiny_cosmology/DD0029-star_colors.h5", "r") #enzo_tiny_cosmology/DD0017-star_colors.h5", "r")
x_pos = fp["x_pos"].value
y_pos = fp["y_pos"].value
z_pos = fp["z_pos"].value
fluxa = fp["fluxa"].value
mass = fp["mass"].value
#finds the number of stars
starnum = x_pos.shape[0]
#calculates min and max mass
maxmass = mass.max()
meanmass = mass.min()
#finds the difference in flux between two filters (B and V)
flux = fluxa[: ,2]-fluxa[:, 1]
#calculates min and max flux
maxflux = flux.max()
minflux = flux.min()

#sets up a class with position, flux, radius, and color bin attributes
class particle:
    def __init__(self):
       
        self.X= 0.0
        self.Y= 0.0
        self.Z= 0.0
        self.fluxa= 0.0
        self.rad= 0.0
        self.bin= 0.0
#creates the empty array "stars"        
stars=[]

#adds the class defined above to the array
for i in range(starnum):
    particl=particle()
    stars.append(particl)
#colors= [(0.0, 0.0, 1.0), (0.0, 0.25, 1.0), (0.0, 0.5, 1.0), (0.0, 0.75, 1.0), (0.0, 1.0, 1.0), (0.0, 1.0, 0.75), (0.0, 1.0, 0.5), (0.0, 1.0, 0.25), (0.0, 1.0, 0.0), (0.25, 1.0, 0.0), (0.5, 1.0, 0.0), (0.75, 1.0, 0.0), (1.0, 1.0, 0.0), (1.0, 0.75, 0.0), (1.0, 0.5, 0.0), (1.0, 0.25, 0.0), (1.0, 0.0, 0.0)]

#method to load the texture
def LoadTextures():
	global  texture, zPlane
        #opens the image
	image = open("texture2.bmp")
	yPlane= (1.0, 0.0, 0.0, 0.0)
        #defines the texture width and height as the image width and height
	ix = image.size[0]
	iy = image.size[1]
	image = image.tostring("raw", "RGBX", 0, -1)
	
	# Create Texture
	texture = glGenTextures(1)
	glBindTexture(GL_TEXTURE_2D, texture)
	
        #store texture 
	glPixelStorei(GL_UNPACK_ALIGNMENT,1)
	glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
	#glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
	#glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_R, GL_CLAMP)
	#glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
	#glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
	#glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
	#glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_NEAREST)
        #glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_EYE_LINEAR)
        #glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_EYE_LINEAR)
        #glTexGenfv(GL_S, GL_EYE_PLANE, yPlane)
        #glTexGenfv(GL_T, GL_EYE_PLANE, yPlane) 

        #allows the texture to blend with the colors of the star
	glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
        #creates mipmaps that allow for zooming in close to the image
	gluBuild2DMipmaps(GL_TEXTURE_2D, 3, ix, iy, GL_RGBA, GL_UNSIGNED_BYTE, image)

#defines the method for drawing a rectangle of the same dimensions as the texture
def DrawRect(origin, width, texture, texturewidth):

    glBindTexture(GL_TEXTURE_2D, texture);
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f(origin[0]-width[0], origin[1] - width[1], origin[2])
    glTexCoord2f(1, 0)
    glVertex3f(origin[0]+width[0], origin[1] - width[1], origin[2])
    glTexCoord2f(1, 1)
    glVertex3f(origin[0]+width[0], origin[1] + width[1], origin[2])
    glTexCoord2f(0, 1)
    glVertex3f(origin[0]-width[0], origin[1] + width[1], origin[2])
    glEnd()

#defines the method for intializing the OpenGL window
def InitGL(Width, Height):
    global quadratic, flux
    
    #loads textures
    LoadTextures()
    #allows for drawing of quadratics
    quadratic = gluNewQuadric()
    gluQuadricNormals(quadratic, GLU_SMOOTH)
    gluQuadricTexture(quadratic, GL_TRUE)
    #enables use of 2D textures
    glEnable(GL_TEXTURE_2D)
    #sets the background color of the window to black
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    #enables depth testing and draws all pixels no matter what depth (this is important so that stars located behind other stars are still drawn--otherwise only the stars in the front would contribute to the brightness)
    glDepthFunc(GL_ALWAYS)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    #glEnable(GL_LIGHTING)
    #glEnable(GL_LIGHT0)
    #adds flux, color, and radius data to the array for each star
    for i in range(starnum):
        stars[i]
        
        #flux is set to a range of [0,255]
        stars[i].fluxa= (((flux[i]-(-5.68360849461e-12))/((1.35207869063e-11)-(-5.68360849461e-12)))*255)

        #print stars[i].fluxa
        #flux values are sorted into an integer bin (these bins will later become the RGB values for each star)
        stars[i].bin= na.searchsorted([0, 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60, 61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,220,221,222,223,224,225,226,227,228,229,230,231,232,233,234,235,236,237,238,239,240,241,242,243,244,245,246,247,248,249,250,251,252,253,254,255], stars[i].fluxa, side= "left")
        #print stars[i].bin
        #adds the position data for each star, changing the ranges to be centered around the origin and pushing the image far enough back to be viewable
        stars[i].X = (x_pos[i]*10)-5
        stars[i].Y = (y_pos[i]*10)-5
        stars[i].Z = (z_pos[i]*10)-20
        
        #sets the radius based on a scale of the mass (the most massive stars will have the biggest radii and vice versa)
        stars[i].rad= ((mass[i]/meanmass)**0.5)/3000
        
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    #gluLookAt(0.0, 0.0, 15.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0)
    #sets the field of view
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    #allows for blending
    glEnable(GL_BLEND)
    glBlendFunc(GL_ONE, GL_ONE)
    #glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    #glLightfv(GL_LIGHT0, GL_AMBIENT, (0.5, 0.5, 0.5, 1.0))
    #glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
    #glLightfv(GL_LIGHT0, GL_POSITION, (0.0, 0.0, 2.0, 1.0))

#defines the method that is executed everytime the viewing window is resized
def ReSizeGLScene(Width, Height):
    if Height == 0:
        Height = 1
    glViewport(0, 0,  Width, Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    #gluLookAt(0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0)
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

#defines the method for drawing the actual scene
def DrawGLScene():
    global quadratic, texture, rsphe,DrawRect, Width, Height, camx, camy, camz
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    #sets up global rotation around the x and y axes
    glRotated(angle, 0.0, 1.0, 0.0)
    glRotated(spin, 1.0, 0.0, 0.0)
    #sets up movement of the camera in the x, y, and z directions
    glTranslatef(camx, camy, camz)
    t0 = time.time()
   
    #draws each star as a rectangle with width given by stars.rad, position given by stars.X, stars.Y, and stars.Z, and color given by stars.bin
    for i in range(starnum):
       
       #glBindTexture(GL_TEXTURE_2D, texture)
       #glTexCoord2d(0.50, 0.50); glVertex3f(stars[i].X, stars[i].Y, stars[i].Z)
       origin = (stars[i].X, stars[i].Y, stars[i].Z)
       width = (stars[i].rad,stars[i].rad,stars[i].rad)
       texturewidth = 128
       
       glColor4f(color_map_luts['RdBu'][0][stars[i].bin], color_map_luts['RdBu'][1][stars[i].bin], color_map_luts['RdBu'][2][stars[i].bin], 1.0)
       DrawRect(origin, width, texture, texturewidth)
       #gluSphere(quadratic, stars[i].rad, 32, 32)
    t1 = time.time()
    #print "Redraw time = %g" % (t1-t0)
    
    #swaps buffer so the drawn scene is displayed
    glutSwapBuffers()

#defines method for key presses
def keyPressed(key, x, y):
    global window, angle, spin, camx,camy, camz
    key = string.upper(key)
    time.sleep(0.01)
    #t0 = time.time()
    #escape key terminates the program
    if key == ESCAPE:
        sys.exit()
    #key specific to enzo_tiny_cosmology that automatically focuses on the biggest galaxy
    elif key == 'G':
        camz+=11.2
        spin+=10
        angle-=20
        camy-=1.6
        camx-=0.6
        print "G"
    #key specific to IsolatedGalaxy that automatically focuses on the galaxy
    elif key == 'R':
        camz+=14.89
        print "R"
    #zoom in
    elif key == 'Z':
        camz+=0.2
        print "Z"
    #zoom out
    elif key == 'X':
        camz-=0.2
        print "X"
    #rotates the camera view down
    elif key == 'W':
        camy-=0.2
        print "W"
    #rotates the camera view up
    elif key == 'S':
        camy+=0.2
        print "S"
    #rotates the camera view to the right 
    elif key == 'A':
        camx+=0.2
        print "A"
    #rotates the camera view to the left
    elif key == 'D':
        camx-=0.2
        print "D"
    #translates the image to the left
    elif key == 'J':
        angle+=10
        print "J"
        glutPostRedisplay()
    #translates the image to the right
    elif key == 'L':
        angle-=10
        print "L"
        glutPostRedisplay() 
    #translates the image up
    elif key == 'I':
        spin+=10
        print "I"
        glutPostRedisplay()
    #translates the image down
    elif key == 'K':
        spin-=10
        print "K"
        glutPostRedisplay()
    #takes a screenshot of the window and saves it as a PNG file
    elif key == 'P':
        glPixelStorei(GL_PACK_ALIGNMENT, 1)
        data = glReadPixels(0, 0, 800, 600, GL_RGBA, GL_UNSIGNED_BYTE)
        image = im.frombuffer("RGBA", (800, 600), data, 'raw', "RGBA", 0, 1)       
        image.show()
        image.save('Pic*26.png', 'PNG')
    #t1 = time.time()
    #print "Key pressed: time = %g" % (t1-t0)

#defines a method for mouse clicks
def mouse(button, state, clickx, clicky):
    #defines what happens for a left click
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            #finds the window width and height in pixels
            window_width = float(glutGet(GLUT_WINDOW_WIDTH))
            window_height = float(glutGet(GLUT_WINDOW_HEIGHT))
            #finds the position in pixels at the mouseclick
            posit = [clickx, (window_height - clicky)]
            #finds the position in codeunits at the mouseclick
            mod = glGetDoublev(GL_MODELVIEW_MATRIX)
            pro = glGetDoublev(GL_PROJECTION_MATRIX)
            vie = glGetIntegerv(GL_VIEWPORT)
            coord= gluUnProject(posit[0], posit[1], 0, model=mod, proj=pro, view=vie)
 
            #glReadPixels(x, window_height-y-1, 1, 1, GL_RGBA, GL_UNSIGNED_BYTE)
            #glReadPixels(x, window_height-y-1, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)
            #glReadPixels(x, window_height-y-1, 1, 1, GL_STENCIL_INDEX, GL_UNSIGNED_INT)
            
            
            print posit, window_width, window_height, coord
            
#the main method that calls of the other methods and makes the program run            
def main():
    global window
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    #sets the initial window size and position
    glutInitWindowSize(800, 600)
    glutInitWindowPosition(100,100)

    window = glutCreateWindow("Image")
    glutDisplayFunc(DrawGLScene)
    #glutFullScreen()
    glutIdleFunc(DrawGLScene)
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyPressed)
    glutMouseFunc(mouse)
    #glutSpecialFunc(specialKeyPressed)
    InitGL(640, 480)
    glutMainLoop()

main()
