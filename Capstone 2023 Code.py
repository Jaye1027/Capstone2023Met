# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 10:09:36 2023

@author: Jay Edelmon, Cal Watson, James McAllister, Nathan Bailey
"""
#Import neccessary packages. 
import datetime as dt
import pandas as pd 
import numpy as np 
import metpy as mp
import cartopy as cartopy
import matplotlib as mpl
import matplotlib.pyplot as plt
import cartopy.feature as cfeature
import cartopy.crs as ccrs

#Github repository push/pull info.
path_of_git_repo = r'https://github.com/Jaye1027/Capstone2023Met.git'

#Reading in the data (pulled from Github)
url1 = "https://raw.githubusercontent.com/Jaye1027/Capstone2023Met/main/JetSuperpositions_EastSubtropicalDominant.txt" 
url2 = "https://raw.githubusercontent.com/Jaye1027/Capstone2023Met/main/JetSuperpositions_Hybrid.txt"
url3 = "https://raw.githubusercontent.com/Jaye1027/Capstone2023Met/main/JetSuperpositions_PolarDominant.txt"
url4 = "https://raw.githubusercontent.com/Jaye1027/Capstone2023Met/main/JetSuperpositions_SubtropicalDominant.txt"
url5 = "https://raw.githubusercontent.com/Jaye1027/Capstone2023Met/main/JetSuperpositions_WestSubtropicalDominant.txt"
eastsubdom1 = pd.read_csv(url1, index_col=('Year'))
eastsubdom2 = eastsubdom1['Event_Latitude'].astype(int)
eastsubdom3 = eastsubdom1['Event_Longitude'].astype(int)
hybrid1 = pd.read_csv(url2, index_col=('Year'))
hybrid2 = hybrid1['Event_Latitude'].astype(int)
hybrid3 = hybrid1['Event_Longitude'].astype(int)
polardom1 = pd.read_csv(url3, index_col=('Year'))
polardom2 = polardom1['Event_Latitude'].astype(int)
polardom3 = polardom1['Event_Longitude'].astype(int)
subtropdom1 = pd.read_csv(url4, index_col=('Year'))
subtropdom2 = subtropdom1['Event_Latitude'].astype(int)
subtropdom3 = subtropdom1['Event_Longitude'].astype(int)
westsubdom1 = pd.read_csv(url5, index_col=('Year'))
westsubdom2 = westsubdom1['Event_Latitude'].astype(int)
westsubdom3 = westsubdom1['Event_Longitude'].astype(int)

#Main code.
central_lat = 37.5
central_lon = -96
extent = [-120, -70, 24, 50.5]
central_lon = np.mean(extent[:2])
central_lat = np.mean(extent[2:])

ax1 = plt.figure(figsize=(12, 6))
ax1 = plt.axes(projection=ccrs.AlbersEqualArea(central_lon, central_lat))
ax1.set_extent(extent)
ax1.add_feature(cartopy.feature.OCEAN)
ax1.add_feature(cartopy.feature.LAND, edgecolor='black')
ax1.add_feature(cartopy.feature.LAKES, edgecolor='black')
ax1.add_feature(cartopy.feature.RIVERS)
ax1.scatter(eastsubdom2, eastsubdom3, color = 'red')
ax1.scatter(hybrid2, hybrid3, color = 'blue')
ax1.scatter(polardom2, polardom3, color = 'green')
ax1.scatter(subtropdom2, subtropdom3, color = 'yellow')
ax1.scatter(westsubdom2, westsubdom3, color = 'purple')

print(westsubdom2)








