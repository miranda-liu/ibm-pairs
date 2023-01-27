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
    reader_obj = csv.reader(file_obj)
      
    # iterate over each row in the csv file using reader object
    for row in reader_obj:
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
            print(mean)

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


           
# hourly reliability factor to start --> find mean of location at 0, 9, 19, 29 etc (each location every "year")
# -> org data in matrix/csv file