from yt.mods import *
import matplotlib.pyplot as plt
import numpy as na
from PIL import Image as im
import random
import h5py as h5
#loads the data
pf = load("Desktop/enzo_tiny_cosmology/DD0044/DD0044")
fp = h5.File("Desktop/enzo_tiny_cosmology/DD0044-star_colors.h5", "r")
#stores the flux values as a variable
fluxa = fp["fluxa"].value
#calculates flux as the difference between the flux in two filters (B and V)
flux = fluxa[:,2]-fluxa[:,1]
#calculates the total flux of the galaxy
totalflux = flux.sum()
limitingflux = 3.16228e-31
#print totalflux
#finds the current redshift at the time step and sets it as the variable "cr"
cr = na.absolute(pf["CosmologyCurrentRedshift"])
#the Hubble Constant with the Mpc to kilometer conversion factor
H0 = 70.0 / 3.086e19
#sets up all of the divisions for na.trapz (1000 divisions in the range [0,cr])
z = na.linspace(0,cr,1000)
#define the function to be integrated
Ez = (0.26 * (1+z)**3 + 0.74)**0.5
integrand = 1.0 / (1+z) / Ez

#integrates by the trapezoidal rule to find the lookback time in seconds 
t = na.zeros(1000)
t = na.trapz(integrand, z) / H0 
#calculates the distance in kilometers as lookback time multiplied by the speed of light
d = (3.0e+05)* t
x = ((0.05481426287244423+0.054814262872444244)*(9.87418e+20))/(1+cr)
y = ((0.04086906987916651+0.04114521224321493)*(9.87418e+20))/(1+cr)
#next three lines would be used to find the distance given by equating the spatial resolution of the image with the spatial resolution of HST (where the spatial resolution of HST is equal to the angular resolution of HST multiplied by the distance)
#dtheta = 2.0847e-07
#spatialresolution = (0.1*0.785398)/600
#d = (spatialresolution/dtheta) * (9.87418e+20) #distance in kilometers
#distance in kilometers if the distance is manually set
#d = (3.08568025e+23)

#calculates the flux from the galaxy that could be observed
obsflux = totalflux/((d/(3.08568025e+14))**2)
#calculates the ratio between the sensitivity of Hubble and the total observable flux and sets it to the range [0,256]
fluctuation = (na.absolute(limitingflux/obsflux))*256

#calculates the angular diameter in the x and y directions in degrees
imagewidthx = na.arctan(x/d)
imagewidthy = na.arctan(y/d)

#calculates the pixel dimensions based on the imagewidths and the angular resolution of HST and sets the max dimensions as 800 by 600
pixx = min(800,na.absolute(int((imagewidthx*3600.0)/0.043)))
pixy = min(600,na.absolute(int((imagewidthy*3600.0)/0.043)))
print pixx, pixy
#loads the original image as a variable
original= im.open("Desktop/Pic*44.png")
#resizes the image
rsize = original.resize((pixx,pixy))
#sets the image as an array
rsizeArr = na.asarray(rsize)
#changes the array to int format
rsizeArrNoise = rsizeArr.astype("int")
#adds the fluctuation to the array
for i in range (3):
    rsizeArrNoise[:,:, i] += na.random.random_integers(-1*fluctuation,fluctuation, size= (pixy, pixx))
    rsizeArrNoise[:, :, i] = na.maximum(rsizeArrNoise[:, : , i],0)
#changes the array back to the uint8 format
rsizeArrNoise = rsizeArrNoise.astype("uint8")
#plots the array with the noise
imgplot = plt.imshow(rsizeArrNoise)
#interpolation set to nearest to maintain the pixelated look
imgplot.set_interpolation('nearest')
#turns of the axes
plt.axis("off")
#saves the image as a PNG file and limits the amount of white margin
plt.savefig("44usingRedshiftData.png", bbox_inches= "tight", pad_inches=-0.1)
