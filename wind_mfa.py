# Import required packages #
# These packages needs to be installed and imported for the script to run #
import pandas as pd
import numpy as np
import os

# Import ODYM dynamic stock model #
# This package is used to carry out the MFA calculations #
# ODYM has other modules, but I am currently only using the dynamic stock model module, see https://github.com/IndEcol/ODYM for detailed documentation#
from dynamic_stock_model import DynamicStockModel as DSM

# Set option so that pandas does not create a copy of the dataframe #
pd.set_option('mode.chained_assignment', None)