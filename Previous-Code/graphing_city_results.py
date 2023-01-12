import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

solar_LCOE = pd.read_csv('/Users/mirandaliu/Documents/GitHub/ibm-pairs/Previous-Code/solar_LCOE_column.csv')
solar_LCOE = solar_LCOE.set_index('PAIRS polygon ID', drop = True)
# wind_LCOE = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\level_1\wind_LCOE_column.csv')
wind_LCOE = pd.read_csv('/Users/mirandaliu/Documents/GitHub/ibm-pairs/Previous-Code/wind_LCOE_column.csv')
wind_LCOE = wind_LCOE.set_index('PAIRS polygon ID', drop = True)

solar_LCOE_series = solar_LCOE.squeeze()
wind_LCOE_series = wind_LCOE.squeeze()

boston_solar = float(solar_LCOE.loc[1333])
boston_wind = float(wind_LCOE.loc[1333])

seattle_solar = float(solar_LCOE.loc[52])
seattle_wind = float(wind_LCOE.loc[52])

tampa_solar = float(solar_LCOE.loc[1072])
tampa_wind = float(wind_LCOE.loc[1072])

houston_solar = float(solar_LCOE.loc[745])
houston_wind = float(wind_LCOE.loc[745])

denver_solar = float(solar_LCOE.loc[485])
denver_wind = float(wind_LCOE.loc[485])

labels = ['solar', 'wind']
boston = [boston_solar, boston_wind]
seattle = [seattle_solar, seattle_wind]
tampa = [tampa_solar, tampa_wind]
houston = [houston_solar, houston_wind]
denver = [denver_solar, denver_wind]

x = np.arange(len(labels))  # the label locations
width = 0.15  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x, boston, width, label='Boston')
rects2 = ax.bar(x + width, seattle, width, label='Seattle')
rects3 = ax.bar(x + 2*width, tampa, width, label='Tampa')
rects4 = ax.bar(x - 2*width, houston, width, label='Houston')
rects5 = ax.bar(x - width, denver, width, label='Denver')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Cost of electricity ($/MWh)')
ax.set_title('TEA by region (new)')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

fig.tight_layout()

plt.show()
print("with new data: ")
print('boston LCOE = ' + str(boston_wind))