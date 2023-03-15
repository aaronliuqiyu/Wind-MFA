# This file contains helper functions that is used in the main script #
# The main purpose of having functions is to make the main script more readable and easier to modify #

# Packages need to be imported here and not the main script #
import pandas as pd

# Interpolation function used to apply material efficiency and market shares #
def interpolate(efficiency, initial_value,market_share_on,market_share_off):
    empty = pd.DataFrame(index=range(14), columns=range(31))
    empty.columns = [list(range(2020,2051))] # Change header #
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
    empty = pd.DataFrame(data = empty.values, columns=[list(range(2020,2051))], dtype='float32')
    empty.interpolate(method='linear', inplace=True, axis=1)

    return empty



    
    