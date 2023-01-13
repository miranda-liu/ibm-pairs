import pandas as pd
from datetime import datetime
import math
import numpy as np
import matplotlib.pyplot as plt

#loop through and do every timestamp
DATE_TIME_FORMAT = '%m_%d_%Y' + 'T' '%H_%M_%S'
start_datetime = datetime.strptime('01_01_2020T01_00_00', DATE_TIME_FORMAT)
end_datetime = datetime.strptime('12_31_2020T23_00_00', DATE_TIME_FORMAT)
timedelta_index = pd.date_range(start=start_datetime, end=end_datetime, periods=8783) # 24 extra hours hecause 2020 was a leap year
time_in_correct_format = timedelta_index.strftime(DATE_TIME_FORMAT)
#print(time_in_correct_format)

testing_level_2 = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated_level_2\Global weather (ERA5)-wind value-01_01_2020T01_00_00level_2.csv')
testing_level_2.columns = ['PAIRS polygon ID level 2', 'averaged value']
correct_index_level_2 = testing_level_2['PAIRS polygon ID level 2']

testing = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated\Global weather (ERA5)-wind value-01_01_2020T01_00_00.csv')
correct_index = testing['PAIRS polygon ID']

wind_level_2_sum = pd.DataFrame(float(0), index = correct_index_level_2, columns = ['level 2 sum'])
I_level_2_sum = pd.DataFrame(float(0), index = correct_index_level_2, columns = ['level 2 sum'])
temp_level_2_sum = pd.DataFrame(float(0), index = correct_index_level_2, columns = ['level 2 sum'])
snow_level_2_sum = pd.DataFrame(float(0), index = correct_index_level_2, columns = ['level 2 sum'])

wind_sum = pd.DataFrame(float(0), index = correct_index, columns = ['sum'])
I_sum = pd.DataFrame(float(0), index = correct_index, columns = ['sum'])
temp_sum = pd.DataFrame(float(0), index = correct_index, columns = ['sum'])
snow_sum = pd.DataFrame(float(0), index = correct_index, columns = ['sum'])

for i in range(8782):
    print(i)
    current_timestamp = time_in_correct_format[i]

    v_level_2 = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated_level_2//' + 'Global weather (ERA5)-wind value-' + current_timestamp + 'level_2.csv') #m/s
    v_level_2.columns = ['PAIRS polygon ID level 2', 'averaged value']
    v_level_2 = v_level_2.set_index('PAIRS polygon ID level 2', drop=True)
    I_horiz_level_2 = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated_level_2//' + 'Global weather (ERA5)-Solar radiation-' + current_timestamp + 'level_2.csv') #J/m^2
    I_horiz_level_2.columns = ['PAIRS polygon ID level 2', 'averaged value']
    I_horiz_level_2 = I_horiz_level_2.set_index('PAIRS polygon ID level 2', drop=True)
    temp_K_level_2 = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated_level_2//' + 'Global weather (ERA5)-Temperature-' + current_timestamp + 'level_2.csv')  # K
    temp_K_level_2.columns = ['PAIRS polygon ID level 2', 'averaged value']
    temp_K_level_2 = temp_K_level_2.set_index('PAIRS polygon ID level 2', drop=True)
    snow_SWE_level_2 = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated_level_2//' + 'Global weather (ERA5)-Snow depth-' + current_timestamp + 'level_2.csv')  # m water equivalent
    snow_SWE_level_2.columns = ['PAIRS polygon ID level 2', 'averaged value']
    snow_SWE_level_2 = snow_SWE_level_2.set_index('PAIRS polygon ID level 2', drop=True)

    v = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated//' + 'Global weather (ERA5)-wind value-' + current_timestamp + '.csv') #m/s
    v = v.set_index('PAIRS polygon ID', drop=True)
    v = v['mean()']
    v = v.to_frame()
    v.columns = ['value']
    I_horiz = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated//' + 'Global weather (ERA5)-Solar radiation-' + current_timestamp + '.csv') #J/m^2
    I_horiz = I_horiz.set_index('PAIRS polygon ID', drop=True)
    I_horiz = I_horiz['mean()']
    I_horiz = I_horiz.to_frame()
    I_horiz.columns = ['value']
    temp_K = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated//' + 'Global weather (ERA5)-Temperature-' + current_timestamp + '.csv')  # K
    temp_K = temp_K.set_index('PAIRS polygon ID', drop=True)
    temp_K = temp_K['mean()']
    temp_K = temp_K.to_frame()
    temp_K.columns = ['value']
    snow_SWE = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated//' + 'Global weather (ERA5)-Snow depth-' + current_timestamp + '.csv')  # m water equivalent
    snow_SWE = snow_SWE.set_index('PAIRS polygon ID', drop = True)
    snow_SWE = snow_SWE['mean()']
    snow_SWE = snow_SWE.to_frame()
    snow_SWE.columns = ['value']

    wind_level_2_sum['level 2 sum'] += v_level_2['averaged value']
    I_level_2_sum['level 2 sum'] += I_horiz_level_2['averaged value']
    temp_level_2_sum['level 2 sum'] += temp_K_level_2['averaged value']
    snow_level_2_sum['level 2 sum'] += snow_SWE_level_2['averaged value']

    wind_sum['sum'] += v['value']
    I_sum['sum'] += I_horiz['value']
    temp_sum['sum'] += temp_K['value']
    snow_sum['sum'] += snow_SWE['value']


#max and mins
wind_max = 60000
wind_min = 9000
I_max = 8000000000
I_min = 4500000000
temp_max = 2400000
temp_min = 2650000
snow_max = 1200
snow_min = 0
#make a wind level 2 heatmap
wind_level_2_sum_shape = pd.DataFrame(index = range(384), columns = ['wind level 2 sum'])
wind_level_2_sum_shape['wind level 2 sum'] = wind_level_2_sum
wind_level_2_sum_shape_np = wind_level_2_sum_shape.to_numpy()
wind_level_2_sum_shape_np_final = np.reshape(wind_level_2_sum_shape_np, (12, 32), order = 'F')

plt.imshow(wind_level_2_sum_shape_np_final, cmap='gist_rainbow') #plasma is good for solar
plt.colorbar()
plt.title('Wind sum level 2')
plt.clim(wind_min, wind_max)
plt.show()

#make a wind heatmap
wind_sum_shape = pd.DataFrame(index = range(1, 1451), columns = ['wind sum'])
wind_sum_shape['wind sum'] = wind_sum
wind_sum_shape_np = wind_sum_shape.to_numpy()
wind_sum_shape_np_final = np.reshape(wind_sum_shape_np, (25, 58), order = 'F')

plt.imshow(wind_sum_shape_np_final, cmap='gist_rainbow') #plasma is good for solar
plt.colorbar()
plt.title('Wind sum')
plt.clim(wind_min, wind_max)
plt.show()

#make a irradiance level 2 heatmap
I_level_2_sum_shape = pd.DataFrame(index = range(384), columns = ['I level 2 sum'])
I_level_2_sum_shape['I level 2 sum'] = I_level_2_sum
I_level_2_sum_shape_np = I_level_2_sum_shape.to_numpy()
I_level_2_sum_shape_np_final = np.reshape(I_level_2_sum_shape_np, (12, 32), order = 'F')

plt.imshow(I_level_2_sum_shape_np_final, cmap='gist_rainbow') #plasma is good for solar
plt.colorbar()
plt.title('Irradiance sum level 2')
plt.clim(I_min, I_max)
plt.show()

#make a irradiance heatmap
I_sum_shape = pd.DataFrame(index = range(1, 1451), columns = ['I sum'])
I_sum_shape['I sum'] = I_sum
I_sum_shape_np = I_sum_shape.to_numpy()
I_sum_shape_np_final = np.reshape(I_sum_shape_np, (25, 58), order = 'F')

plt.imshow(I_sum_shape_np_final, cmap='gist_rainbow') #plasma is good for solar
plt.colorbar()
plt.title('Irradiance sum')
plt.clim(I_min, I_max)
plt.show()

#make a temp level 2 heatmap
temp_level_2_sum_shape = pd.DataFrame(index = range(384), columns = ['temp level 2 sum'])
temp_level_2_sum_shape['temp level 2 sum'] = temp_level_2_sum
temp_level_2_sum_shape_np = temp_level_2_sum_shape.to_numpy()
temp_level_2_sum_shape_np_final = np.reshape(temp_level_2_sum_shape_np, (12, 32), order = 'F')

plt.imshow(temp_level_2_sum_shape_np_final, cmap='gist_rainbow') #plasma is good for solar
plt.colorbar()
plt.title('Temperature sum level 2')
plt.clim(temp_min, temp_max)
plt.show()

#make a temp heatmap
temp_sum_shape = pd.DataFrame(index = range(1, 1451), columns = ['temp sum'])
temp_sum_shape['temp sum'] = temp_sum
temp_sum_shape_np = temp_sum_shape.to_numpy()
temp_sum_shape_np_final = np.reshape(temp_sum_shape_np, (25, 58), order = 'F')

plt.imshow(temp_sum_shape_np_final, cmap='gist_rainbow') #plasma is good for solar
plt.colorbar()
plt.title('Temperature sum')
plt.clim(temp_min, temp_max)
plt.show()

#make a snow level 2 heatmap
snow_level_2_sum_shape = pd.DataFrame(index = range(384), columns = ['snow level 2 sum'])
snow_level_2_sum_shape['snow level 2 sum'] = snow_level_2_sum
snow_level_2_sum_shape_np = snow_level_2_sum_shape.to_numpy()
snow_level_2_sum_shape_np_final = np.reshape(snow_level_2_sum_shape_np, (12, 32), order = 'F')

plt.imshow(snow_level_2_sum_shape_np_final, cmap='gist_rainbow') #plasma is good for solar
plt.colorbar()
plt.title('Snow sum level 2')
plt.clim(snow_min, snow_max)
plt.show()

#make a snow heatmap
snow_sum_shape = pd.DataFrame(index = range(1, 1451), columns = ['snow sum'])
snow_sum_shape['snow sum'] = snow_sum
snow_sum_shape_np = snow_sum_shape.to_numpy()
snow_sum_shape_np_final = np.reshape(snow_sum_shape_np, (25, 58), order = 'F')

plt.imshow(snow_sum_shape_np_final, cmap='gist_rainbow') #plasma is good for solar
plt.colorbar()
plt.title('Snow sum')
plt.clim(snow_min, snow_max)
plt.show()
