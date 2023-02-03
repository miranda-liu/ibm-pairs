# SOLAR AND WIND RFs COMBINED
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import combining_wind_solar_cf


width = combining_wind_solar_cf.width
length = combining_wind_solar_cf.length

# graphs average of combined reliability factors on heat map
def graph_combined_rf():
    RF_combined_df = pd.DataFrame(columns = ['RF'])
    RF_combined_df['RF'] = c
    RF_combined_df_np = RF_combined_df.to_numpy()
    RF_combined_df_np_final = np.reshape(RF_combined_df_np, (width, length))

    # graphing reliability factor average
    color_map = plt.cm.get_cmap('RdPu')
    plt.imshow(RF_combined_df_np_final, cmap=color_map)
    plt.colorbar()
    plt.title("Combined Reliability Factors (Mean)")
    plt.show()

graph_combined_rf()


 