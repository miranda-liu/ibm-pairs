import solar_rf_calculations
import wind_rf_calculations
import wind_cf_generator
import numpy as np
import pandas as pd
import csv


width = wind_cf_generator.width
length = wind_cf_generator.length
hours = wind_cf_generator.hours_per_year
years = wind_cf_generator.years

with open('/Users/mirandaliu/Documents/GitHub/ibm-pairs/Pipeline_B/random_solar_capacity_factors.csv') as solar_cf_data:
        heading = next(solar_cf_data)
        solar_csv_reader = csv.reader(solar_cf_data)
        solar_cfs = list(solar_csv_reader)
        for i in range(width * length):
            solar_cfs[i].pop(0)
        solar_cfs = [[float(x) for x in sublist] for sublist in solar_cfs]


with open('/Users/mirandaliu/Documents/GitHub/ibm-pairs/Pipeline_B/random_wind_capacity_factors.csv') as wind_cf_data:
        heading = next(wind_cf_data)
        wind_csv_reader = csv.reader(wind_cf_data)
        wind_cfs = list(wind_csv_reader)
        for i in range(width * length):
            wind_cfs[i].pop(0)
        wind_cfs = [[float(x) for x in sublist] for sublist in wind_cfs]

# combine solar and wind CFs
def combine_cfs():
    combined_cf = []
    for i in range(width * length):
        temp = []
        for j in range(years * hours):
                loc_hour_total = solar_cfs[i][j] + wind_cfs[i][j]
                temp.append(loc_hour_total)
        combined_cf.append(temp)
    return combined_cf

# return combined CFs as csv file
def csv_combine_cfs():
    csv_list = combine_cfs()
    df = pd.DataFrame(csv_list) 
    df.to_csv('/Users/mirandaliu/Documents/GitHub/ibm-pairs/Pipeline_B/combined_capacity_factors.csv') 

csv_combine_cfs()

# calc combined RFs
def combine_rfs():
    all_combined_rfs = []

    with open('/Users/mirandaliu/Documents/GitHub/ibm-pairs/Pipeline_B/combined_capacity_factors.csv') as file_obj:
            heading = next(file_obj)
            combined_cf_data = csv.reader(file_obj)

            for row in combined_cf_data:
                rf_location_yearly = []
             
                for i in range(1, int(len(row)/years) + 1): # iterate through each location excluding row #
                    temp_total = 0

                    for j in range(i, len(row), hours):
                        temp_total += float(row[j])
                    # calc mean
                    mean = temp_total/years
                   

                    # calc standard deviation
                    temp_variance_sum = 0
                    for j in range(i, len(row), hours):
                        temp_variance_sum += (float(row[j]) - mean) ** 2
                    variance = temp_variance_sum/years
                    st_dev = variance ** 0.5


                    # calc reliability factor
                    rf = mean - 2 * st_dev

                    rf_location_yearly.append(rf)
                all_combined_rfs.append(rf_location_yearly)

    return all_combined_rfs

# representing combined rf data in a matrix
def rf_3d_combined():

    # generates a 3d matrix inner arrays of dimensions width * length, and h number of inner arrays (each 2d array represents a new hour)
    rf_3dmatrix_combined = np.ndarray(shape=(hours,width,length), dtype=float, order='F')
    np.set_printoptions(suppress=True) # supresses scientific notation in np array

    all_combined_rfs = combine_rfs()
    temp_list = []
    for i in range(hours):
        for j in range(width * length):
            temp = all_combined_rfs[j][i]
            temp_list.append(temp)
    for i in range(hours):
        for k in range(width):
            for l in range(length):
                rf_3dmatrix_combined[i][k][l] = temp_list.pop(0)
          
    return rf_3dmatrix_combined

# return combined RFs as csv file
def csv_combine_rfs():
    csv_list = combine_rfs()
    df = pd.DataFrame(csv_list) 
    df.to_csv('/Users/mirandaliu/Documents/GitHub/ibm-pairs/Pipeline_B/combined_reliability_factors.csv') 

csv_combine_rfs()
print(rf_3d_combined())

# wind_cfs = wind_rf_calculations.rf_3d_matrix_wind()
# solar_cfs = solar_rf_calculations.rf_3d_matrix_solar()

# combined_cf = []

# for i in range(hours):
#     temp_list_hours = []
#     for j in range(width):
#         temp_list_width = []
#         for k in range(length):
#             total = wind_cfs[i][j][k] + solar_cfs[i][j][k]
#             temp_list_width.append(total)
#         temp_list_hours.append(temp_list_width)
#     combined_cf.append(temp_list_hours)

# print(combined_cf)

# # change combined cf in list format to 3d matrix
# def combined_3dmatrix():
#     # generates a 3d matrix inner arrays of dimensions width * length, and h number of inner arrays (each 2d array represents a new hour)
#     cf_3dmatrix_combined = np.ndarray(shape=(hours,width,length), dtype=float, order='F')
#     np.set_printoptions(suppress=True) # supresses scientific notation in np array
#     for i in range(hours):
#         for j in range(width):
#             for k in range(length):
#                 cf_3dmatrix_combined[i][j][k] = combined_cf[i][j][k]
#     return cf_3dmatrix_combined

# print(combined_3dmatrix())

# # condense hourly matrices to one overall
# def condensed_matrix():
   
#     rf_3dmatrix_combined = np.ndarray(shape=(1,width,length), dtype=float, order='F')
    
#     # calc mean
#     cf_mean_list = []
#     cf_stdev_list = []
#     condensed_combined_rfs = []

#     for i in range(width):
#         for j in range(length):
#             total = 0.
#             for k in range(hours):
#                 temp = combined_3dmatrix()[k][i][j]
#                 total += temp

#             mean = total/hours
#             cf_mean_list.append(mean)
#     cf_mean_list = np.reshape(cf_mean_list, (width, length))

#     # calc st dev
#     for i in range(width):
#         for j in range(length):
#             variance_sum = 0.
#             mean = cf_mean_list[i][j]
#             for k in range(hours):
#                 variance_sum += (combined_3dmatrix()[k][i][j] - mean) ** 2
            
#             variance = variance_sum/hours
#             st_dev = variance ** 0.5
#             cf_stdev_list.append(st_dev)
#     cf_stdev_list = np.reshape(cf_stdev_list, (width, length))

#     # calc combined rf
#     for i in range(width):
#         for j in range(length):
#             combined_rf = cf_mean_list[i][j] - 2 * cf_stdev_list[i][j]
#             condensed_combined_rfs.append(combined_rf)
#     condensed_combined_rfs = np.reshape(condensed_combined_rfs, (width, length))

#     return condensed_combined_rfs

# print(condensed_matrix())