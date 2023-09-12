#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 05:55:55 2023

@author: nathansmacbook
"""

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import pandas as pd

# Load your data from the CSV file
Eastsub = pd.read_csv('JetSuperpositions_EastSubtropicalDominant.csv')
PolarDom = pd.read_csv('JetSuperpositions_PolarDominant.csv')
SubtropicalDom = pd.read_csv('JetSuperpositions_SubtropicalDominant.csv')
WestSubdom= pd.read_csv('JetSuperpositions_WestSubtropicalDominant.csv')
Hybrid = pd.read_csv('JetSuperpositions_Hybrid.csv')

# Extract latitude, longitude, year, month, day, and hour columns for Eastsub
latsEast = Eastsub['Event_Latitude']
lonsEast = Eastsub['Event_Longitude']
yearsEast = Eastsub['Year']
# months = Eastsub['Month']
# days = Eastsub['Day']
# hours = Eastsub['Hour']

# Extract latitude, longitude, year, month, day, and hour columns for PolarDom
latsPolarDom = PolarDom['Event_Latitude']
lonsPolarDom = PolarDom['Event_Longitude']
yearsPolarDom = PolarDom['Year']
# months = Eastsub['Month']
# days = Eastsub['Day']
# hours = Eastsub['Hour']

# Extract latitude, longitude, year, month, day, and hour columns for SubtropicalDom
latsSubtropicalDom = SubtropicalDom['Event_Latitude']
lonsSubtropicalDom = SubtropicalDom['Event_Longitude']
yearsSubtropicalDom = SubtropicalDom['Year']
# months = Eastsub['Month']
# days = Eastsub['Day']
# hours = Eastsub['Hour']

# Extract latitude, longitude, year, month, day, and hour columns for WestSubdom
latsWestSubdom = WestSubdom['Event_Latitude']
lonsWestSubdom = WestSubdom['Event_Longitude']
yearsWestSubdom = WestSubdom['Year']
# months = Eastsub['Month']
# days = Eastsub['Day']
# hours = Eastsub['Hour']

# Extract latitude, longitude, year, month, day, and hour columns for Hybrid
latsHybrid = Hybrid['Event_Latitude']
lonsHybrid = Hybrid['Event_Longitude']
yearsHybrid = Hybrid['Year']
# months = Eastsub['Month']
# days = Eastsub['Day']
# hours = Eastsub['Hour']

# Create a Basemap of the US
map = Basemap(llcrnrlon=-125, llcrnrlat=20, urcrnrlon=-65, urcrnrlat=50, projection='merc', resolution='l')

# Draw coastlines, countries, and states
map.drawcoastlines()
map.drawcountries()
map.drawstates()

# Convert latitude and longitude to map coordinates
x, y = map(list(lonsEast), list(latsEast))
a, b = map(list(lonsPolarDom), list(latsPolarDom))
c, d = map(list(lonsSubtropicalDom), list(latsSubtropicalDom))
e, f = map(list(lonsWestSubdom), list(latsWestSubdom))
g, I = map(list(lonsHybrid), list(latsHybrid))


# Plot the data points with different colors based on year for East
for year_value in set(yearsEast):
    indices = [i for i, year in enumerate(yearsEast) if year == year_value]
    x_year = [x[i] for i in indices]
    y_year = [y[i] for i in indices]
    map.scatter(x_year, y_year, marker='o', label=f'Year {year_value}', alpha=0.7)
    
    
# Plot the data points with different colors based on year for PolarDom
for year_value in set(yearsPolarDom):
    indices = [i for i, year in enumerate(yearsPolarDom) if year == year_value]
    a_year = [a[i] for i in indices]
    b_year = [b[i] for i in indices]
    map.scatter(a_year, b_year, marker='o', label=f'Year {year_value}', alpha=0.7)
    
# Plot the data points with different colors based on year for subtropicalDom
for year_value in set(yearsSubtropicalDom):
    indices = [i for i, year in enumerate(yearsSubtropicalDom) if year == year_value]
    c_year = [c[i] for i in indices]
    d_year = [d[i] for i in indices]
    map.scatter(c_year, d_year, marker='o', label=f'Year {year_value}', alpha=0.7)
    
# Plot the data points with different colors based on year for WestSubdom
for year_value in set(yearsWestSubdom):
    indices = [i for i, year in enumerate(yearsWestSubdom) if year == year_value]
    e_year = [e[i] for i in indices]
    f_year = [f[i] for i in indices]
    map.scatter(e_year, f_year, marker='o', label=f'Year {year_value}', alpha=0.7)

# Plot the data points with different colors based on year for Hybrid
for year_value in set(yearsHybrid):
    indices = [i for i, year in enumerate(yearsHybrid) if year == year_value]
    g_year = [g[i] for i in indices]
    I_year = [I[i] for i in indices]
    map.scatter(g_year, I_year, marker='o', label=f'Year {year_value}', alpha=0.7)
    


# Add a legend

#plt.legend(ncol=2)

# Add title and show the plot
plt.title('Jetstream Positions via Lattitude and Longtitude Data on US Map (Color-coded by Year)')


plt.show()
