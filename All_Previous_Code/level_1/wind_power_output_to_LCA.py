import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import statistics

rating = 2550 #kWp
wind_data = pd.read_csv('/Users/mirandaliu/Documents/GitHub/ibm-pairs/Data/Solar_and_Wind/tracking_wind_output.csv')
wind_data = wind_data.set_index('PAIRS polygon ID', drop = True)
wind_transposed = wind_data.T
yearly_sum = wind_transposed.sum() #Wh/yr

#calculating CF
optimum_power_output = 2.55 * 1000000 * 366 * 24

cf = yearly_sum / optimum_power_output

print('max cf = ')
print(cf.max())

print('min cf = ')
print(cf.min())

electricity_total = cf * rating * 8760 * 30 #kW
#electricity_total = pd.Series(0.4 * rating * 8760 * 30, index = cf.index)
"""
rating = 2500 #kWp
lifetime = 30 #years
hours_per_year = 8760 #hour/yr
total_electricity_output = lifetime * yearly_sum
GWP = 6.2 # g CO2e/kWh
total_emissions = total_electricity_output * GWP
"""
emissions_intensity = 520862 #g CO2/kWp
emissions_per_turbine = emissions_intensity * rating #emissions/turbine
LCA = emissions_per_turbine / electricity_total

LCA_shape_df = pd.DataFrame(index = range(1, 1451), columns = ['LCA'])
LCA_shape_df['LCA'] = LCA
LCA_shape_np = LCA_shape_df.to_numpy()
LCA_shape_np_final = np.reshape(LCA_shape_np, (25, 58), order = 'F')

#make a heatmap out of
hot_reversed = matplotlib.cm.get_cmap('hot_r')
plt.imshow(LCA_shape_np_final, cmap=hot_reversed) #plasma is good for solar
plt.colorbar()
# plt.clim(1.3, 2)
plt.title('Wind LCA (gCO2/kWh)')
plt.show()

LCA.to_csv('/Users/mirandaliu/Documents/GitHub/ibm-pairs/Data/Solar_and_Wind/wind_LCA.csv')
