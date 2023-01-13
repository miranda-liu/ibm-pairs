#putting all weather data into level two aggregation and folder


#loop through and do every timestamp
import pandas as pd
from datetime import datetime
import numpy as np

DATE_TIME_FORMAT = '%m_%d_%Y' + 'T' '%H_%M_%S'
start_datetime = datetime.strptime('01_01_2020T01_00_00', DATE_TIME_FORMAT)
end_datetime = datetime.strptime('12_31_2020T23_00_00', DATE_TIME_FORMAT)
timedelta_index = pd.date_range(start=start_datetime, end=end_datetime, periods=8783) # 24 extra hours hecause 2020 was a leap year
time_in_correct_format = timedelta_index.strftime(DATE_TIME_FORMAT)

conversion = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\conversion_level_3.csv')
correct_index = conversion['PAIRS polygon ID']
conversion = conversion.set_index('PAIRS polygon ID', drop=True)
sum = pd.DataFrame(float(0), index = range(50), columns = ['total'])

for index, row in conversion.iterrows():
    new_index = conversion.loc[index, 'level_3 value']
    sum.loc[new_index, 'total'] += conversion.loc[index, 'count']


wind_dataframe = pd.DataFrame(float(0), index = range(50), columns = ['averaged value', 'testing column'])
irradiance_dataframe = pd.DataFrame(float(0), index = range(50), columns = ['averaged value', 'testing column'])
temperature_dataframe = pd.DataFrame(float(0), index = range(50), columns = ['averaged value', 'testing column'])
snow_dataframe = pd.DataFrame(float(0), index = range(50), columns = ['averaged value', 'testing column'])

wind_dataframe['testing column'] = 1
temperature_dataframe['testing column'] = 1
irradiance_dataframe['testing column'] = 1
snow_dataframe['testing column'] = 1

wind_dataframe['testing column'] = wind_dataframe['testing column'] / sum['total']
temperature_dataframe['testing column'] = wind_dataframe['testing column'] / sum['total']
irradiance_dataframe['testing column'] = wind_dataframe['testing column'] / sum['total']
snow_dataframe['testing column'] = wind_dataframe['testing column'] / sum['total']

wind_dataframe = wind_dataframe.replace([np.inf, -np.inf], np.nan).dropna(axis=0)
temperature_dataframe = temperature_dataframe.replace([np.inf, -np.inf], np.nan).dropna(axis=0)
irradiance_dataframe = irradiance_dataframe.replace([np.inf, -np.inf], np.nan).dropna(axis=0)
snow_dataframe = snow_dataframe.replace([np.inf, -np.inf], np.nan).dropna(axis=0)

wind_dataframe = wind_dataframe.drop(columns=['testing column'])
temperature_dataframe = temperature_dataframe.drop(columns=['testing column'])
irradiance_dataframe = irradiance_dataframe.drop(columns=['testing column'])
snow_dataframe = snow_dataframe.drop(columns=['testing column'])

#for the length of the time_in_correct_format object, loop through each element
for i in range(8783):
    print(i)
    current_timestamp = time_in_correct_format[i]

    v = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated//' + 'Global weather (ERA5)-wind value-' + current_timestamp + '.csv') #m/s
    v = v.set_index('PAIRS polygon ID', drop=True)
    I_horiz = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated//' + 'Global weather (ERA5)-Solar radiation-' + current_timestamp + '.csv') #J/m^2
    I_horiz = I_horiz.set_index('PAIRS polygon ID', drop=True)
    temp_K = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated//' + 'Global weather (ERA5)-Temperature-' + current_timestamp + '.csv')  # K
    temp_K = temp_K.set_index('PAIRS polygon ID', drop=True)
    snow_SWE = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated//' + 'Global weather (ERA5)-Snow depth-' + current_timestamp + '.csv')  # m water equivalent
    snow_SWE = snow_SWE.set_index('PAIRS polygon ID', drop = True)

    for index, row in conversion.iterrows():
        new_index = conversion.loc[index, 'level_3 value']
        wind_dataframe.loc[new_index, 'averaged value'] += v.loc[index, 'mean()'] * conversion.loc[index, 'count'] / sum.loc[new_index, 'total']
        irradiance_dataframe.loc[new_index, 'averaged value'] += I_horiz.loc[index, 'mean()'] * conversion.loc[index, 'count'] / sum.loc[new_index, 'total']
        temperature_dataframe.loc[new_index, 'averaged value'] += temp_K.loc[index, 'mean()'] * conversion.loc[index, 'count'] / sum.loc[new_index, 'total']
        snow_dataframe.loc[new_index, 'averaged value'] += snow_SWE.loc[index, 'mean()'] * conversion.loc[index, 'count'] / sum.loc[new_index, 'total']

    wind_dataframe.to_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated_level_3//' + 'Global weather (ERA5)-wind value-' + current_timestamp + 'level_3.csv', index = True)
    irradiance_dataframe.to_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated_level_3//' + 'Global weather (ERA5)-Solar radiation-' + current_timestamp + 'level_3.csv', index=True)
    temperature_dataframe.to_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated_level_3//' + 'Global weather (ERA5)-Temperature-' + current_timestamp + 'level_3.csv', index = True)
    snow_dataframe.to_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated_level_3//' + 'Global weather (ERA5)-Snow depth-' + current_timestamp + 'level_3.csv', index=True)

    """
    level_1_wind_average = v.mean()
    level_1_I_average = I_horiz.mean()
    level_1_temp_average = temp_K.mean()
    level_1_snow_average = snow_SWE.mean()

    level_2_wind_average = wind_dataframe.mean()
    level_2_I_average = irradiance_dataframe.mean()
    level_2_temp_average = temperature_dataframe.mean()
    level_2_snow_average = snow_dataframe.mean()
    """

    wind_dataframe *= 0
    irradiance_dataframe *= 0
    temperature_dataframe *= 0
    snow_dataframe *= 0