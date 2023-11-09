# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 11:48:21 2023

@author: Jay Edelmon 
This script combines multiple data files into one large file to be used for creating graphics, running analysis, etc.
"""
import pandas as pd 

df1 = pd.read_csv('storm_data_search_results.csv', error_bad_lines=(False))
df2 = pd.read_csv('storm_data_search_results(1).csv', error_bad_lines=(False))
df3 = pd.read_csv('storm_data_search_results(1)2.csv', error_bad_lines=(False))
df4 = pd.read_csv('storm_data_search_results(1)3.csv', error_bad_lines=(False))
df5 = pd.read_csv('storm_data_search_results(1)4.csv', error_bad_lines=(False))
df6 = pd.read_csv('storm_data_search_results(1)5.csv', error_bad_lines=(False))
df7 = pd.read_csv('storm_data_search_results(1)6.csv', error_bad_lines=(False))
df8 = pd.read_csv('storm_data_search_results(1)7.csv', error_bad_lines=(False))
df9 = pd.read_csv('storm_data_search_results(1)8.csv', error_bad_lines=(False))
df10 = pd.read_csv('storm_data_search_results(1)9.csv', error_bad_lines=(False))
df11 = pd.read_csv('storm_data_search_results(1)10.csv', error_bad_lines=(False))
df12 = pd.read_csv('storm_data_search_results(1)11.csv', error_bad_lines=(False))
df13 = pd.read_csv('storm_data_search_results(1)12.csv', error_bad_lines=(False))
df14 = pd.read_csv('storm_data_search_results(1)13.csv', error_bad_lines=(False))

df1.fillna(-999, inplace = False)
df2.fillna(-999, inplace = False)
df3.fillna(-999, inplace = False)
df4.fillna(-999, inplace = False)
df5.fillna(-999, inplace = False)
df6.fillna(-999, inplace = False)
df7.fillna(-999, inplace = False)
df8.fillna(-999, inplace = False)
df9.fillna(-999, inplace = False)
df10.fillna(-999, inplace = False)
df11.fillna(-999, inplace = False)
df12.fillna(-999, inplace = False)
df13.fillna(-999, inplace = False)
df14.fillna(-999, inplace = False)

dataframelist = [df1,df2,df3,df4,df5,df6,df7,df8,df9,df10,df11,df12,df13,df14]
newframe = pd.concat(dataframelist, ignore_index=True)
#newframe["BEGIN_DATE"] = newframe["BEGIN_DATE"].astype('datetime64[ns]')
newframe.to_csv('Combined Winter Data 1979-2010.csv')





