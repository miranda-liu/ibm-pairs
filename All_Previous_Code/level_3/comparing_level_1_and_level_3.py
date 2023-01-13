import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd
import scipy
from scipy.stats import norm

#importing dataframes
solar_power_output_level_1 = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\level_1\solar_power_output_sum_GWh.csv')
solar_power_output_level_1 = solar_power_output_level_1.drop(columns=solar_power_output_level_1.columns[0])
solar_power_output_level_3 = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\level_3\solar_power_output_sum_GWh_level_3.csv')
solar_power_output_level_3 = solar_power_output_level_3.drop(columns=solar_power_output_level_3.columns[0])

#recording dimensions
solar_level_1_width = solar_power_output_level_1.shape[1]
solar_level_1_height = solar_power_output_level_1.shape[0]

solar_level_3_width = solar_power_output_level_3.shape[1]
solar_level_3_height = solar_power_output_level_3.shape[0]

#finding LCM
#height
for i in range(1, solar_level_3_height + 1):
    if i * solar_level_1_height % solar_level_3_height == 0:
        lcm_height = i * solar_level_1_height
        break

#width
for j in range(1, solar_level_3_width):
    if j * solar_level_1_width % solar_level_3_width == 0:
        lcm_width = j * solar_level_1_width
        break

error_at_high_res = np.empty([lcm_height, lcm_width])

solar_power_output_level_3_np = solar_power_output_level_3.to_numpy()
solar_power_level_3_high_res = np.repeat(solar_power_output_level_3_np, lcm_width/solar_level_3_width, axis = 1)
solar_power_level_3_high_res = np.repeat(solar_power_level_3_high_res, lcm_height/solar_level_3_height, axis = 0)

solar_power_output_level_1_np = solar_power_output_level_1.to_numpy()
solar_power_level_1_high_res = np.repeat(solar_power_output_level_1_np, lcm_width/solar_level_1_width, axis = 1)
solar_power_level_1_high_res = np.repeat(solar_power_level_1_high_res, lcm_height/solar_level_1_height, axis = 0)

error_at_high_res = (solar_power_level_3_high_res - solar_power_level_1_high_res) / solar_power_level_1_high_res * 100
#make a heatmap out of
plt.imshow(error_at_high_res, cmap='seismic_r') #'seismic_r'
plt.colorbar()
plt.title('Percent error in energy output annual sum')
plt.clim(-10, 10)
plt.show()

#making a histogram with normalized curve
error_at_high_res_column = np.reshape(error_at_high_res, (lcm_width * lcm_height))
error_at_high_res_column_values_only = error_at_high_res_column[~np.isnan(error_at_high_res_column)]
fig = plt.figure(figsize=(5, 3), tight_layout = True)
num_bins = 100
n, bins, patches = plt.hist(error_at_high_res_column_values_only, num_bins, density = 1, color = 'black', alpha = 0.7) #alpha is color density
plt.xlabel('Percent error')
plt.ylabel('Frequency')
plt.ylim(ymin=0, ymax = 0.35)
plt.xlim(xmin=-10, xmax = 10)
plt.title('Error distribution level 3')#, fontweight="bold")

(mu, sigma) = norm.fit(error_at_high_res_column_values_only)
y = norm.pdf(bins, mu, sigma) * sum(n * np.diff(bins))
plt.plot(bins, y, '-', linewidth = 1, label = 'normalized curve')
plt.legend()

plt.show()


print('all done :-)')