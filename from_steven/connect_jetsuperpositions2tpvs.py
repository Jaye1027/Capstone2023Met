# connect_jetsuperpostions2tpvs.py
# Steven Cavallo
# November 2023

#####Imports##############################
# imports
import os
import conda

conda_file_dir = conda.__file__
conda_dir = conda_file_dir.split('lib')[0]
proj_lib = os.path.join(os.path.join(conda_dir, 'share'), 'proj')
os.environ["PROJ_LIB"] = proj_lib
import netCDF4
import csv

import numpy as np
import weather_modules as wm
from mstats import *
import utilities_modules as um
#####User Inupts##########################
#mm_prefix = ''
mm_prefix = ''

#Jet superposition events near TPV tracks: track count / total tracks / percentage
#22 / 327 /  6.73
#TPV tracks near jet superpositions: track count / total tracks / percentage
#23 / 5238 /  0.44

#track_file1 = '/data2/scavallo/jet_superpositions/JetSuperpositions_all.txt'
track_file1 = '/data2/scavallo/jet_superpositions/JetSuperpositions_PolarDominant.txt'
track_file2 = '/data2/scavallo/ERA5/tpv_tracks/tracks_low_horizPlusVert_60Ngen_' + mm_prefix + 'withids_1979-2021.txt'


fpath_out1a = '/data2/scavallo/jet_superpositions/superposition_event_matches_PolarDominant.dat'
fpath_out1b = '/data2/scavallo/jet_superpositions/superpostion_event_nonmatches_PolarDominant.dat'
fpath_out2a = '/data2/scavallo/jet_superpositions/superposition_tpv_matches_PolarDominant.dat'
fpath_out2b = '/data2/scavallo/jet_superpositions/superposition_tpv_nonmatches_PolarDominant.dat'

datestart = '1979010100'
dateend = '2010123118'
hinc = 6

climate_anomaly_option = False
tpv_labels = 'True'
search_dist_thresh = 1000. # km


###############################
# Load track files
###############################
fpath = track_file1
f = open(fpath,'r')

years_jet = []
months_jet = []
days_jet = []
hours_jet = []
latitude_jet = []
longitude_jet = []
with open(fpath,'r'):
    r = csv.reader(f,delimiter=',')
    for ii, data in enumerate(r):
        if ii == 0:
            pass
        else:
            years_jet.append(str(data[0]))
            months_jet.append(str(data[1]))	    
            days_jet.append(str(data[2]))
            hours_jet.append(str(data[3]))
            latitude_jet.append(float(data[4]))
            longitude_jet.append(float(data[5]))	    
  
years_jet = np.array(years_jet).astype('float')
months_jet = np.array(months_jet).astype('float')
days_jet = np.array(days_jet).astype('float')
hours_jet = np.array(hours_jet).astype('float')
latitude_jet = np.array(latitude_jet).astype('float')
longitude_jet = np.array(longitude_jet).astype('float')

dates_jet = []
for ii in range(0,len(years_jet)):
    yrnow = (int(years_jet[ii]))
    monthnow = (int(months_jet[ii]))
    daynow = (int(days_jet[ii]))
    hournow = (int(hours_jet[ii]))    

    if monthnow < 10:
        monthstr = '0'+ str(monthnow)
    else:
        monthstr = str(monthnow)
    
    if daynow < 10:
        daystr = '0'+ str(daynow)
    else:
        daystr = str(daynow)
    
    if hournow == 1:
        hourstr = '00'
    elif hournow == 2:
        hourstr = '06'
    elif hournow == 3:
        hourstr = '12'    
    else:
        hourstr = '18'

    dates_jet.append(str(yrnow)+monthstr+daystr+hourstr) 

datelist_sfc = np.array(dates_jet).astype('int')


fpath = track_file2
bb = np.loadtxt(fpath, skiprows=1) 
datelist = bb[:,0]

if tpv_labels == 'False':
    outfile1a = open(fpath_out1a,'w')
    outfile1a.write('date lat lon')
    outfile1a.write('\n')

    outfile1b = open(fpath_out1b,'w')
    outfile1b.write('date lat lon')
    outfile1b.write('\n')

    outfile2a = open(fpath_out2a,'w')
    outfile2a.write('date lat lon thetamin amplitude circulation radius')
    outfile2a.write('\n')

    outfile2b = open(fpath_out2b,'w')
    outfile2b.write('date lat lon thetamin amplitude circulation radius')
    outfile2b.write('\n')
else:
    outfile1a = open(fpath_out1a,'w')
    outfile1a.write('date lat lon tpvid tpvlat tpvlon tpvthetamin tpvamp tpvcircnow tpvradius')
    outfile1a.write('\n')

    outfile1b = open(fpath_out1b,'w')
    outfile1b.write('date lat lon tpvid tpvlat tpvlon tpvthetamin tpvamp tpvcircnow tpvradius')
    outfile1b.write('\n')

    outfile2a = open(fpath_out2a,'w')
    outfile2a.write('date lat lon thetamin amplitude circulation radius tpvid')
    outfile2a.write('\n')

    outfile2b = open(fpath_out2b,'w')
    outfile2b.write('date lat lon thetamin amplitude circulation radius tpvid')
    outfile2b.write('\n')


datelist_sfc = np.array(datelist_sfc).astype('int')
datenow = datestart
jet_superposition_event_count = 0
tpv_track_count = 0
jet_superposition_event_compare_count = 0
tpv_compare_count = 0


while datenow <= dateend:
    print(datenow)
    [tinds_sfc] = np.where(datelist_sfc == int(datenow))
    print(tinds_sfc)
    
    lat_sfc = latitude_jet[tinds_sfc]	
    lon_sfc = longitude_jet[tinds_sfc]

    [tinds] = np.where(datelist == np.int(datenow))
    lat = bb[tinds,1]	
    lon = bb[tinds,2]
    thetamin = bb[tinds,3]
    if climate_anomaly_option == True:
        thetaclim = bb[tinds,4]
        thetaamp = bb[tinds,5]
        vort_circ = bb[tinds,6]
        vort_radius = bb[tinds,7]
        if tpv_labels == 'True':
            tpvid = bb[tinds,8]
    else:	    
        thetaamp = bb[tinds,4]
        vort_circ = bb[tinds,5]	    
        vort_radius = bb[tinds,6]
        if tpv_labels == 'True':    
            tpvid = bb[tinds,7]
    
    latprev_sfc = -9999.
    lonprev_sfc = -9999.        
    for ii in range(0,len(lat_sfc)):

        if ( (ii < len(lat_sfc)) and (latprev_sfc == lat_sfc[ii]) and (lonprev_sfc == lon_sfc[ii]) ):             
            latprev_sfc = lat_sfc[ii] 
            lonprev_sfc = lon_sfc[ii]
            ii += 1
            break; break;	    

     
        #print("Working on surface cyclone point %i of %i" %(ii,len(lat_sfc)))
        lat_sfc_now = lat_sfc[ii]
        lon_sfc_now = lon_sfc[ii]
     
        jet_superposition_event_compare_count += 1

        latprev = -9999.
        lonprev = -9999.
        counted_sfccyclone = False
        for jj in range(0,len(lat)):
	    
            latnow = lat[jj]    
            lonnow = lon[jj]
            thetanow = thetamin[jj]
            ampnow = thetaamp[jj]
            circnow = vort_circ[jj]
            radiusnow = vort_radius[jj]
            if tpv_labels == 'True':
                tpvidnow = tpvid[jj]
            			    
            tpv_compare_count += 1
                 	
            distnow = um.earth_distm(latnow,lonnow,lat_sfc_now,lon_sfc_now) 
            
            if ( (distnow <= search_dist_thresh) ):
                #print(jj,len(lat),latnow,lonnow,latprev,lonprev,distnow)     
                if ( (latnow != latprev) and (lonnow != lonprev) ):
                    tpv_track_count += 1	
                    if counted_sfccyclone == False:	    
                        jet_superposition_event_count += 1  
                    counted_sfccyclone = True
                    if tpv_labels == 'False':                      
                        outfile1a.write('%-10s %7.2f %7.2f\n' % (datenow,lat_sfc_now,lon_sfc_now))
                        outfile2a.write('%-10s %7.2f %7.2f %7.2f %7.2f %7.2f %7.2f\n' % (datenow, latnow, lonnow, thetanow, ampnow, circnow, radiusnow))
                    else:
                        outfile1a.write('%-10s %7.2f %7.2f %6d %7.2f %7.2f %7.2f %7.2f %7.2f %7.2f\n' % (datenow,lat_sfc_now,lon_sfc_now,tpvidnow,latnow,lonnow,thetanow,ampnow,circnow,radiusnow))
                        outfile2a.write('%-10s %7.2f %7.2f %7.2f %7.2f %7.2f %7.2f %6d\n' % (datenow, latnow, lonnow, thetanow, ampnow, circnow, radiusnow, tpvidnow))		    
            else:
                if tpv_labels == 'False':
                    outfile1b.write('%-10s %7.2f %7.2f\n' % (datenow,lat_sfc_now,lon_sfc_now))
                    outfile2b.write('%-10s %7.2f %7.2f %7.2f %7.2f %7.2f %7.2f\n' % (datenow, latnow, lonnow, thetanow, ampnow, circnow, radiusnow))	    
                else:
                    outfile1b.write('%-10s %7.2f %7.2f %6d %7.2f %7.2f %7.2f %7.2f %7.2f %7.2f\n' % (datenow,lat_sfc_now,lon_sfc_now,tpvidnow,latnow,lonnow,thetanow,ampnow,circnow,radiusnow))
                    outfile2b.write('%-10s %7.2f %7.2f %7.2f %7.2f %7.2f %7.2f %6d\n' % (datenow, latnow, lonnow, thetanow, ampnow, circnow, radiusnow, tpvidnow))			
            latprev = latnow
            lonprev = lonnow
               
        latprev_sfc = lat_sfc_now
        lonprev_sfc = lon_sfc_now               
	        
    datenow = um.advance_time(datenow,hinc)
    del tinds, tinds_sfc    

percent_jetsuperpositions_near_tpvs = (jet_superposition_event_count/jet_superposition_event_compare_count)*100.
percent_tpvs_near_jetsuperpositions = (tpv_track_count/tpv_compare_count)*100.
print("Jet superposition events near TPV tracks: track count / total tracks / percentage")
print("%d / %d / %5.2f" %(jet_superposition_event_count,jet_superposition_event_compare_count,percent_jetsuperpositions_near_tpvs))
print("TPV tracks near jet superpositions: track count / total tracks / percentage")
print("%d / %d / %5.2f" %(tpv_track_count,tpv_compare_count,percent_tpvs_near_jetsuperpositions))
