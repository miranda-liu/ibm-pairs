import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import statistics

solar_data = pd.read_csv('/Users/mirandaliu/Documents/GitHub/ibm-pairs/Data/Solar_and_Wind/tracking_solar_output.csv')
solar_data = solar_data.set_index('PAIRS polygon ID', drop = True)
solar_transposed = solar_data.T
yearly_sum = solar_transposed.sum() #Wh/yr

emissions = 7.23 * pow(10, 5) / 570 #gCO2/W
size = 50 * pow(10, 6) #W
#emissions = 45.1 / 1000 #gCO2 / m^2
#size = 190000 #m^2

emissions_normalized = emissions * size #gCO2
lifetime = 30 #yr
LCA = emissions_normalized / yearly_sum / lifetime * 1000 #gCO2/kWh

LCA.to_csv('/Users/mirandaliu/Documents/GitHub/ibm-pairs/Data/Solar_and_Wind/solar_LCA_column.csv')

# via extrapolation
#calculating CF
optimum_power_output = 50000000 * 366 * 24

cf = yearly_sum / optimum_power_output*100
""" 
LCA = 665.73 * cf**(-1)
"""

LCA_shape_df = pd.DataFrame(index = range(1, 1451), columns = ['LCA'])
LCA_shape_df['LCA'] = LCA
LCA_shape_np = LCA_shape_df.to_numpy()
LCA_shape_np_final = np.reshape(LCA_shape_np, (25, 58), order = 'F')

#make a heatmap out of
hot_reversed = matplotlib.cm.get_cmap('hot_r')
plt.imshow(LCA_shape_np_final, cmap=hot_reversed) #plasma is good for solar
plt.colorbar()
#plt.clim(25, 45)
plt.title('Solar LCA (gCO2/kWh)')
plt.show()

LCA_shape_df_final = pd.DataFrame(LCA_shape_np_final)
LCA_shape_df_final.to_csv('/Users/mirandaliu/Documents/GitHub/ibm-pairs/Data/Solar_and_Wind/solar_LCA.csv')

#comparing SESAME to PAIRS results
boston_PAIRS = float(LCA.loc[1333])
boston_SESAME = float(35.0)

seattle_PAIRS = float(LCA.loc[52])
seattle_SESAME = float(42)

miami_PAIRS = float(LCA.loc[1124])
miami_SESAME = float(32)

tuscon_PAIRS = float(LCA.loc[343])
tuscon_SESAME = float(26)

labels = ['Boston', 'Seattle', 'Miami', 'Tuscon']
PAIRS = [boston_PAIRS, seattle_PAIRS, miami_PAIRS, tuscon_PAIRS]
SESAME = [boston_SESAME, seattle_SESAME, miami_SESAME, tuscon_SESAME]

x = np.arange(len(labels))  # the label locations
width = 0.3  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, PAIRS, width, label='PAIRS')
rects2 = ax.bar(x + width/2, SESAME, width, label='SESAME')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Emissions per power output (gCO2e/kWh)')
ax.set_title('LCA by region')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

fig.tight_layout()

plt.show()


#comparing differences SESAME to PAIRS (in cfs and LCA)
boston_cf_difference = abs(float(cf.loc[1333]) - 15.6) / statistics.mean([cf.loc[1333], 15.6]) * 100
boston_LCA_difference = abs(boston_PAIRS - boston_SESAME) / statistics.mean([boston_PAIRS, boston_SESAME]) * 100

seattle_cf_difference = abs(float(cf.loc[52]) - 12.69) / statistics.mean([cf.loc[52], 12.69]) * 100
seattle_LCA_difference = abs(seattle_PAIRS - seattle_SESAME) / statistics.mean([seattle_PAIRS, seattle_SESAME]) * 100

miami_cf_difference = abs(float(cf.loc[1124]) - 16.72) / statistics.mean([cf.loc[1124], 16.72]) * 100
miami_LCA_difference = abs(miami_PAIRS - miami_SESAME) / statistics.mean([miami_PAIRS, miami_SESAME]) * 100

tuscon_cf_difference = abs(float(cf.loc[343]) - 20.53) / statistics.mean([cf.loc[343], 20.53]) * 100
tuscon_LCA_difference = abs(tuscon_PAIRS - tuscon_SESAME) / statistics.mean([tuscon_PAIRS, tuscon_SESAME]) * 100

labels = ['Boston', 'Seattle', 'Miami', 'Tuscon']
LCA_difference = [boston_LCA_difference, seattle_LCA_difference, miami_LCA_difference, tuscon_LCA_difference]
cf_difference = [boston_cf_difference, seattle_cf_difference, miami_cf_difference, tuscon_cf_difference]

x = np.arange(len(labels))  # the label locations
width = 0.3  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, LCA_difference, width, label='LCA')
rects2 = ax.bar(x + width/2, cf_difference, width, label='Capacity factor')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Percent difference')
ax.set_title('Variability in PAIRS vs SESAME analysis by region')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

fig.tight_layout()

plt.show()





print('solar power output to LCA is done :)')


