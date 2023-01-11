import pandas as pd
from datetime import datetime
import math

#https://www.sciencedirect.com/science/article/pii/S0306261915004237?via%3Dihub
rated_power = 2550000 #W

#loop through and do every timestamp
DATE_TIME_FORMAT = '%m_%d_%Y' + 'T' '%H_%M_%S'
start_datetime = datetime.strptime('01_01_2020T01_00_00', DATE_TIME_FORMAT)
end_datetime = datetime.strptime('12_31_2020T23_00_00', DATE_TIME_FORMAT)
timedelta_index = pd.date_range(start=start_datetime, end=end_datetime, periods=8783) # 24 extra hours hecause 2020 was a leap year
time_in_correct_format = timedelta_index.strftime(DATE_TIME_FORMAT)
#print(time_in_correct_format)

testing = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated\Global weather (ERA5)-wind value-01_01_2020T01_00_00.csv')
correct_index = testing['PAIRS polygon ID']

tracking_wind_output = pd.DataFrame(index = correct_index, columns = range(8783))

cf_2 = 0
cf_3 = 0.0052
cf_4 = 0.0423
cf_5 = 0.1031
cf_6 = 0.1909
cf_7 = 0.3127
cf_8 = 0.4731
cf_9 = 0.6693
cf_10 = 0.8554
cf_11 = 0.9641
cf_12 = 0.9942
cf_13 = 0.9994
cf_14 = 1


#for the length of the time_in_correct_format object, loop through each element
for i in range(8783):
    print(i)
    current_timestamp = time_in_correct_format[i]

    v = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated//' + 'Global weather (ERA5)-wind value-' + current_timestamp + '.csv') #m/s
    v = v.set_index('PAIRS polygon ID', drop=True)
    cf = v.copy()

    cf[cf > 25] = 0
    cf[cf < 3] = 0
    cf[cf > 14] = 1
    cf[cf > 13] = ((v - 12) * cf_13 + (1 - (v - 12)) * cf_12)
    cf[cf > 12] = ((v - 11) * cf_12 + (1 - (v - 11)) * cf_11)
    cf[cf > 11] = ((v - 10) * cf_11 + (1 - (v - 10)) * cf_10)
    cf[cf > 10] = ((v - 9) * cf_10 + (1 - (v - 9)) * cf_9)
    cf[cf > 9] = ((v - 8) * cf_9 + (1 - (v - 8)) * cf_8)
    cf[cf > 8] = ((v - 7) * cf_8 + (1 - (v - 7)) * cf_7)
    cf[cf > 7] = ((v - 6) * cf_7 + (1 - (v - 6)) * cf_6)
    cf[cf > 6] = ((v - 5) * cf_6 + (1 - (v - 5)) * cf_5)
    cf[cf > 5] = ((v - 4) * cf_5 + (1 - (v - 4)) * cf_4)
    cf[cf > 4] = ((v - 3) * cf_4 + (1 - (v - 3)) * cf_3)
    cf[cf > 3] = ((v - 2) * cf_3 + (1 - (v - 2)) * cf_2)

    tracking_wind_output.iloc[:, i] = cf * rated_power

tracking_wind_output.to_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\level_1\tracking_wind_output.csv')
print('wind calculations are finished :)')


