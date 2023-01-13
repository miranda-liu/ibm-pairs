import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
import scipy
from scipy.stats import norm

#setting known dimensions from previvous code
solar_level_1_height = 25
solar_level_1_width = 58

solar_level_2_height = 12
solar_level_2_width = 32

lcm_height = 300
lcm_width = 928

#initializing datatime format
DATE_TIME_FORMAT = '%m_%d_%Y' + 'T' '%H_%M_%S'
start_datetime = datetime.strptime('01_01_2020T01_00_00', DATE_TIME_FORMAT)
end_datetime = datetime.strptime('12_31_2020T23_00_00', DATE_TIME_FORMAT)
timedelta_index = pd.date_range(start=start_datetime, end=end_datetime, periods=8783) # 24 extra hours hecause 2020 was a leap year
time_in_correct_format = timedelta_index.strftime(DATE_TIME_FORMAT)

#for the length of the time_in_correct_format object, loop through each element
for i in range(8783):
    print(i)
    current_timestamp = time_in_correct_format[i]

    #temp data
    temp_K_level_1 = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated//' + 'Global weather (ERA5)-Temperature-' + current_timestamp + '.csv')  # K
    temp_K_level_1 = temp_K_level_1.set_index('PAIRS polygon ID', drop=True)
    temp_K_level_1.columns = ['count', 'min', 'max', 'mean', '2nd moment']
    temp_K_level_1 = temp_K_level_1['mean']
    temp_K_level_1 = pd.DataFrame(temp_K_level_1, columns=['mean'])
    temp_K_level_1_shape_df = pd.DataFrame(index = range(1, 1451), columns = ['Values'])
    temp_K_level_1_shape_df['Values'] = temp_K_level_1
    temp_K_level_1_shape_np = temp_K_level_1_shape_df.to_numpy()
    temp_K_level_1_np_final = np.reshape(temp_K_level_1_shape_np, (solar_level_1_height, solar_level_1_width), order='F')

    temp_K_level_2 = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated_level_2//' + 'Global weather (ERA5)-Temperature-' + current_timestamp + 'level_2.csv')  # K
    temp_K_level_2.columns = ['PAIRS polygon ID level 2', 'averaged value']
    temp_K_level_2 = temp_K_level_2.set_index('PAIRS polygon ID level 2', drop=True)
    temp_K_level_2 = temp_K_level_2.iloc[:, 0]
    temp_K_level_2 = pd.DataFrame(temp_K_level_2)
    temp_K_level_2_shape_df = pd.DataFrame(index = range(solar_level_2_height * solar_level_2_width), columns = ['Values'])
    temp_K_level_2_shape_df['Values'] = temp_K_level_2
    temp_K_level_2_shape_np = temp_K_level_2_shape_df.to_numpy()
    temp_K_level_2_np_final = np.reshape(temp_K_level_2_shape_np, (solar_level_2_height, solar_level_2_width), order='F')

    temp_K_level_2_high_res = np.repeat(temp_K_level_2_np_final, lcm_width / solar_level_2_width, axis=1)
    temp_K_level_2_high_res = np.repeat(temp_K_level_2_high_res, lcm_height / solar_level_2_height, axis=0)

    temp_K_level_1_high_res = np.repeat(temp_K_level_1_np_final, lcm_width / solar_level_1_width, axis=1)
    temp_K_level_1_high_res = np.repeat(temp_K_level_1_high_res, lcm_height / solar_level_1_height, axis=0)

    temp_K_level_2_df_final = pd.DataFrame(temp_K_level_2_high_res)
    temp_K_level_1_df_final = pd.DataFrame(temp_K_level_1_high_res)

    if i == 0:
        temp_error_sum_high_res = abs(temp_K_level_2_df_final - temp_K_level_1_df_final)
    else:
        temp_error_sum_high_res += abs(temp_K_level_2_df_final - temp_K_level_1_df_final)


    wind_level_1 = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated//' + 'Global weather (ERA5)-wind value-' + current_timestamp + '.csv')  # K
    wind_level_1 = wind_level_1.set_index('PAIRS polygon ID', drop=True)
    wind_level_1 = pd.DataFrame(wind_level_1)
    wind_level_1_shape_df = pd.DataFrame(index = range(1, 1451), columns = ['Values'])
    wind_level_1_shape_df['Values'] = wind_level_1
    wind_level_1_shape_np = wind_level_1_shape_df.to_numpy()
    wind_level_1_np_final = np.reshape(wind_level_1_shape_np, (solar_level_1_height, solar_level_1_width), order='F')

    wind_level_2 = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated_level_2//' + 'Global weather (ERA5)-wind value-' + current_timestamp + 'level_2.csv')  # K
    wind_level_2.columns = ['PAIRS polygon ID level 2', 'averaged value']
    wind_level_2 = wind_level_2.set_index('PAIRS polygon ID level 2', drop=True)
    wind_level_2_shape_df = pd.DataFrame(index = range(solar_level_2_height * solar_level_2_width), columns = ['Values'])
    wind_level_2_shape_df['Values'] = wind_level_2
    wind_level_2_shape_np = wind_level_2_shape_df.to_numpy()
    wind_level_2_np_final = np.reshape(wind_level_2_shape_np, (solar_level_2_height, solar_level_2_width), order='F')

    wind_level_2_high_res = np.repeat(wind_level_2_np_final, lcm_width / solar_level_2_width, axis=1)
    wind_level_2_high_res = np.repeat(wind_level_2_high_res, lcm_height / solar_level_2_height, axis=0)

    wind_level_1_high_res = np.repeat(wind_level_1_np_final, lcm_width / solar_level_1_width, axis=1)
    wind_level_1_high_res = np.repeat(wind_level_1_high_res, lcm_height / solar_level_1_height, axis=0)

    wind_level_2_df_final = pd.DataFrame(wind_level_2_high_res)
    wind_level_1_df_final = pd.DataFrame(wind_level_1_high_res)

    if i == 0:
        wind_error_sum_high_res = abs(wind_level_2_df_final - wind_level_1_df_final)
    else:
        wind_error_sum_high_res += abs(wind_level_2_df_final - wind_level_1_df_final)

    #I
    I_level_1 = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated//' + 'Global weather (ERA5)-Solar radiation-' + current_timestamp + '.csv')  # K
    I_level_1 = I_level_1.set_index('PAIRS polygon ID', drop=True)
    I_level_1.columns = ['count', 'min', 'max', 'mean', '2nd moment']
    I_level_1 = I_level_1['mean']
    I_level_1 = pd.DataFrame(I_level_1, columns=['mean'])
    I_level_1_shape_df = pd.DataFrame(index = range(1, 1451), columns = ['Values'])
    I_level_1_shape_df['Values'] = I_level_1
    I_level_1_shape_np = I_level_1_shape_df.to_numpy()
    I_level_1_np_final = np.reshape(I_level_1_shape_np, (solar_level_1_height, solar_level_1_width), order='F')

    I_level_2 = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated_level_2//' + 'Global weather (ERA5)-Solar radiation-' + current_timestamp + 'level_2.csv')  # K
    I_level_2.columns = ['PAIRS polygon ID level 2', 'averaged value']
    I_level_2 = I_level_2.set_index('PAIRS polygon ID level 2', drop=True)
    I_level_2 = I_level_2.iloc[:, 0]
    I_level_2 = pd.DataFrame(I_level_2)
    I_level_2_shape_df = pd.DataFrame(index = range(solar_level_2_height * solar_level_2_width), columns = ['Values'])
    I_level_2_shape_df['Values'] = I_level_2
    I_level_2_shape_np = I_level_2_shape_df.to_numpy()
    I_level_2_np_final = np.reshape(I_level_2_shape_np, (solar_level_2_height, solar_level_2_width), order='F')

    I_level_2_high_res = np.repeat(I_level_2_np_final, lcm_width / solar_level_2_width, axis=1)
    I_level_2_high_res = np.repeat(I_level_2_high_res, lcm_height / solar_level_2_height, axis=0)

    I_level_1_high_res = np.repeat(I_level_1_np_final, lcm_width / solar_level_1_width, axis=1)
    I_level_1_high_res = np.repeat(I_level_1_high_res, lcm_height / solar_level_1_height, axis=0)

    I_level_2_df_final = pd.DataFrame(I_level_2_high_res)
    I_level_1_df_final = pd.DataFrame(I_level_1_high_res)

    if i == 0:
        I_error_sum_high_res = abs(I_level_2_df_final - I_level_1_df_final)
    else:
        I_error_sum_high_res += abs(I_level_2_df_final - I_level_1_df_final)

    #snow
    snow_level_1 = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated//' + 'Global weather (ERA5)-Snow depth-' + current_timestamp + '.csv')  # K
    snow_level_1 = snow_level_1.set_index('PAIRS polygon ID', drop=True)
    snow_level_1.columns = ['count', 'min', 'max', 'mean', '2nd moment']
    snow_level_1 = snow_level_1['mean']
    snow_level_1 = pd.DataFrame(snow_level_1, columns=['mean'])
    snow_level_1_shape_df = pd.DataFrame(index = range(1, 1451), columns = ['Values'])
    snow_level_1_shape_df['Values'] = snow_level_1
    snow_level_1_shape_np = snow_level_1_shape_df.to_numpy()
    snow_level_1_np_final = np.reshape(snow_level_1_shape_np, (solar_level_1_height, solar_level_1_width), order='F')

    snow_level_2 = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated_level_2//' + 'Global weather (ERA5)-Snow depth-' + current_timestamp + 'level_2.csv')  # K
    snow_level_2.columns = ['PAIRS polygon ID level 2', 'averaged value']
    snow_level_2 = snow_level_2.set_index('PAIRS polygon ID level 2', drop=True)
    snow_level_2 = snow_level_2.iloc[:, 0]
    snow_level_2 = pd.DataFrame(snow_level_2)
    snow_level_2_shape_df = pd.DataFrame(index = range(solar_level_2_height * solar_level_2_width), columns = ['Values'])
    snow_level_2_shape_df['Values'] = snow_level_2
    snow_level_2_shape_np = snow_level_2_shape_df.to_numpy()
    snow_level_2_np_final = np.reshape(snow_level_2_shape_np, (solar_level_2_height, solar_level_2_width), order='F')

    snow_level_2_high_res = np.repeat(snow_level_2_np_final, lcm_width / solar_level_2_width, axis=1)
    snow_level_2_high_res = np.repeat(snow_level_2_high_res, lcm_height / solar_level_2_height, axis=0)

    snow_level_1_high_res = np.repeat(snow_level_1_np_final, lcm_width / solar_level_1_width, axis=1)
    snow_level_1_high_res = np.repeat(snow_level_1_high_res, lcm_height / solar_level_1_height, axis=0)

    snow_level_2_df_final = pd.DataFrame(snow_level_2_high_res)
    snow_level_1_df_final = pd.DataFrame(snow_level_1_high_res)

    if i == 0:
        snow_error_sum_high_res = abs(snow_level_2_df_final - snow_level_1_df_final)
    else:
        snow_error_sum_high_res += abs(snow_level_2_df_final - snow_level_1_df_final)

temp_error_sum_high_res /= 8783
temp_error_sum_high_res_np = temp_error_sum_high_res.to_numpy()

wind_error_sum_high_res /= 8783
wind_error_sum_high_res_np = wind_error_sum_high_res.to_numpy()

I_error_sum_high_res /= 8783
I_error_sum_high_res_np = I_error_sum_high_res.to_numpy()

snow_error_sum_high_res /= 8783
snow_error_sum_high_res_np = snow_error_sum_high_res.to_numpy()

#make a heatmap out of
plt.imshow(temp_error_sum_high_res_np, cmap = 'Reds', aspect = 1.35) #aspect = pixels in length / pixels in width??
plt.colorbar()
plt.clim(0, 10)
plt.title('Hourly temperature error at level 2 (K)')
plt.show()

#making histogram
temp_error_sum_high_res_np_values_only = temp_error_sum_high_res_np[~np.isnan(temp_error_sum_high_res_np)]
fig = plt.figure(figsize=(5, 3), tight_layout = True)
num_bins = 100
n, bins, patches = plt.hist(temp_error_sum_high_res_np_values_only, num_bins, density = 1, color = 'black', alpha = 0.7) #alpha is color density
plt.xlabel('Hourly error (C)')
plt.ylabel('Fraction of locations with output')
plt.ylim(ymin=0, ymax = 1.25)
plt.xlim(xmin=0, xmax = 8)
plt.title('Temperature error distribution at level 2')#, fontweight="bold")

(mu, sigma) = norm.fit(temp_error_sum_high_res_np_values_only)
y = norm.pdf(bins, mu, sigma) * sum(n * np.diff(bins))
plt.plot(bins, y, '-', linewidth = 1, label = 'normalized curve')
plt.axvline(x = mu, color = 'm', linestyle = 'dotted', label = 'average')
plt.legend()
plt.show()

#make a heatmap out of
plt.imshow(wind_error_sum_high_res_np, cmap = 'Blues', aspect = 1.35) #aspect = pixels in length / pixels in width??
plt.colorbar()
plt.clim(0, 3.5)
plt.title('Hourly wind error at level 2 (m/s)')
plt.show()

#making histogram
wind_error_sum_high_res_np_values_only = wind_error_sum_high_res_np[~np.isnan(wind_error_sum_high_res_np)]
fig = plt.figure(figsize=(5, 3), tight_layout = True)
num_bins = 100
n, bins, patches = plt.hist(wind_error_sum_high_res_np_values_only, num_bins, density = 1, color = 'black', alpha = 0.7) #alpha is color density
plt.xlabel('Hourly error (m/s)')
plt.ylabel('Fraction of locations with output')
plt.ylim(ymin=0, ymax = 2)
plt.xlim(xmin=0, xmax = 2.5)
plt.title('Wind error distribution at level 2')#, fontweight="bold")

(mu, sigma) = norm.fit(wind_error_sum_high_res_np_values_only)
y = norm.pdf(bins, mu, sigma) * sum(n * np.diff(bins))
plt.plot(bins, y, '-', linewidth = 1, label = 'normalized curve')
plt.axvline(x = mu, color = 'm', linestyle = 'dotted', label = 'average')
plt.legend()
plt.show()


#make a heatmap out of
plt.imshow(I_error_sum_high_res_np, cmap = 'Purples', aspect = 1.35) #aspect = pixels in length / pixels in width??
plt.colorbar()
plt.clim(0, 160000)
plt.title('Hourly irradiance error at level 2 (J/m^2)')
plt.show()

#making histogram
I_error_sum_high_res_np_values_only = I_error_sum_high_res_np[~np.isnan(I_error_sum_high_res_np)]
fig = plt.figure(figsize=(5, 3), tight_layout = True)
num_bins = 100
n, bins, patches = plt.hist(I_error_sum_high_res_np_values_only, num_bins, density = 1, color = 'black', alpha = 0.7) #alpha is color density
plt.xlabel('Hourly error (J/m^2)')
plt.ylabel('Fraction of locations with output')
plt.ylim(ymin=0, ymax = 3* 10**(-5))
plt.xlim(xmin=65, xmax = 120000)
plt.title('Irradiance error distribution at level 2')#, fontweight="bold")

(mu, sigma) = norm.fit(I_error_sum_high_res_np_values_only)
y = norm.pdf(bins, mu, sigma) * sum(n * np.diff(bins))
plt.plot(bins, y, '-', linewidth = 1, label = 'normalized curve')
plt.axvline(x = mu, color = 'm', linestyle = 'dotted', label = 'average')
plt.legend()
plt.show()

#make a heatmap out of
plt.imshow(snow_error_sum_high_res_np, cmap = 'Greens', aspect = 1.35) #aspect = pixels in length / pixels in width??
plt.colorbar()
plt.clim(0, 0.1)
plt.title('Hourly snow error at level 2 (m.w.e.)')
plt.show()

#making histogram
snow_error_sum_high_res_np_values_only = snow_error_sum_high_res_np[~np.isnan(snow_error_sum_high_res_np)]
fig = plt.figure(figsize=(5, 3), tight_layout = True)
num_bins = 100
n, bins, patches = plt.hist(snow_error_sum_high_res_np_values_only, num_bins, density = 1, color = 'black', alpha = 0.7) #alpha is color density
plt.xlabel('Hourly error (m.w.e.)')
plt.ylabel('Fraction of locations with output')
plt.ylim(ymin=0, ymax = 500)
plt.xlim(xmin=0, xmax = 0.04)
plt.title('Snow error distribution at level 2')#, fontweight="bold")

(mu, sigma) = norm.fit(snow_error_sum_high_res_np_values_only)
y = norm.pdf(bins, mu, sigma) * sum(n * np.diff(bins))
plt.plot(bins, y, '-', linewidth = 1, label = 'normalized curve')
plt.axvline(x = mu, color = 'm', linestyle = 'dotted', label = 'average')
plt.legend()
plt.show()