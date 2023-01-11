import pandas as pd
from datetime import datetime
import math

density = 1.23 #kg/m^2
r = 60 #m https://www.energy.gov/eere/articles/wind-turbines-bigger-better
A = math.pi * r**2
C_p = 0.4 #power coefficient

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

#for the length of the time_in_correct_format object, loop through each element
for i in range(8783):
    print(i)
    current_timestamp = time_in_correct_format[i]

    v = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated//' + 'Global weather (ERA5)-wind value-' + current_timestamp + '.csv') #m/s
    v = v.set_index('PAIRS polygon ID', drop=True)

    #v = v * (40/10)**0.2 #this is to extrapolate wind speed for 10 to 40 meteres high using: https://websites.pmc.ucsc.edu/~jnoble/wind/extrap/

    v[v > 25] = 0
    v[v < 3] = 0
    v[v > 13] = 14

    power = density*A*v**3*C_p/2 #https://www.raeng.org.uk/publications/other/23-wind-turbine

    tracking_wind_output.iloc[:, i] = power

tracking_wind_output.to_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\level_1\tracking_wind_output.csv')
print('wind calculations are finished :)')


