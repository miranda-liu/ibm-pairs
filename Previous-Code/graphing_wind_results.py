import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# pwd to print absolute path
wind_data = pd.read_csv('/Users/mirandaliu/Documents/GitHub/ibm-pairs/All_Previous_Code/tracking_wind_output.csv')
wind_data = wind_data.set_index('PAIRS polygon ID', drop = True)
wind_transposed = wind_data.T

#plot all location trends over a year.  line graph with 931 lines on it
ax = wind_transposed.plot(legend=False)
ax.set_xlabel('Time into year (h)', fontsize=12)
ax.set_ylabel('Wind power output (W)', fontsize=12)
ax.set_xlim([0, 8783])
ax.set_ylim(0)
plt.show()

# plot cities for two weeks.
start_time = 3000
end_time = 3168

x = range(start_time, end_time)

boston_wind_MW = wind_transposed[1333]/1000000
seattle_wind_MW = wind_transposed[52]/1000000
tampa_wind_MW = wind_transposed[1072]/1000000
houston_wind_MW = wind_transposed[745]/1000000
denver_wind_MW = wind_transposed[485]/1000000

plt.plot(x, boston_wind_MW[start_time:end_time], label = 'Boston')
plt.plot(x, seattle_wind_MW[start_time:end_time], label = 'Seattle')
plt.plot(x, tampa_wind_MW[start_time:end_time], label = 'Tampa')
plt.plot(x, houston_wind_MW[start_time:end_time], label = 'Houston')
plt.plot(x, denver_wind_MW[start_time:end_time], label = 'Denver')
plt.legend()
plt.xlim(start_time, end_time)
plt.ylim(0)
plt.xlabel('Hours into 2020')
plt.ylabel('Wind power output (MW)')
plt.show()

#Plot yearly sum in a heat map
yearly_sum = wind_transposed.sum()

#change the shape to be the way it should be
correct_shape_df = pd.DataFrame(index = range(1, 1451), columns = ['yearly_sum'])
correct_shape_df['yearly_sum'] = yearly_sum
correct_shape_np = correct_shape_df.to_numpy()
correct_shape_np_final = np.reshape(correct_shape_np, (25, 58), order = 'F')
correct_shape_np_final_GWh = correct_shape_np_final / 1000000000

#make a heatmap out of
plt.imshow(correct_shape_np_final_GWh, cmap='viridis') #plasma is good for solar
plt.colorbar()
plt.title('Yearly sum of wind energy output (GWh)')
plt.show()

#Plot ystandard deviation and coefficient of variance in a heat map
std = wind_data.std(axis = 1)

#change the shape to be the way it should be
std_shape_df = pd.DataFrame(index = range(1, 1451), columns = ['standard_deviation'])
std_shape_df['standard_deviation'] = std
std_shape_np = std_shape_df.to_numpy()
std_shape_np_final = np.reshape(std_shape_np, (25, 58), order = 'F')

#make a heatmap out of
plt.imshow(std_shape_np_final, cmap='viridis') #plasma is good for solar
plt.colorbar()
plt.title('Standard deviation of wind energy output (Wh)')
plt.show()

mean = wind_data.mean(axis = 1)
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
plt.title('Coefficient of variation of wind energy output')
plt.show()

#comparing pps "gen_shapes" to PAIRS results:
boston_index = 1333
seattle_index = 52
houston_index = 745
atlanta_index = 1016
minneapolis_index = 780
sanfrancisco_index = 62
tuscon_index = 343
oklahomacity_index = 689

#calculating CFs at all points
optimum_power_output = 2550000 * 366 * 24
cf = yearly_sum / optimum_power_output * 100

pps_boston_cfs = np.array([0.424962998, 0.404892336, 0.427098861, 0.45009757, 0.413671653, 0.392525311, 0.405490577]) * 100
PAIRS_boston = cf.loc[boston_index]

pps_seattle_cfs = np.array([0.257376989, 0.252323736, 0.233281151, 0.260364482, 0.263008424, 0.276037874, 0.209631166]) * 100
PAIRS_seattle = cf.loc[seattle_index]

pps_houston_cfs = np.array([0.316103362, 0.376608147, 0.369478258, 0.369364732, 0.40420927, 0.342442126, 0.357217638]) * 100
PAIRS_houston = cf.loc[houston_index]

pps_atlanta_cfs = np.array([0.309853611, 0.331548418, 0.310317797, 0.298879189, 0.3215505, 0.276169978, 0.30973271]) * 100
PAIRS_atlanta = cf.loc[atlanta_index]

pps_minneapolis_cfs = np.array([0.434410201, 0.408013958, 0.389019882, 0.386534483, 0.398401036, 0.395516891, 0.409251173]) * 100
PAIRS_minneapolis = cf.loc[minneapolis_index]

pps_sanfrancisco_cfs = np.array([0.2737314, 0.265879277, 0.257401579, 0.261030189, 0.245273873, 0.263609324, 0.24251378]) * 100
PAIRS_sanfrancisco = cf.loc[sanfrancisco_index]

pps_tuscon_cfs = np.array([0.205516685, 0.233128489, 0.204291089, 0.221328522, 0.202067879, 0.188062108, 0.216384075]) * 100
PAIRS_tuscon = cf.loc[tuscon_index]

pps_oklahomacity_cfs = np.array([0.414393353, 0.482831747, 0.471037717, 0.459719826, 0.489208485, 0.465930777, 0.459860936]) * 100
PAIRS_oklahomacity = cf.loc[oklahomacity_index]

pps_boston = np.mean(pps_boston_cfs)
pps_seattle = np.mean(pps_seattle_cfs)
pps_houston = np.mean(pps_houston_cfs)
pps_atlanta = np.mean(pps_atlanta_cfs)
pps_minneapolis = np.mean(pps_minneapolis_cfs)
pps_sanfrancisco = np.mean(pps_sanfrancisco_cfs)
pps_tuscon = np.mean(pps_tuscon_cfs)
pps_oklahomacity = np.mean(pps_oklahomacity_cfs)

pps_boston_std = max((max(pps_boston_cfs) - pps_boston), (pps_boston - min(pps_boston_cfs)))
pps_seattle_std = max((max(pps_seattle_cfs) - pps_seattle), (pps_seattle - min(pps_seattle_cfs)))
pps_houston_std = max((max(pps_houston_cfs) - pps_houston), (pps_houston - min(pps_houston_cfs)))
pps_atlanta_std = max((max(pps_atlanta_cfs) - pps_atlanta), (pps_atlanta - min(pps_atlanta_cfs)))
pps_minneapolis_std = max((max(pps_minneapolis_cfs) - pps_minneapolis), (pps_minneapolis - min(pps_minneapolis_cfs)))
pps_sanfrancisco_std = max((max(pps_sanfrancisco_cfs) - pps_sanfrancisco), (pps_sanfrancisco - min(pps_sanfrancisco_cfs)))
pps_tuscon_std = max((max(pps_tuscon_cfs) - pps_tuscon), (pps_tuscon - min(pps_tuscon_cfs)))
pps_oklahomacity_std = max((max(pps_oklahomacity_cfs) - pps_oklahomacity), (pps_oklahomacity - min(pps_oklahomacity_cfs)))

error = [pps_boston_std, pps_seattle_std, pps_houston_std, pps_atlanta_std, pps_minneapolis_std, pps_sanfrancisco_std, pps_tuscon_std, pps_oklahomacity_std]

labels = ['Boston', 'Seattle', 'Houston', 'Atlanta', 'Minneapolis', 'San Francisco', 'Tuscon', 'Oklahoma City']
pps = [pps_boston, pps_seattle, pps_houston, pps_atlanta, pps_minneapolis, pps_sanfrancisco, pps_tuscon, pps_oklahomacity]
PAIRS = [PAIRS_boston, PAIRS_seattle, PAIRS_houston, PAIRS_atlanta, PAIRS_minneapolis, PAIRS_sanfrancisco, PAIRS_tuscon, PAIRS_oklahomacity]

x = np.arange(len(labels))  # the label locations
width = 0.3  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, pps, width, yerr = error, label='Power Greenfield')
rects2 = ax.bar(x + width/2, PAIRS, width, label='PAIRS')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('CF (%)')
ax.set_title('CF comparison by region')
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation = 45)
ax.yaxis.grid(True)
ax.legend()

fig.tight_layout()

plt.show()

print('graphing wind results done :)')
