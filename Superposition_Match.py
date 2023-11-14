#!/usr/bin/env python
# coding: utf-8

# In[57]:


### Import ###
from netCDF4 import Dataset
import numpy as np
import pandas as pd

import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib
import matplotlib.pyplot as plt
import utilities_modules as um


# In[58]:


### User Inputs ###
storm_events = 'NOAA_Storm_Events_Database_1950-2021_v2_5020206754103453289.csv'
hybrid = 'JetSuperpositions_Hybrid (1).txt'
eastsub = 'JetSuperpositions_EastSubtropicalDominant (1).txt'
polar = 'JetSuperpositions_PolarDominant (1).txt'
sub = 'JetSuperpositions_SubtropicalDominant (1).txt'
westsub = 'JetSuperpositions_WestSubtropicalDominant (1).txt'


# In[62]:


### Parameters ###

# Storm Events
events = pd.read_csv(storm_events,sep=',')
#print(events)
storm_dates = events['BEGIN_DATE_TIME']
#print(storm_dates)

## Convert to datetime
storm_dt = pd.to_datetime(storm_dates)
#print(storm_dt)

## Add datetime column to end of file
events.insert(0, 'Dates', storm_dt)
#print(events)

# Jet Superpositions
## Concatenate files
super_hybrid = pd.read_csv(hybrid, error_bad_lines=(False))
super_hybrid.fillna(-999, inplace = False)
super_eastsub = pd.read_csv(eastsub, error_bad_lines=(False))
super_eastsub.fillna(-999, inplace = False)
super_polar = pd.read_csv(polar, error_bad_lines=(False))
super_polar.fillna(-999, inplace = False)
super_sub = pd.read_csv(sub, error_bad_lines=(False))
super_sub.fillna(-999, inplace = False)
super_westsub = pd.read_csv(westsub, error_bad_lines=(False))
super_westsub.fillna(-999, inplace = False)

df_list = [super_hybrid, super_eastsub, super_polar, super_sub, super_westsub]
super_file = pd.concat(df_list, ignore_index = True)
super_file.to_csv('Combined Jet Superpositions')
#print(super_file)

## Convert to datetime
year = super_file['Year'].astype(int)
month = super_file['Month'].astype(int)
day = super_file['Day'].astype(int)
df = year.map(str) + '-' + month.map(str) + '-' + day.map(str)
df_dt = pd.to_datetime(df)
#print(df_dt)

## Add datetime column to end of file
super_file.insert(0, 'Dates', df_dt)
#print(super_file)


# In[66]:


### Code ###

# Store jet superposition lats/lons
super_file_lat = super_file['Event_Latitude']
super_file_lon = super_file['Event_Longitude']
#print(super_file_lat)

# Store events lat/lons
events_lon = events['x'] # lon is x
events_lat = events['y'] # lat is y
#print(events_lat)

# Loop through event dates
dates_length = len(storm_dates) # number of dates
#print(dates_length)

## Create empty array that stores dates
equal_df = []
current_date = 0
for i in range(dates_length):
    current_date = storm_dates[i] # set current date
    #for j in range(dates_length):
        #if sotrm

## current date event
# Find if there are any dates that equal in superposition
## loop through superposition lat, lons
### calculate distance between superposition lat/lon and event lat/lon
#### if distance <= threshold, save data


# In[ ]:




