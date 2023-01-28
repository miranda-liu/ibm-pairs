import csv
import pandas as pd
import cf_generator

hours = cf_generator.hours_per_year
years = cf_generator.years

all_rfs = []

with open('/Users/mirandaliu/Documents/GitHub/ibm-pairs/Pipeline_B/random_capacity_factors.csv') as file_obj:
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

        all_rfs.append(rf_location_yearly)

# each row represents a new location
# each column represents a new hour
df = pd.DataFrame(all_rfs) 
df.to_csv('/Users/mirandaliu/Documents/GitHub/ibm-pairs/Pipeline_B/reliability_factors.csv') 

# representing rf data in a 2d list (each inner list represents one location's rf hourly)
def rf_list():
    return all_rfs

# representing rf data in a matrix
def rf_3d_matrix():
    rf_matrix_3d = []
    
    hour_matrix = []

    for i in range(hours):
        temp_list = [all_rfs[0][i]]
        hour_matrix.append(temp_list)
    
    for i in range(hours):
        for j in range(1, cf_generator.width*cf_generator.length):

    
    print(hour_matrix)

rf_3d_matrix()

    # hour_matrix = []


    # for i in range(cf_generator.width * cf_generator.length):
    #     loc_all_hourly_rf = []
    #     for j in range(hours):
    #         loc_all_hourly_rf.append(all_rfs[i][j])
    #     hour_matrix.append(loc_all_hourly_rf)
    # rf_matrix_3d.append(hour_matrix)
    
    # return rf_matrix_3d

# print(rf_3d_matrix())