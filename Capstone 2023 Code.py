# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 10:09:36 2023

@author: Jay Edelmon, Cal Watson, James McAllister, Nathan Bailey
"""
#Import neccessary packages. 
import datetime as dt
import pandas as pd 
import numpy as np 

#Github repository push/pull info.
path_of_git_repo = r'https://github.com/Jaye1027/Capstone2023Met.git'
commit_message = "Capstone project 2023 updated comment script"

#Reading in the data (pulled from Github)
url1 = "https://raw.githubusercontent.com/Jaye1027/Capstone2023Met/main/JetSuperpositions_EastSubtropicalDominant.txt" 
url2 = "https://raw.githubusercontent.com/Jaye1027/Capstone2023Met/main/JetSuperpositions_Hybrid.txt"
url3 = "https://raw.githubusercontent.com/Jaye1027/Capstone2023Met/main/JetSuperpositions_PolarDominant.txt"
url4 = "https://raw.githubusercontent.com/Jaye1027/Capstone2023Met/main/JetSuperpositions_SubtropicalDominant.txt"
url5 = "https://raw.githubusercontent.com/Jaye1027/Capstone2023Met/main/JetSuperpositions_WestSubtropicalDominant.txt"
eastsubdom = pd.read_csv(url1)
hybrid = pd.read_csv(url2)
polardom = pd.read_csv(url3)
subtropdom = pd.read_csv(url4)
westsubdom = pd.read_csv(url5)

#Main code.


#Upload to Github (push to Github).

