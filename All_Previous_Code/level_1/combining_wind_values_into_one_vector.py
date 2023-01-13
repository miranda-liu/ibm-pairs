import pandas as pd
from datetime import datetime

#loop through and do every timestamp
DATE_TIME_FORMAT = '%m_%d_%Y' + 'T' '%H_%M_%S'
start_datetime = datetime.strptime('01_01_2020T01_00_00', DATE_TIME_FORMAT)
end_datetime = datetime.strptime('12_31_2020T23_00_00', DATE_TIME_FORMAT)
timedelta_index = pd.date_range(start=start_datetime, end=end_datetime, periods=8783) # 24 extra hours hecause 2020 was a leap year
time_in_correct_format = timedelta_index.strftime(DATE_TIME_FORMAT)
#print(time_in_correct_format)

#for the length of the time_in_correct_format object, loop through each element
for i in range(8783):
    current_timestamp = time_in_correct_format[i]

    # read east csv and read north csv
    east = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated//' + 'Global weather (ERA5)-100 meter wind towards east-' + current_timestamp + '.csv')
    north = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated//' + 'Global weather (ERA5)-100 meter wind towards north-' + current_timestamp + '.csv')

    #drop all columns expect mean
    east = east.drop(columns=['count()[unit: km^2]', 'min()', 'max()', '2nd moment'])
    north = north.drop(columns=['count()[unit: km^2]', 'min()', 'max()', '2nd moment'])

    #set PAIRS polygon ID as index value
    east = east.set_index('PAIRS polygon ID', drop = True)
    north = north.set_index('PAIRS polygon ID', drop = True)

    #wind_value = (north_value^2 + east_value^2) ^ (1/2)
    wind_value = (east**2 + north**2)**(1/2)

    #print a csv with wind data for each timestamp
    wind_value.to_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated//' + 'Global weather (ERA5)-wind value-' + current_timestamp + '.csv', index = True)
    print(i)
