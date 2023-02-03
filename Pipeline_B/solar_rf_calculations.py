import csv
import pandas as pd
import solar_cf_generator
import numpy as np

# vre_type = cf_generator.vre_type
hours = solar_cf_generator.hours_per_year
years = solar_cf_generator.years

all_solar_rfs = []

with open('/Users/mirandaliu/Documents/GitHub/ibm-pairs/Pipeline_B/random_solar_capacity_factors.csv') as file_obj:
    # skip header
    heading = next(file_obj)

    # create reader object by passing the file 
    # object to reader method
    cf_data = csv.reader(file_obj)
      
    # iterate over each row in the csv file using reader object
    for row in cf_data:
        # stores RFs for each location
        rf_location_yearly = []
        for i in range(1, int(len(row)/years) + 1): # iterate through each location excluding row #
            location_mean_hourly = 0
            location_stdev_hourly = 0
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

            #rf_location_hourly.append(rf)
            rf_location_yearly.append(rf)

        all_solar_rfs.append(rf_location_yearly)

# each row represents a new location
# each column represents a new hour
df = pd.DataFrame(all_solar_rfs) 
df.to_csv('/Users/mirandaliu/Documents/GitHub/ibm-pairs/Pipeline_B/solar_reliability_factors.csv') 

# representing rf data in a 2d list (each inner list represents one location's rf hourly)
def rf_list():
    return all_solar_rfs

# representing rf data in a matrix
def rf_3d_matrix_solar():
    width = solar_cf_generator.width
    length = solar_cf_generator.length

    # generates a 3d matrix inner arrays of dimensions width * length, and h number of inner arrays (each 2d array represents a new hour)
    rf_3dmatrix_solar = np.ndarray(shape=(hours,width,length), dtype=float, order='F')
    np.set_printoptions(suppress=True) # supresses scientific notation in np array

    temp_list = []
    for i in range(hours):
        for j in range(width * length):
            temp = all_solar_rfs[j][i]
            temp_list.append(temp)
    for i in range(hours):
        for k in range(width):
            for l in range(length):
                rf_3dmatrix_solar[i][k][l] = temp_list.pop(0)
          
    return rf_3dmatrix_solar


rf_3d_matrix_solar()

# print(rf_3d_matrix())

# print(rf_list())