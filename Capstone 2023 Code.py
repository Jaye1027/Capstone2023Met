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
eastsubdom = pd.read_csv(url1, index_col='Year')
hybrid = pd.read_csv(url2, index_col='Year')
polardom = pd.read_csv(url3, index_col='Year')
subtropdom = pd.read_csv(url4, index_col='Year')
westsubdom = pd.read_csv(url5, index_col="Year")

#Main code.
central_lat = 37.5
central_lon = -96
extent = [-120, -70, 24, 50.5]
central_lon = np.mean(extent[:2])
central_lat = np.mean(extent[2:])

ax = plt.figure(figsize=(12, 6))
ax = plt.axes(projection=ccrs.AlbersEqualArea(central_lon, central_lat))
ax.set_extent(extent)
ax.add_feature(cartopy.feature.OCEAN)
ax.add_feature(cartopy.feature.LAND, edgecolor='black')
ax.add_feature(cartopy.feature.LAKES, edgecolor='black')
ax.add_feature(cartopy.feature.RIVERS)
ax.scatter(eastsubdom['Event_Latitude'], eastsubdom['Event_Longitude'], color = 'red')
ax.scatter(hybrid['Event_Latitude'], hybrid['Event_Longitude'], color = 'blue')
ax.scatter(polardom['Event_Latitude'], polardom['Event_Longitude'], color = 'green')
ax.scatter(subtropdom['Event_Latitude'], subtropdom['Event_Longitude'], color = 'yellow')
ax.scatter(westsubdom['Event_Latitude'], westsubdom['Event_Longitude'], color = 'purple')








