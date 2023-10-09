# connect_sfccyclones2tpvs.py
# Steven Cavallo
# June 2022

#####Imports##############################
# imports
import os
import conda

conda_file_dir = conda.__file__
conda_dir = conda_file_dir.split('lib')[0]
proj_lib = os.path.join(os.path.join(conda_dir, 'share'), 'proj')
os.environ["PROJ_LIB"] = proj_lib
import netCDF4

import numpy as np
import weather_modules as wm
from mstats import *
import utilities_modules as um
#####User Inupts##########################
#mm_prefix = ''
mm_prefix = ''


track_file1 = '/data2/scavallo/ERA5/sprenger_sfccyclone/ERA5_sfccyclones_arctictracks_2days_synoptic_' + mm_prefix + '1979010100_2019123100.dat'
track_file2 = '/data2/scavallo/ERA5/tpv_tracks/tracks_low_horizPlusVert_60N65_' + mm_prefix + 'withids_1979-2021.txt'


fpath_out1a = '/data2/scavallo/ERA5/sprenger_sfccyclone/interactions_2023/NH/radius_933km/dummy1.dat'
fpath_out1b = '/data2/scavallo/ERA5/sprenger_sfccyclone/interactions_2023/NH/radius_933km/dummy2.dat'
fpath_out2a = '/data2/scavallo/ERA5/sprenger_sfccyclone/interactions_2023/NH/radius_933km/dummy3.dat'
fpath_out2b = '/data2/scavallo/ERA5/sprenger_sfccyclone/interactions_2023/NH/radius_933km/dummy4.dat'

datestart = '1979010100'
dateend = '2019123118'
hinc = 6

climate_anomaly_option = False
tpv_labels = 'True'
search_dist_thresh = 933. # km


###############################
# Load track files
###############################
fpath = track_file1
aa = np.loadtxt(fpath, skiprows=1)     
datelist_sfc = aa[:,0]

fpath = track_file2
bb = np.loadtxt(fpath, skiprows=1) 
datelist = bb[:,0]

if tpv_labels == 'False':
    outfile1a = open(fpath_out1a,'w')
    outfile1a.write('date lat lon pmin pintensity idclust label1 label2 label3')
    outfile1a.write('\n')

    outfile1b = open(fpath_out1b,'w')
    outfile1b.write('date lat lon pmin pintensity idclust label1 label2 label3')
    outfile1b.write('\n')

    outfile2a = open(fpath_out2a,'w')
    outfile2a.write('date lat lon thetamin amplitude circulation radius')
    outfile2a.write('\n')

    outfile2b = open(fpath_out2b,'w')
    outfile2b.write('date lat lon thetamin amplitude circulation radius')
    outfile2b.write('\n')
else:
    outfile1a = open(fpath_out1a,'w')
    outfile1a.write('date lat lon pmin pintensity idclust label1 label2 label3 tpvid tpvlat tpvlon tpvthetamin tpvamp tpvcircnow tpvradius')
    outfile1a.write('\n')

    outfile1b = open(fpath_out1b,'w')
    outfile1b.write('date lat lon pmin pintensity idclust label1 label2 label3 tpvid tpvlat tpvlon tpvthetamin tpvamp tpvcircnow tpvradius')
    outfile1b.write('\n')

    outfile2a = open(fpath_out2a,'w')
    outfile2a.write('date lat lon thetamin amplitude circulation radius tpvid sfcid')
    outfile2a.write('\n')

    outfile2b = open(fpath_out2b,'w')
    outfile2b.write('date lat lon thetamin amplitude circulation radius tpvid sfcid')
    outfile2b.write('\n')


datelist_sfc = np.array(datelist_sfc).astype('int')
datenow = datestart
sfc_cyclone_track_count = 0
tpv_track_count = 0
sfc_cyclone_compare_count = 0
tpv_compare_count = 0
while datenow <= dateend:
    print(datenow)
    [tinds_sfc] = np.where(datelist_sfc == int(datenow))
    
    lat_sfc = aa[tinds_sfc,1]	
    lon_sfc = aa[tinds_sfc,2]
    mslp = aa[tinds_sfc,3]
    pamp = aa[tinds_sfc,4]
    idclusts = aa[tinds_sfc,5]
    labels1 = aa[tinds_sfc,6]
    labels2 = aa[tinds_sfc,7]
    labels3 = aa[tinds_sfc,8]  

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
        mslp_now = mslp[ii]
        pamp_now = pamp[ii]
        idclusts_now = idclusts[ii]
        labels1_now = labels1[ii]
        labels2_now = labels2[ii]	
        labels3_now = labels3[ii]
     
        sfc_cyclone_compare_count += 1

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
            
            if (datenow == '2000122206'):
                print(jj,len(lat),datenow,latnow,lonnow,lat_sfc_now,lon_sfc_now)
                abc = 0
            else:
                abc = 0
            if ( (distnow <= search_dist_thresh) ):
                #print(jj,len(lat),latnow,lonnow,latprev,lonprev,distnow)     
                if ( (latnow != latprev) and (lonnow != lonprev) ):
                    tpv_track_count += 1	
                    if counted_sfccyclone == False:	    
                        sfc_cyclone_track_count += 1  
                    counted_sfccyclone = True
                    if tpv_labels == 'False':                      
                        outfile1a.write('%-10s %7.2f %7.2f %7.2f %7.2f %7.2f %7.2f %9.1f %9.1f\n' % (datenow,lat_sfc_now,lon_sfc_now,mslp_now,pamp_now,idclusts_now,labels1_now,labels2_now,labels3_now))
                        outfile2a.write('%-10s %7.2f %7.2f %7.2f %7.2f %7.2f %7.2f\n' % (datenow, latnow, lonnow, thetanow, ampnow, circnow, radiusnow))
                    else:
                        outfile1a.write('%-10s %7.2f %7.2f %7.2f %7.2f %7.2f %7.2f %9.1f %9.1f %6d %7.2f %7.2f %7.2f %7.2f %7.2f %7.2f\n' % (datenow,lat_sfc_now,lon_sfc_now,mslp_now,pamp_now,idclusts_now,labels1_now,labels2_now,labels3_now,tpvidnow,latnow,lonnow,thetanow,ampnow,circnow,radiusnow))
                        outfile2a.write('%-10s %7.2f %7.2f %7.2f %7.2f %7.2f %7.2f %6d %9.1f\n' % (datenow, latnow, lonnow, thetanow, ampnow, circnow, radiusnow, tpvidnow, labels3_now))		    
            else:
                if tpv_labels == 'False':
                    outfile1b.write('%-10s %7.2f %7.2f %7.2f %7.2f %7.2f %7.2f %9.1f %9.1f\n' % (datenow,lat_sfc_now,lon_sfc_now,mslp_now,pamp_now,idclusts_now,labels1_now,labels2_now,labels3_now))
                    outfile2b.write('%-10s %7.2f %7.2f %7.2f %7.2f %7.2f %7.2f\n' % (datenow, latnow, lonnow, thetanow, ampnow, circnow, radiusnow))	    
                else:
                    outfile1b.write('%-10s %7.2f %7.2f %7.2f %7.2f %7.2f %7.2f %9.1f %9.1f %6d %7.2f %7.2f %7.2f %7.2f %7.2f %7.2f\n' % (datenow,lat_sfc_now,lon_sfc_now,mslp_now,pamp_now,idclusts_now,labels1_now,labels2_now,labels3_now,tpvidnow,latnow,lonnow,thetanow,ampnow,circnow,radiusnow))
                    outfile2b.write('%-10s %7.2f %7.2f %7.2f %7.2f %7.2f %7.2f %6d %9.1f\n' % (datenow, latnow, lonnow, thetanow, ampnow, circnow, radiusnow, tpvidnow, labels3_now))			
            latprev = latnow
            lonprev = lonnow
               
        latprev_sfc = lat_sfc_now
        lonprev_sfc = lon_sfc_now               
	        
    datenow = um.advance_time(datenow,hinc)
    del tinds, tinds_sfc    

percent_sfccyclones_near_tpvs = (sfc_cyclone_track_count/sfc_cyclone_compare_count)*100.
percent_tpvs_near_sfccyclones = (tpv_track_count/tpv_compare_count)*100.
print("Surface cyclone tracks near TPV tracks: track count / total tracks / percentage")
print("%d / %d / %5.2f" %(sfc_cyclone_track_count,sfc_cyclone_compare_count,percent_sfccyclones_near_tpvs))
print("TPV tracks near surface cyclone tracks: track count / total tracks / percentage")
print("%d / %d / %5.2f" %(tpv_track_count,tpv_compare_count,percent_tpvs_near_sfccyclones))
