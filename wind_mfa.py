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
# SF future capacity with years as index #
sf_capacity = pd.read_excel(file_loc, sheet_name='Future capacity', usecols='B:D', index_col=0) # Onshore and offshore in one dataframe #
# FM future capacity with years as index #
fm_capacity = pd.read_excel(file_loc, sheet_name='Future capacity', usecols='G:I', index_col=0) # Onshore and offshore in one dataframe #
# ep future capacity with years as index #
ep_capacity = pd.read_excel(file_loc, sheet_name='Future capacity', usecols='L:N', index_col=0) # Onshore and offshore in one dataframe #

# Read in material intensity values #
MI = pd.read_excel(file_loc, sheet_name='Material intensity', index_col=0) # All materials in one dataframe, ton/MW #

# Market share variables for MI #
MS_on = 0.3 # onshore #
MS_off = 0.1 # offshore #

# Material efficiency improvements #
material_efficiency = pd.read_excel(file_loc, sheet_name='Material efficiency',usecols='A', index_col=0) 
final_year_value = pd.read_excel(file_loc, sheet_name='Material efficiency',usecols='B', index_col=0) 
