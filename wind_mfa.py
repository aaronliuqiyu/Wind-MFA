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

# Read in lifetime parameter from excel #
lifetime = pd.read_excel(file_loc, sheet_name='Lifetime', usecols='A:C', index_col=0)

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
MI_both = interpolate(material_efficiency,initial_year_value,MS_on,MS_off)

# Seperate on and offshore into two dataframes to make life easier#
MI_on = MI_both.loc[[0,2,4,6,8,10,12], :]
MI_off = MI_both.loc[[1,3,5,7,9,11,13], :]

# Change the row indexes
MI_on.index = ['Concrete', 'Steel', 'Copper', 'Aluminium', 'Fiber Glass', 'Neodymium', 'Dysprosium']
MI_off.index = ['Concrete', 'Steel', 'Copper', 'Aluminium', 'Fiber Glass', 'Neodymium', 'Dysprosium']

# stock driven #
from helper import stock_driven
sf_on_capacity_expansion, sf_on_outflow, sf_on_inflow = stock_driven(sf_capacity_on,lifetime)
sf_off_capacity_expansion, sf_off_outflow, sf_off_inflow = stock_driven(sf_capacity_off,lifetime)
fm_on_capacity_expansion, fm_on_outflow, fm_on_inflow = stock_driven(fm_capacity_on,lifetime)
fm_off_capacity_expansion, fm_off_outflow, fm_off_inflow = stock_driven(fm_capacity_off,lifetime)
ep_on_capacity_expansion, ep_on_outflow, ep_on_inflow = stock_driven(ep_capacity_on,lifetime)
ep_off_capacity_expansion, ep_off_outflow, ep_off_inflow = stock_driven(ep_capacity_off,lifetime)

# inflow materials #
# Ugly code I know :(, will think about a better way to do it# # TO DO #
# I tried a more elegant way to do this but it broke my code :( , so leaving it like this for now #
sf_on_inflow_concrete = MI_on.iloc[0].values * sf_on_inflow.values.flatten()
sf_on_inflow_steel = MI_on.iloc[1].values * sf_on_inflow.values.flatten()
sf_on_inflow_copper = MI_on.iloc[2].values * sf_on_inflow.values.flatten()
sf_on_inflow_aluminium = MI_on.iloc[3].values * sf_on_inflow.values.flatten()
sf_on_inflow_fiberglass = MI_on.iloc[4].values * sf_on_inflow.values.flatten()
sf_on_inflow_neodymium = MI_on.iloc[5].values * sf_on_inflow.values.flatten()
sf_on_inflow_dysprosium = MI_on.iloc[6].values * sf_on_inflow.values.flatten()

sf_off_inflow_concrete = MI_on.iloc[0].values * sf_off_inflow.values.flatten()
sf_off_inflow_steel = MI_on.iloc[1].values * sf_off_inflow.values.flatten()
sf_off_inflow_copper = MI_on.iloc[2].values * sf_off_inflow.values.flatten()
sf_off_inflow_aluminium = MI_on.iloc[3].values * sf_off_inflow.values.flatten()
sf_off_inflow_fiberglass = MI_on.iloc[4].values * sf_off_inflow.values.flatten()
sf_off_inflow_neodymium = MI_on.iloc[5].values * sf_off_inflow.values.flatten()
sf_off_inflow_dysprosium = MI_on.iloc[6].values * sf_off_inflow.values.flatten()

fm_on_inflow_concrete = MI_on.iloc[0].values * fm_on_inflow.values.flatten()
fm_on_inflow_steel = MI_on.iloc[1].values * fm_on_inflow.values.flatten()
fm_on_inflow_copper = MI_on.iloc[2].values * fm_on_inflow.values.flatten()
fm_on_inflow_aluminium = MI_on.iloc[3].values * fm_on_inflow.values.flatten()
fm_on_inflow_fiberglass = MI_on.iloc[4].values * fm_on_inflow.values.flatten()
fm_on_inflow_neodymium = MI_on.iloc[5].values * fm_on_inflow.values.flatten()
fm_on_inflow_dysprosium = MI_on.iloc[6].values * fm_on_inflow.values.flatten()

fm_off_inflow_concrete = MI_on.iloc[0].values * fm_off_inflow.values.flatten()
fm_off_inflow_steel = MI_on.iloc[1].values * fm_off_inflow.values.flatten()
fm_off_inflow_copper = MI_on.iloc[2].values * fm_off_inflow.values.flatten()
fm_off_inflow_aluminium = MI_on.iloc[3].values * fm_off_inflow.values.flatten()
fm_off_inflow_fiberglass = MI_on.iloc[4].values * fm_off_inflow.values.flatten()
fm_off_inflow_neodymium = MI_on.iloc[5].values * fm_off_inflow.values.flatten()
fm_off_inflow_dysprosium = MI_on.iloc[6].values * fm_off_inflow.values.flatten()

ep_on_inflow_concrete = MI_on.iloc[0].values * ep_on_inflow.values.flatten()
ep_on_inflow_steel = MI_on.iloc[1].values * ep_on_inflow.values.flatten()
ep_on_inflow_copper = MI_on.iloc[2].values * ep_on_inflow.values.flatten()
ep_on_inflow_aluminium = MI_on.iloc[3].values * ep_on_inflow.values.flatten()
ep_on_inflow_fiberglass = MI_on.iloc[4].values * ep_on_inflow.values.flatten()
ep_on_inflow_neodymium = MI_on.iloc[5].values * ep_on_inflow.values.flatten()
ep_on_inflow_dysprosium = MI_on.iloc[6].values * ep_on_inflow.values.flatten()

ep_off_inflow_concrete = MI_on.iloc[0].values * ep_off_inflow.values.flatten()
ep_off_inflow_steel = MI_on.iloc[1].values * ep_off_inflow.values.flatten()
ep_off_inflow_copper = MI_on.iloc[2].values * ep_off_inflow.values.flatten()
ep_off_inflow_aluminium = MI_on.iloc[3].values * ep_off_inflow.values.flatten()
ep_off_inflow_fiberglass = MI_on.iloc[4].values * ep_off_inflow.values.flatten()
ep_off_inflow_neodymium = MI_on.iloc[5].values * ep_off_inflow.values.flatten()
ep_off_inflow_dysprosium = MI_on.iloc[6].values * ep_off_inflow.values.flatten()

# Outflows #
sf_on_outflow_concrete = MI_on.iloc[0].values * sf_on_outflow.values.flatten()
sf_on_outflow_steel = MI_on.iloc[1].values * sf_on_outflow.values.flatten()
sf_on_outflow_copper = MI_on.iloc[2].values * sf_on_outflow.values.flatten()
sf_on_outflow_aluminium = MI_on.iloc[3].values * sf_on_outflow.values.flatten()
sf_on_outflow_fiberglass = MI_on.iloc[4].values * sf_on_outflow.values.flatten()
sf_on_outflow_neodymium = MI_on.iloc[5].values * sf_on_outflow.values.flatten()
sf_on_outflow_dysprosium = MI_on.iloc[6].values * sf_on_outflow.values.flatten()

sf_off_outflow_concrete = MI_on.iloc[0].values * sf_off_outflow.values.flatten()
sf_off_outflow_steel = MI_on.iloc[1].values * sf_off_outflow.values.flatten()
sf_off_outflow_copper = MI_on.iloc[2].values * sf_off_outflow.values.flatten()
sf_off_outflow_aluminium = MI_on.iloc[3].values * sf_off_outflow.values.flatten()
sf_off_outflow_fiberglass = MI_on.iloc[4].values * sf_off_outflow.values.flatten()
sf_off_outflow_neodymium = MI_on.iloc[5].values * sf_off_outflow.values.flatten()
sf_off_outflow_dysprosium = MI_on.iloc[6].values * sf_off_outflow.values.flatten()

fm_on_outflow_concrete = MI_on.iloc[0].values * fm_on_outflow.values.flatten()
fm_on_outflow_steel = MI_on.iloc[1].values * fm_on_outflow.values.flatten()
fm_on_outflow_copper = MI_on.iloc[2].values * fm_on_outflow.values.flatten()
fm_on_outflow_aluminium = MI_on.iloc[3].values * fm_on_outflow.values.flatten()
fm_on_outflow_fiberglass = MI_on.iloc[4].values * fm_on_outflow.values.flatten()
fm_on_outflow_neodymium = MI_on.iloc[5].values * fm_on_outflow.values.flatten()
fm_on_outflow_dysprosium = MI_on.iloc[6].values * fm_on_outflow.values.flatten()

fm_off_outflow_concrete = MI_on.iloc[0].values * fm_off_outflow.values.flatten()
fm_off_outflow_steel = MI_on.iloc[1].values * fm_off_outflow.values.flatten()
fm_off_outflow_copper = MI_on.iloc[2].values * fm_off_outflow.values.flatten()
fm_off_outflow_aluminium = MI_on.iloc[3].values * fm_off_outflow.values.flatten()
fm_off_outflow_fiberglass = MI_on.iloc[4].values * fm_off_outflow.values.flatten()
fm_off_outflow_neodymium = MI_on.iloc[5].values * fm_off_outflow.values.flatten()
fm_off_outflow_dysprosium = MI_on.iloc[6].values * fm_off_outflow.values.flatten()

ep_on_outflow_concrete = MI_on.iloc[0].values * ep_on_outflow.values.flatten()
ep_on_outflow_steel = MI_on.iloc[1].values * ep_on_outflow.values.flatten()
ep_on_outflow_copper = MI_on.iloc[2].values * ep_on_outflow.values.flatten()
ep_on_outflow_aluminium = MI_on.iloc[3].values * ep_on_outflow.values.flatten()
ep_on_outflow_fiberglass = MI_on.iloc[4].values * ep_on_outflow.values.flatten()
ep_on_outflow_neodymium = MI_on.iloc[5].values * ep_on_outflow.values.flatten()
ep_on_outflow_dysprosium = MI_on.iloc[6].values * ep_on_outflow.values.flatten()

ep_off_outflow_concrete = MI_on.iloc[0].values * ep_off_outflow.values.flatten()
ep_off_outflow_steel = MI_on.iloc[1].values * ep_off_outflow.values.flatten()
ep_off_outflow_copper = MI_on.iloc[2].values * ep_off_outflow.values.flatten()
ep_off_outflow_aluminium = MI_on.iloc[3].values * ep_off_outflow.values.flatten()
ep_off_outflow_fiberglass = MI_on.iloc[4].values * ep_off_outflow.values.flatten()
ep_off_outflow_neodymium = MI_on.iloc[5].values * ep_off_outflow.values.flatten()
ep_off_outflow_dysprosium = MI_on.iloc[6].values * ep_off_outflow.values.flatten()

# Expansion calculated by ODYM #
sf_on_expansion_concrete = MI_on.iloc[0].values * sf_on_capacity_expansion.values.flatten()
sf_on_expansion_steel = MI_on.iloc[1].values * sf_on_capacity_expansion.values.flatten()
sf_on_expansion_copper = MI_on.iloc[2].values * sf_on_capacity_expansion.values.flatten()
sf_on_expansion_aluminium = MI_on.iloc[3].values * sf_on_capacity_expansion.values.flatten()
sf_on_expansion_fiberglass = MI_on.iloc[4].values * sf_on_capacity_expansion.values.flatten()
sf_on_expansion_neodymium = MI_on.iloc[5].values * sf_on_capacity_expansion.values.flatten()
sf_on_expansion_dysprosium = MI_on.iloc[6].values * sf_on_capacity_expansion.values.flatten()

sf_off_expansion_concrete = MI_on.iloc[0].values * sf_off_capacity_expansion.values.flatten()
sf_off_expansion_steel = MI_on.iloc[1].values * sf_off_capacity_expansion.values.flatten()
sf_off_expansion_copper = MI_on.iloc[2].values * sf_off_capacity_expansion.values.flatten()
sf_off_expansion_aluminium = MI_on.iloc[3].values * sf_off_capacity_expansion.values.flatten()
sf_off_expansion_fiberglass = MI_on.iloc[4].values * sf_off_capacity_expansion.values.flatten()
sf_off_expansion_neodymium = MI_on.iloc[5].values * sf_off_capacity_expansion.values.flatten()
sf_off_expansion_dysprosium = MI_on.iloc[6].values * sf_off_capacity_expansion.values.flatten()

fm_on_expansion_concrete = MI_on.iloc[0].values * fm_on_capacity_expansion.values.flatten()
fm_on_expansion_steel = MI_on.iloc[1].values * fm_on_capacity_expansion.values.flatten()
fm_on_expansion_copper = MI_on.iloc[2].values * fm_on_capacity_expansion.values.flatten()
fm_on_expansion_aluminium = MI_on.iloc[3].values * fm_on_capacity_expansion.values.flatten()
fm_on_expansion_fiberglass = MI_on.iloc[4].values * fm_on_capacity_expansion.values.flatten()
fm_on_expansion_neodymium = MI_on.iloc[5].values * fm_on_capacity_expansion.values.flatten()
fm_on_expansion_dysprosium = MI_on.iloc[6].values * fm_on_capacity_expansion.values.flatten()

fm_off_expansion_concrete = MI_on.iloc[0].values * fm_off_capacity_expansion.values.flatten()
fm_off_expansion_steel = MI_on.iloc[1].values * fm_off_capacity_expansion.values.flatten()
fm_off_expansion_copper = MI_on.iloc[2].values * fm_off_capacity_expansion.values.flatten()
fm_off_expansion_aluminium = MI_on.iloc[3].values * fm_off_capacity_expansion.values.flatten()
fm_off_expansion_fiberglass = MI_on.iloc[4].values * fm_off_capacity_expansion.values.flatten()
fm_off_expansion_neodymium = MI_on.iloc[5].values * fm_off_capacity_expansion.values.flatten()
fm_off_expansion_dysprosium = MI_on.iloc[6].values * fm_off_capacity_expansion.values.flatten()

ep_on_expansion_concrete = MI_on.iloc[0].values * ep_on_capacity_expansion.values.flatten()
ep_on_expansion_steel = MI_on.iloc[1].values * ep_on_capacity_expansion.values.flatten()
ep_on_expansion_copper = MI_on.iloc[2].values * ep_on_capacity_expansion.values.flatten()
ep_on_expansion_aluminium = MI_on.iloc[3].values * ep_on_capacity_expansion.values.flatten()
ep_on_expansion_fiberglass = MI_on.iloc[4].values * ep_on_capacity_expansion.values.flatten()
ep_on_expansion_neodymium = MI_on.iloc[5].values * ep_on_capacity_expansion.values.flatten()
ep_on_expansion_dysprosium = MI_on.iloc[6].values * ep_on_capacity_expansion.values.flatten()

ep_off_expansion_concrete = MI_on.iloc[0].values * ep_off_capacity_expansion.values.flatten()
ep_off_expansion_steel = MI_on.iloc[1].values * ep_off_capacity_expansion.values.flatten()
ep_off_expansion_copper = MI_on.iloc[2].values * ep_off_capacity_expansion.values.flatten()
ep_off_expansion_aluminium = MI_on.iloc[3].values * ep_off_capacity_expansion.values.flatten()
ep_off_expansion_fiberglass = MI_on.iloc[4].values * ep_off_capacity_expansion.values.flatten()
ep_off_expansion_neodymium = MI_on.iloc[5].values * ep_off_capacity_expansion.values.flatten()
ep_off_expansion_dysprosium = MI_on.iloc[6].values * ep_off_capacity_expansion.values.flatten()

# Repalcement #
sf_on_repalcement_concrete = sf_on_inflow_concrete - sf_on_expansion_concrete
sf_on_repalcement_steel = sf_on_inflow_steel - sf_on_expansion_steel
sf_on_repalcement_copper = sf_on_inflow_copper - sf_on_expansion_copper
sf_on_repalcement_aluminium = sf_on_inflow_aluminium - sf_on_expansion_aluminium
sf_on_repalcement_fiberglass = sf_on_inflow_fiberglass - sf_on_expansion_fiberglass
sf_on_repalcement_neodymium = sf_on_inflow_neodymium - sf_on_expansion_neodymium
sf_on_repalcement_dysprosium = sf_on_inflow_dysprosium - sf_on_expansion_dysprosium

sf_off_repalcement_concrete = sf_off_inflow_concrete - sf_off_expansion_concrete
sf_off_repalcement_steel = sf_off_inflow_steel - sf_off_expansion_steel
sf_off_repalcement_copper = sf_off_inflow_copper - sf_off_expansion_copper
sf_off_repalcement_aluminium = sf_off_inflow_aluminium - sf_off_expansion_aluminium
sf_off_repalcement_fiberglass = sf_off_inflow_fiberglass - sf_off_expansion_fiberglass
sf_off_repalcement_neodymium = sf_off_inflow_neodymium - sf_off_expansion_neodymium
sf_off_repalcement_dysprosium = sf_off_inflow_dysprosium - sf_off_expansion_dysprosium

fm_on_repalcement_concrete = fm_on_inflow_concrete - fm_on_expansion_concrete
fm_on_repalcement_steel = fm_on_inflow_steel - fm_on_expansion_steel
fm_on_repalcement_copper = fm_on_inflow_copper - fm_on_expansion_copper
fm_on_repalcement_aluminium = fm_on_inflow_aluminium - fm_on_expansion_aluminium
fm_on_repalcement_fiberglass = fm_on_inflow_fiberglass - fm_on_expansion_fiberglass
fm_on_repalcement_neodymium = fm_on_inflow_neodymium - fm_on_expansion_neodymium
fm_on_repalcement_dysprosium = fm_on_inflow_dysprosium - fm_on_expansion_dysprosium

fm_off_repalcement_concrete = fm_off_inflow_concrete - fm_off_expansion_concrete
fm_off_repalcement_steel = fm_off_inflow_steel - fm_off_expansion_steel
fm_off_repalcement_copper = fm_off_inflow_copper - fm_off_expansion_copper
fm_off_repalcement_aluminium = fm_off_inflow_aluminium - fm_off_expansion_aluminium
fm_off_repalcement_fiberglass = fm_off_inflow_fiberglass - fm_off_expansion_fiberglass
fm_off_repalcement_neodymium = fm_off_inflow_neodymium - fm_off_expansion_neodymium
fm_off_repalcement_dysprosium = fm_off_inflow_dysprosium - fm_off_expansion_dysprosium

ep_on_repalcement_concrete = ep_on_inflow_concrete - ep_on_expansion_concrete
ep_on_repalcement_steel = ep_on_inflow_steel - ep_on_expansion_steel
ep_on_repalcement_copper = ep_on_inflow_copper - ep_on_expansion_copper
ep_on_repalcement_aluminium = ep_on_inflow_aluminium - ep_on_expansion_aluminium
ep_on_repalcement_fiberglass = ep_on_inflow_fiberglass - ep_on_expansion_fiberglass
ep_on_repalcement_neodymium = ep_on_inflow_neodymium - ep_on_expansion_neodymium
ep_on_repalcement_dysprosium = ep_on_inflow_dysprosium - ep_on_expansion_dysprosium

ep_off_repalcement_concrete = ep_off_inflow_concrete - ep_off_expansion_concrete
ep_off_repalcement_steel = ep_off_inflow_steel - ep_off_expansion_steel
ep_off_repalcement_copper = ep_off_inflow_copper - ep_off_expansion_copper
ep_off_repalcement_aluminium = ep_off_inflow_aluminium - ep_off_expansion_aluminium
ep_off_repalcement_fiberglass = ep_off_inflow_fiberglass - ep_off_expansion_fiberglass
ep_off_repalcement_neodymium = ep_off_inflow_neodymium - ep_off_expansion_neodymium
ep_off_repalcement_dysprosium = ep_off_inflow_dysprosium - ep_off_expansion_dysprosium