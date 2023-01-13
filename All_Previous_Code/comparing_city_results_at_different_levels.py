import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

boston_level_1 = 1333
seattle_level_1 = 52
miami_level_1 = 1124
tuscon_level_1 = 343

boston_level_2 = 351
seattle_level_2 = 12
miami_level_2 = 299
tuscon_level_2 = 92

boston_level_3 = 46
seattle_level_3 = 0
miami_level_3 = 39
tuscon_level_3 = 13

#reading all LCA dataframes
LCA_level_3 = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\solar_LCA_column_level_3.csv')
LCA_level_3 = LCA_level_3.set_index('PAIRS polygon ID level 3', drop = True)
LCA_level_2 = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\level_2\solar_LCA_column_level_2.csv')
LCA_level_2 = LCA_level_2.set_index('PAIRS polygon ID level 2', drop = True)
LCA_level_1 = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\level_1\solar_LCA_column.csv')
LCA_level_1 = LCA_level_1.set_index('PAIRS polygon ID', drop = True)

#making the bar chart
labels = ['Boston', 'Seattle', 'Miami', 'Tuscon']
level_1 = [LCA_level_1.loc[boston_level_1, '0'], LCA_level_1.loc[seattle_level_1, '0'], LCA_level_1.loc[miami_level_1, '0'], LCA_level_1.loc[tuscon_level_1, '0']]
level_2 = [LCA_level_2.loc[boston_level_2, '0'], LCA_level_2.loc[seattle_level_2, '0'], LCA_level_2.loc[miami_level_2, '0'], LCA_level_2.loc[tuscon_level_2, '0']]
level_3 = [LCA_level_3.loc[boston_level_3, '0'], LCA_level_3.loc[seattle_level_3, '0'], LCA_level_3.loc[miami_level_3, '0'], LCA_level_3.loc[tuscon_level_3, '0']]

x = np.arange(len(labels))  # the label locations
width = 0.3  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width, level_1, width, label='level 1')
rects2 = ax.bar(x, level_2, width, label='level 2')
rects3 = ax.bar(x + width, level_3, width, label='level 3')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Emissions per power output (gCO2e/kWh)')
ax.set_title('Affect of aggregation on LCA values')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

fig.tight_layout()

plt.show()

#making the bar chart
labels = ['Boston', 'Seattle', 'Miami', 'Tuscon']
level_2_change = [(LCA_level_2.loc[boston_level_2, '0']  - LCA_level_1.loc[boston_level_1, '0']) / LCA_level_1.loc[boston_level_1, '0'] * 100, (LCA_level_2.loc[seattle_level_2, '0']  - LCA_level_1.loc[seattle_level_1, '0']) / LCA_level_1.loc[seattle_level_1, '0'] * 100, (LCA_level_2.loc[miami_level_2, '0']  - LCA_level_1.loc[miami_level_1, '0']) / LCA_level_1.loc[miami_level_1, '0'] * 100, (LCA_level_2.loc[tuscon_level_2, '0']  - LCA_level_1.loc[tuscon_level_1, '0']) / LCA_level_1.loc[tuscon_level_1, '0'] * 100]
level_3_change = [(LCA_level_3.loc[boston_level_3, '0']  - LCA_level_1.loc[boston_level_1, '0']) / LCA_level_1.loc[boston_level_1, '0'] * 100, (LCA_level_3.loc[seattle_level_3, '0']  - LCA_level_1.loc[seattle_level_1, '0']) / LCA_level_1.loc[seattle_level_1, '0'] * 100, (LCA_level_3.loc[miami_level_3, '0']  - LCA_level_1.loc[miami_level_1, '0']) / LCA_level_1.loc[miami_level_1, '0'] * 100, (LCA_level_3.loc[tuscon_level_3, '0']  - LCA_level_1.loc[tuscon_level_1, '0']) / LCA_level_1.loc[tuscon_level_1, '0'] * 100]

x = np.arange(len(labels))  # the label locations
width = 0.3  # the width of the bars

fig, ax = plt.subplots()
rects2_change = ax.bar(x - width/2, level_2_change, width, label='level 2 change')
rects3_change = ax.bar(x + width/2, level_3_change, width, label='level 3 change')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Change in LCA value from aggregation (%)')
ax.set_title('Affect of aggregation')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

plt.axhline(y=0, color='black', linestyle='dashed', linewidth=1)

fig.tight_layout()

plt.show()
