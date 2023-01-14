import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy.stats import norm

solar_data = pd.read_csv('/Users/mirandaliu/Documents/GitHub/ibm-pairs/All_Previous_code/level_1/tracking_solar_output.csv')
solar_data = solar_data.set_index('PAIRS polygon ID', drop = True)
solar_transposed = solar_data.T

#plot all location trends over a year.  line graph with 931 lines on it
ax = solar_transposed.plot(legend=False)
ax.set_xlabel('Time into year (h)', fontsize=12)
ax.set_ylabel('Solar power output (W)', fontsize=12)
ax.set_xlim([0, 8783])
ax.set_ylim(0)
plt.show()


# plot cities for two weeks.
start_time = 3000
end_time = 3168

x = range(start_time, end_time)

boston_solar_MW = solar_transposed[1333]/1000000
seattle_solar_MW = solar_transposed[52]/1000000
tampa_solar_MW = solar_transposed[1072]/1000000
houston_solar_MW = solar_transposed[745]/1000000
denver_solar_MW = solar_transposed[485]/1000000

plt.plot(x, boston_solar_MW[start_time:end_time], label = 'Boston')
plt.plot(x, seattle_solar_MW[start_time:end_time], label = 'Seattle')
plt.plot(x, tampa_solar_MW[start_time:end_time], label = 'Tampa')
plt.plot(x, houston_solar_MW[start_time:end_time], label = 'Houston')
plt.plot(x, denver_solar_MW[start_time:end_time], label = 'Denver')
plt.legend()
plt.xlim(start_time, end_time)
plt.ylim(0)
plt.xlabel('Hours into 2020')
plt.ylabel('Solar power output (MW)')
plt.show()


#Plot yearly sum in a heat map
yearly_sum = solar_transposed.sum()

#change the shape to be the way it should be
correct_shape_df = pd.DataFrame(index = range(1, 1451), columns = ['yearly_sum'])
correct_shape_df['yearly_sum'] = yearly_sum
correct_shape_np = correct_shape_df.to_numpy()
correct_shape_np_final = np.reshape(correct_shape_np, (25, 58), order = 'F')
correct_shape_np_final_GWh = correct_shape_np_final/ 1000000000

#make a heatmap out of
plt.imshow(correct_shape_np_final_GWh, cmap='plasma') #plasma is good for solar
plt.colorbar()
plt.title('Solar yearly sum output level 1 (GWh)')
plt.clim(65, 100)
plt.show()

correct_shape_np_final_GWh_df = pd.DataFrame(correct_shape_np_final_GWh)
correct_shape_np_final_GWh_df.to_csv('solar_power_output_sum_GWh.csv')

fig = plt.figure(figsize=(5, 3), tight_layout = True)
num_bins = 100
n, bins, patches = plt.hist(yearly_sum/1000000000, num_bins, density = 1, color = 'black', alpha = 0.7) #alpha is color density
#plt.xlabel('Energy output (GWh)')
plt.ylabel('Fraction of locations with output')
plt.ylim(ymin=0, ymax = 0.15)
plt.xlim(xmin=65, xmax = 100)
plt.title('Solar yearly sum output distribution level 1')#, fontweight="bold")


intermediate = yearly_sum/1000000000
(mu, sigma) = norm.fit(intermediate)
y = norm.pdf(bins, mu, sigma) * sum(n * np.diff(bins))
plt.plot(bins, y, '-', linewidth = 1, label = 'normalized curve')
plt.legend()
plt.show()


#Plot ystandard deviation and coefficient of variance in a heat map
std = solar_data.std(axis = 1)

#change the shape to be the way it should be
std_shape_df = pd.DataFrame(index = range(1, 1451), columns = ['standard_deviation'])
std_shape_df['standard_deviation'] = std
std_shape_np = std_shape_df.to_numpy()
std_shape_np_final = np.reshape(std_shape_np, (25, 58), order = 'F')

#make a heatmap out of
plt.imshow(std_shape_np_final, cmap='plasma') #plasma is good for solar
plt.colorbar()
plt.title('Standard deviation of solar energy output (Wh)')
plt.show()


mean = solar_data.mean(axis = 1)
cov = std/mean

#change the shape to be the way it should be
cov_shape_df = pd.DataFrame(index = range(1, 1451), columns = ['standard_deviation'])
cov_shape_df['standard_deviation'] = cov
cov_shape_np = cov_shape_df.to_numpy()
cov_shape_np_final = np.reshape(cov_shape_np, (25, 58), order = 'F')

#make a heatmap out of
plt.imshow(cov_shape_np_final, cmap='rainbow') #plasma is good for solar
plt.colorbar()
plt.clim(1.3, 2)
plt.title('Coefficient of variation of solar energy output')
plt.show()

print('hi amanda')
