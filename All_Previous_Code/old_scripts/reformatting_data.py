import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import time

start_time = time.time()
number_of_files = 49239
hours_in_this_year = 8883

#each column contains all the locations for one hour and all the rows contain all the hours for one location
time_before_first_dataframe = time.time()
latitudes = pd.DataFrame(index=range(number_of_files),columns=range(hours_in_this_year))
time_after_first_dataframe = time.time()
longitudes = pd.DataFrame(index=range(number_of_files),columns=range(hours_in_this_year))
values = pd.DataFrame(index=range(number_of_files),columns=range(hours_in_this_year))

file_number = 0
for filename in os.listdir(r'C:\Users\ChemeGrad2019\Downloads\49420.tar'):
    before_read_file = time.time()
    data = pd.read_csv(r'C:\Users\ChemeGrad2019\Downloads\49420.tar' + "\\" + filename)
    after_read_file = time.time()
    for hour_number in range(0, hours_in_this_year):
        latitudes.iloc[file_number, hour_number] = data.iloc[hour_number, 3]
        longitudes.iloc[file_number, hour_number] = data.iloc[hour_number, 2]
        values.iloc[file_number, hour_number] = data.iloc[hour_number, 4]
    file_number = file_number + 1
    after_calculations = time.time()
    if file_number%1000 == 0:
        print(file_number)
        print('time to read file = ')
        print(after_read_file - before_read_file)
        print('time to do calculations = ')
        print(after_calculations - after_read_file)


#saving the dataframes:
latitudes.to_csv('Latitudes')
longitudes.to_csv('Longitudes')
values.to_csv('Values')

#plotting a specific hour
chosen_hour = 0

plt.rcParams['figure.figsize'] = (8, 6)
ax = plt.axes(projection = '3d')
latitudes_one_hours  = latitudes.iloc[:, chosen_hour]
longitudes_one_hours  = longitudes.iloc[:, chosen_hour]
values_one_hours  = values.iloc[:, chosen_hour]
ax.scatter3D(latitudes_one_hour, longitudes_one_hour, values_one_hour)#, s = 10)
ax.set_xlabel('Latitude')
ax.set_ylabel('Longitude')
ax.set_zlabel('Irradiance Value (Units)')

ax.view_init(45, 45)
plt.show()
end_time = time.time()

print('Time to do one hour:')
print(end_time - start_time)