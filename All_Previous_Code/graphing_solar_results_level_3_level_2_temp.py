import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy.stats import norm

lcm_height = 300
lcm_width = 160

solar_data = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\tracking_solar_output_level_3_and_temp_level_2.csv', index_col = 0)

#Plot yearly sum in a heat map
yearly_sum = solar_data.sum(axis = 1) #sum along each row
yearly_sum = yearly_sum.replace(0, np.nan)

#change the shape to be the way it should be
yearly_sum_np = yearly_sum.to_numpy()
correct_shape_np_final = np.reshape(yearly_sum_np, (lcm_height, lcm_width), order = 'F')
correct_shape_np_final_GWh = correct_shape_np_final / 1000000000

#make a heatmap out of
plt.imshow(correct_shape_np_final_GWh, cmap='plasma', aspect = 0.25) #plasma is good for solar
plt.colorbar()
plt.title('Solar yearly sum output level 3 and 2 temp (GWh)')
plt.clim(65, 100)
plt.show()

correct_shape_np_final_GWh_df = pd.DataFrame(correct_shape_np_final_GWh)
correct_shape_np_final_GWh_df.to_csv('solar_power_output_sum_GWh_level_3_level_2_temp.csv')

fig = plt.figure(figsize=(5, 3), tight_layout = True)
num_bins = 100
n, bins, patches = plt.hist(yearly_sum_np/1000000000, num_bins, density = 1, color = 'black', alpha = 0.7) #alpha is color density
plt.xlabel('Energy output (GWh)')
plt.ylabel('Fraction of locations with output')
plt.ylim(ymin=0, ymax = 0.15)
plt.xlim(xmin=65, xmax = 100)
plt.title('Solar yearly sum output distribution level 3 and 2 temp')#, fontweight="bold")


yearly_sum_values_only = yearly_sum_np[~np.isnan(yearly_sum_np)]
(mu, sigma) = norm.fit(yearly_sum_values_only/1000000000)
y = norm.pdf(bins, mu, sigma) * sum(n * np.diff(bins))
plt.plot(bins, y, '-', linewidth = 1, label = 'normalized curve')
plt.legend()

plt.show()

print('hi amanda. combo done with temp level 2')