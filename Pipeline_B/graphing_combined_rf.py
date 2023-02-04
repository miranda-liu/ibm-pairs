# SOLAR AND WIND RFs COMBINED

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv
import statistics
import combining_wind_solar_cf

years = combining_wind_solar_cf.years
width = combining_wind_solar_cf.width
length = combining_wind_solar_cf.length
hours = combining_wind_solar_cf.hours

rf_avg_combined = []
rf_stdev_combined = []

with open('/Users/mirandaliu/Documents/GitHub/ibm-pairs/Pipeline_B/combined_reliability_factors.csv') as file_obj:
    # skip header
    heading = next(file_obj)

    # create reader object by passing the file 
    # object to reader method
    combined_rf_data = csv.reader(file_obj)
      
    # iterate over each row in the csv file using reader object
    for row in combined_rf_data:
        row.pop(0) # remove row number

        # convert items in list from str to int
        for i in range(len(row)):
                row[i] = float(row[i])

        # calc mean of combined RFs of one location
        total = sum(row)
        mean = total/len(row)
        rf_avg_combined.append(mean)

        # calc standard deviation of combined RFs of one location
        st_dev = statistics.stdev(row)
        rf_stdev_combined.append(st_dev)

# graphs average of combined reliability factors on heat map
def graph_comb_RF_mean_heatmap(mean_list):
    RF_df = pd.DataFrame(columns = ['Comb RF'])
    RF_df['Comb RF'] = mean_list
    RF_df_np = RF_df.to_numpy()
    RF_df_np_final = np.reshape(RF_df_np, (width, length))


    # graphing reliability factor average
    color_map = plt.cm.get_cmap('RdPu')
    plt.imshow(RF_df_np_final, cmap=color_map)
    plt.colorbar()
    plt.title("Combined Reliability Factors (Mean)")
    plt.show()

# graphs standard deviation of combined reliability factors on heat map
def graph_comb_RF_stdev_heatmap(stdev_list):
    RF_df = pd.DataFrame(columns = ['Comb RF'])
    RF_df['Comb RF'] = stdev_list
    RF_df_np = RF_df.to_numpy()
    RF_df_np_final = np.reshape(RF_df_np, (width, length))


    # graphing reliability factor average
    color_map = plt.cm.get_cmap('RdPu')
    plt.imshow(RF_df_np_final, cmap=color_map)
    plt.colorbar()
    plt.title("Combined Reliability Factors (Standard Deviation)")
    plt.show()


graph_comb_RF_mean_heatmap(rf_avg_combined)
graph_comb_RF_stdev_heatmap(rf_stdev_combined)