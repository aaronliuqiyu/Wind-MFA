# This file contains helper functions that is used in the main script #
# The main purpose of having functions is to make the main script more readable and easier to modify #

# Packages need to be imported here and not the main script #
import pandas as pd
import numpy as np

# Import ODYM dynamic stock model #
from dynamic_stock_model import DynamicStockModel as DSM

# Interpolation function used to apply material efficiency and market shares #
def interpolate(efficiency, initial_value,market_share_on,market_share_off):
    empty = pd.DataFrame(index=range(14), columns=range(30))
    empty.columns = [list(range(2021,2051))] # Change header #
    # Mutiply the market shares to  #
    initial_value.loc['Neodymium on']  = initial_value.loc['Neodymium on'] * market_share_on
    initial_value.loc['Neodymium off'] = initial_value.loc['Neodymium off'] * market_share_off
    initial_value.loc['Dysprosium on'] = initial_value.loc['Dysprosium on'] * market_share_on
    initial_value.loc['Dysprosium off'] = initial_value.loc['Dysprosium off'] * market_share_off
    final_value = initial_value.values * efficiency.values
    initial_value = pd.DataFrame(initial_value.values)
    final_value = pd.DataFrame(final_value)


    empty.iloc[:,0] = initial_value # add initial year value to empty #
    empty.iloc[:,-1] = final_value # add final year value to empty #
    # Pandas gymnastics #
    empty = pd.DataFrame(data = empty.values, columns=[list(range(2021,2051))], dtype='float32')
    empty.interpolate(method='linear', inplace=True, axis=1)

    return empty

# define a function for calculating the stock driven inflow and outflow
def stock_driven(stock,lifetime):  # stock is the different type of roads in different regions
    shape_list = lifetime.iloc[:, 0]
    scale_list = lifetime.iloc[:, 1]

    DSMforward = DSM(t=list(stock.index), s=np.array(stock),
                     lt={'Type': 'Weibull', 'Shape': np.array(shape_list), 'Scale': np.array(scale_list)})

    out_sc, out_oc, out_i = DSMforward.compute_stock_driven_model(NegativeInflowCorrect=True)

    # sum up the total outflow and stock and add years as index #
    out_oc[out_oc < 0] = 0
    out_oc = out_oc.sum(axis=1)
    out_oc = pd.DataFrame(out_oc, index=np.unique(list(stock.index)))
    out_sc = out_sc.sum(axis=1)
    out_sc = pd.DataFrame(out_sc, index=np.unique(list(stock.index)))
    out_i = pd.DataFrame(out_i, index=np.unique(list(stock.index)))

    return out_oc, out_i

# define a function for calculating the inflow driven stock and outflow
def inflow_driven_stock(inflow,lifetime):  # stock is the different type of roads in different regions
    shape_list = lifetime.iloc[:, 0]
    scale_list = lifetime.iloc[:, 1]

    DSMforward = DSM(t=list(list(range(2021,2051))), i=np.array(inflow),
                     lt={'Type': 'Weibull', 'Shape': np.array(shape_list), 'Scale': np.array(scale_list)})

    out_sc = DSMforward.compute_s_c_inflow_driven()
    out_sc = out_sc.sum(axis=1)
    out_sc = pd.DataFrame(out_sc, index=list(range(2021,2051)))

    return out_sc

    
    