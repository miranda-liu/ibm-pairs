import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import solar_rf_calculations
import csv
import solar_cf_generator
import statistics

# vre_type = solar_cf_generator.vre_type
years = solar_rf_calculations.years
width = solar_cf_generator.width
length = solar_cf_generator.length
hours = solar_cf_generator.hours_per_year

rf_avg_hourly = []
rf_stdev_hourly = []

with open('/Users/mirandaliu/Documents/GitHub/ibm-pairs/Pipeline_B/solar_reliability_factors.csv') as file_obj:
    # skip header
    heading = next(file_obj)

    # create reader object by passing the file 
    # object to reader method
    rf_data = csv.reader(file_obj)
      
    # iterate over each row in the csv file using reader object
    for row in rf_data:
        row.pop(0) # remove row number

        # convert items in list from str to int
        for i in range(len(row)):
                row[i] = float(row[i])

        # calc mean of RFs of one location
        total = sum(row)
        mean = total/len(row)
        rf_avg_hourly.append(mean)

        # calc standard deviation of RFs of one location
        st_dev = statistics.stdev(row)
        rf_stdev_hourly.append(st_dev)

# graphs average of reliability factors on heat map
def graph_RF_mean_heatmap(mean_list):
    RF_df = pd.DataFrame(columns = ['RF'])
    RF_df['RF'] = mean_list
    RF_df_np = RF_df.to_numpy()
    RF_df_np_final = np.reshape(RF_df_np, (width, length))


    # graphing reliability factor average
    color_map = plt.cm.get_cmap('RdPu')
    plt.imshow(RF_df_np_final, cmap=color_map)
    plt.colorbar()
    #plt.clim(25, 45)#
    #if vre_type == "solar":
    title_name = "Solar Reliability Factors (Mean)"
    # elif vre_type == "wind":
    #     title_name = "Wind Reliability Factors (Mean)"
    plt.title(title_name)
    plt.show()

# graphs standard deviation of reliability factors on heat map
def graph_RF_stdev_heatmap(stdev_list):
    RF_df = pd.DataFrame(columns = ['RF'])
    RF_df['RF'] = stdev_list
    RF_df_np = RF_df.to_numpy()
    RF_df_np_final = np.reshape(RF_df_np, (width, length))


    # graphing reliability factor average
    color_map = plt.cm.get_cmap('RdPu')
    plt.imshow(RF_df_np_final, cmap=color_map)
    plt.colorbar()
    #plt.clim(25, 45)#
    # if vre_type == "solar":
    title_name = "Solar Reliability Factors (Standard Deviation)"
    # elif vre_type == "wind":
    #     title_name = "Wind Reliability Factors (Standard Deviation)"
    plt.title(title_name)
    plt.show()


graph_RF_mean_heatmap(rf_avg_hourly)
graph_RF_stdev_heatmap(rf_stdev_hourly)



# put data into a length * width array
    # data = mean of the points at each point
    # making heat map of the data
