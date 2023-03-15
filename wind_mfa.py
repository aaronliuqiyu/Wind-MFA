# Import required packages #
# These packages needs to be installed and imported for the script to run #
import pandas as pd
import numpy as np
import os

# Import ODYM dynamic stock model #
# This package is used to carry out the MFA calculations #
# ODYM has other modules, but I am currently only using the dynamic stock model module, see https://github.com/IndEcol/ODYM for detailed documentation #
from dynamic_stock_model import DynamicStockModel as DSM

# Set option so that pandas does not create a copy of the dataframe #
pd.set_option('mode.chained_assignment', None)

# Create an object for easier index slicing #
idx = pd.IndexSlice

# Set working directory #
# Change the directory in the bracket to where your data files are located #
# This does not have to be the same location as the git clone #
os.chdir("C:\\Users\\qiyu\\OneDrive - Chalmers\\WindMFA") # Change this to local directory# 

# Suppress scientific notation so the output is easier to read #
pd.set_option('display.float_format', lambda x: '%.3f' % x)

# Read in input data from excel file #
file_loc = 'wind_input.xlsx'
# Historical capacity with years as index #
hist_capacity = pd.read_excel(file_loc, sheet_name='Historical capacity', usecols='A:C', index_col=0)
hist_capacity_on = hist_capacity.iloc[:,0] # Onshore historical installed capacity #
hist_capacity_off = hist_capacity.iloc[:,1] # Offshore historical installed capacity #
# SF future capacity with years as index #
sf_capacity = pd.read_excel(file_loc, sheet_name='Future capacity', usecols='B:D', index_col=0) # Onshore and offshore in one dataframe #
sf_capacity_on = sf_capacity.iloc[:,0] # Onshore sf scenario installed capacity #
sf_capacity_off = sf_capacity.iloc[:,1] # Offshore sf scenario installed capacity #
# FM future capacity with years as index #
fm_capacity = pd.read_excel(file_loc, sheet_name='Future capacity', usecols='G:I', index_col=0) # Onshore and offshore in one dataframe #
fm_capacity_on = fm_capacity.iloc[:,0] # Onshore fm scenario installed capacity #
fm_capacity_off = fm_capacity.iloc[:,1] # Offshore fm scenario installed capacity #
# ep future capacity with years as index #
ep_capacity = pd.read_excel(file_loc, sheet_name='Future capacity', usecols='L:N', index_col=0) # Onshore and offshore in one dataframe #
ep_capacity_on = fm_capacity.iloc[:,0] # Onshore ep scenario installed capacity #
ep_capacity_off = fm_capacity.iloc[:,1] # Offshore ep scenario installed capacity #

# Read in material intensity values #
MI = pd.read_excel(file_loc, sheet_name='Material intensity', index_col=0) # All materials in one dataframe, ton/MW #
MI_onshore = MI.iloc[:,0]
MI_offshore = MI.iloc[:,1]


# Market share variables for MI #
MS_on = 0.3 # onshore #
MS_off = 1 # offshore #

# Material efficiency improvements #
material_efficiency = pd.read_excel(file_loc, sheet_name='Material efficiency',usecols='A, B', index_col=0) 
initial_year_value = pd.read_excel(file_loc, sheet_name='Material efficiency',usecols='A, C', index_col=0) # Here initial year value is for 2020 #

# Interpolation of MI based on efficiency and market share #
from helper import interpolate
MI_final = interpolate(material_efficiency,initial_year_value,MS_on,MS_off)
print(MI_final)
