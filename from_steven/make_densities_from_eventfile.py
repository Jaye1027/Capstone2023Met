#!/usr/bin/python 

# plot_density_map(fTracks,fSave,aSave,track_length_min):

import numpy as np
import netCDF4
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from mpl_toolkits.basemap import Basemap
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
import datetime as dt

#import basinMetrics
#import correspond
#import helpers
#import my_settings
from mstats import *
import tpv_tracker_plotting_modules as tpvmod

r2d = 180./np.pi
###### General options#############################################

fTracks = '/data1/scavallo/data/seaice/seaice_loss_events/5percentile/sfccyclones_atimesofevents_5percentile_jja_1979010100_2014123118.dat'
aSave = '/data1/scavallo/data/seaice/seaice_loss_events/5percentile/density_array_events_wrfgrid_5percentile_jja_1979010100_2014123118.npz'


lat_origin_range = [30., 90.]
metric_min = -9999.
radius = 555000. #in meters
######Filter options##############################################
use_wrfgrid = True
gridpath = '/data2/scavallo/era_interim/track_files/wrf_arcticgrid.nc'
##################################################################
hinc = 6.0
R_earth = 6371200.
#R_earth = R_earth / 1000
pid = np.pi/180.

file = open(aSave, 'w+')


datain = np.loadtxt(fTracks, skiprows=1)       
nrows, ncols = np.shape(datain)

datelist = datain[:,0]
vortlat = datain[:,1]	
vortlon = datain[:,2]
print len(vortlat)

ntracks_tot = len(vortlat)
##################################################################
# Create new mesh for grids
##################################################################

latboxsize = 2
lonboxsize = 5

xlat = np.arange(30,90+(latboxsize/2),latboxsize)
xlon = np.arange(0,365,lonboxsize)

if ( use_wrfgrid == False ):
    xloni,xlati = np.meshgrid(xlon,xlat)
else:
    print 'Using WRF grid'
    nc = netCDF4.Dataset(gridpath,'r')
    xlati = nc.variables['XLAT'][0,:,:].squeeze()
    xloni = nc.variables['XLONG'][0,:,:].squeeze()
    [a,b] = np.where(xloni<0)
    xloni[a,b] = xloni[a,b] + 360.    
    nc.close 
    mstats(xloni)
    
    del xlat, xlon
    xlat = xlati
    xlon = xloni
    
##################################################################
# Create the tracks
##################################################################



if use_wrfgrid == False:
    den_arr = np.zeros([len(xlat),len(xlon)])
    count_arr = np.zeros([len(xlat),len(xlon)])
    hit_arr = np.zeros([len(xlat),len(xlon)])
    for ii in xrange(0,len(xlat)):
	for jj in xrange(0,len(xlon)):
            vortices = 0

	    print "Working on ii %d of %d" % (ii, len(xlat))

            for kk in xrange(0,len(vortlat)):
               # If using NETCDF, subtract 360 from any value greater than 180 in order to
               # use a longitude scale of -180-180 degrees (possibly not needed now due to radian conversion)
               #if (False):
               if vortlon[kk] < 0:
        	   vortlon[kk] = vortlon[kk] + 360

               #print vortlat[kk],vortlon[kk],xlat[ii],xlon[jj]
	       try:
		   distance = abs(tpvmod.rEarth*tpvmod.distance_on_unit_sphere(vortlat[kk],vortlon[kk],xlat[ii],xlon[jj]))
               except:
		   distance = 9999999999.

	       if distance <= radius:
		   vortices = vortices + 1

            den_arr[ii,jj] = den_arr[ii,jj] + vortices
	    if vortices > 0:
		hit_arr[ii,jj] = hit_arr[ii,jj] + 1
	    count_arr[ii,jj] = count_arr[ii,jj] + 1
 
else:
    ny,nx = np.shape(xlat)
    den_arr = np.zeros([ny,nx])
    count_arr = np.zeros([ny,nx])
    hit_arr = np.zeros([ny,nx])    
    for ii in xrange(0,nx-1):
	for jj in xrange(0,ny-1):
            vortices = 0
	    print "Working on ii %d of %d" % (ii, nx-1)
	    

            for kk in xrange(0,len(vortlat)):
        	# If using NETCDF, subtract 360 from any value greater than 180 in order to
        	# use a longitude scale of -180-180 degrees (possibly not needed now due to radian conversion)
        	#if (False):
        	if vortlon[kk] < 0:
        	    vortlon[kk] = vortlon[kk] + 360

        	#print vortlat[kk],vortlon[kk],xlat[ii],xlon[jj]
		try:
		    distance = abs(tpvmod.rEarth*tpvmod.distance_on_unit_sphere(vortlat[kk],vortlon[kk],xlat[jj,ii],xlon[jj,ii]))
        	except:
		    distance = 9999999999.

		if distance <= radius:
		    vortices = vortices + 1

            den_arr[jj,ii] = den_arr[jj,ii] + vortices
	    if vortices > 0:
		hit_arr[jj,ii] = hit_arr[jj,ii] + 1
	    count_arr[jj,ii] = count_arr[jj,ii] + 1

np.savez(file,den_arr=den_arr,hit_arr=hit_arr,count_arr=count_arr)
