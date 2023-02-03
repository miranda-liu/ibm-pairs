import solar_rf_calculations
import wind_rf_calculations
import wind_cf_generator
import numpy as np
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


print("SOLAR")
print(solar_cfs)
print("WIND")
print(wind_cfs)

def combine_cfs():
    combined_cf = []
    for i in range(width * length):
        temp = []
        for j in range(years * hours):
                loc_hour_total = solar_cfs[i][j] + wind_cfs[i][j]
                temp.append(loc_hour_total)
        combined_cf.append(temp)
    return combined_cf

print("COMBINED")
print(combine_cfs())


### calc combined rf values 

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