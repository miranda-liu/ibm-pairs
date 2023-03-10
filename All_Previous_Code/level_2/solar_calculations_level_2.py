import pandas as pd
from datetime import datetime
import math
import numpy as np

#set all constants
K_to_C = 273.15
Wh_per_J = 0.0002777778
Uc = 25 # W/m^2/K
Uv = 1.2 #W/m^2/k/(m/s)
alpha = 0.9
eta_m = 0.1
P_dc0 = 0.26
gamma = -0.0047
f_lid = 0.015
A = 190000 #m^2
f_shade = 0.03
f_soil = 0.02
f_electric = 0.025
f_install = 0.02
f_available = 0.03
f_rating = 0.01
nu_inv_ref = 0.96

f_losses = (1 - f_electric) * (1 - f_install) * (1 - f_available) * (1 - f_rating)

#loop through and do every timestamp
DATE_TIME_FORMAT = '%m_%d_%Y' + 'T' '%H_%M_%S'
start_datetime = datetime.strptime('01_01_2020T01_00_00', DATE_TIME_FORMAT)
end_datetime = datetime.strptime('12_31_2020T23_00_00', DATE_TIME_FORMAT)
timedelta_index = pd.date_range(start=start_datetime, end=end_datetime, periods=8783) # 24 extra hours hecause 2020 was a leap year
time_in_correct_format = timedelta_index.strftime(DATE_TIME_FORMAT)
#print(time_in_correct_format)

testing = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated_level_2\Global weather (ERA5)-wind value-01_01_2020T01_00_00level_2.csv')
testing.columns = ['PAIRS polygon ID level 2', 'averaged value']
correct_index = testing['PAIRS polygon ID level 2']
testing = testing.set_index('PAIRS polygon ID level 2', drop = True)
testing['column for checking'] = 1

tracking_solar_output = pd.DataFrame(index = correct_index, columns = range(8783))

#finding_latitudes based on IDs
ID_to_latitude = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\shape_info\mit-grid-level-2.csv', index_col='id')
ID_to_latitude = ID_to_latitude.iloc[:384, :6]
latitudes = pd.DataFrame(ID_to_latitude.iloc[:, -2])
latitudes['check'] = 1
latitudes['check'] = latitudes['check'] / testing['column for checking']
latitudes = latitudes.dropna()
latitudes = latitudes.drop(columns = ['check'])

optimal_tilt = latitudes * 0.76 + 3.1

one_to_365 = pd.Series(range(1, 367))
day = one_to_365.repeat(24)
day = day.reset_index(drop=True)

C_snow_df = pd.DataFrame(index=correct_index, columns=['C snow'])

#for the length of the time_in_correct_format object, loop through each element
for i in range(8783):
    print(i)
    current_timestamp = time_in_correct_format[i]

    #collect all hourly data
    v = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated_level_2//' + 'Global weather (ERA5)-wind value-' + current_timestamp + 'level_2.csv') #m/s
    v.columns = ['PAIRS polygon ID level 2', 'averaged value']
    v = v.set_index('PAIRS polygon ID level 2', drop=True)
    I_horiz = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated_level_2//' + 'Global weather (ERA5)-Solar radiation-' + current_timestamp + 'level_2.csv') #J/m^2
    I_horiz.columns = ['PAIRS polygon ID level 2', 'averaged value']
    I_horiz = I_horiz.set_index('PAIRS polygon ID level 2', drop=True)
    temp_K = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated_level_2//' + 'Global weather (ERA5)-Temperature-' + current_timestamp + 'level_2.csv')  # K
    temp_K.columns = ['PAIRS polygon ID level 2', 'averaged value']
    temp_K = temp_K.set_index('PAIRS polygon ID level 2', drop=True)
    snow_SWE = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated_level_2//' + 'Global weather (ERA5)-Snow depth-' + current_timestamp + 'level_2.csv')  # m water equivalent
    snow_SWE.columns = ['PAIRS polygon ID level 2', 'averaged value']
    snow_SWE = snow_SWE.set_index('PAIRS polygon ID level 2', drop=True)

    #unit conversions
    temp_C = temp_K['averaged value'] - K_to_C
    I_horiz_Wh = I_horiz['averaged value'] * Wh_per_J
    snow_SWE_mm = snow_SWE['averaged value'] * 1000

    #irradiance_conversion based on tilt
    declination_angle = 23.45 * math.sin(math.radians(360/365 * (284 + day[i])))
    elevation_angle = 90 - latitudes + declination_angle
    alpha_plus_beta = np.deg2rad(elevation_angle) + np.deg2rad(optimal_tilt)
    sin_alpha_plus_beta = np.sin(alpha_plus_beta)
    sin_alpha = np.sin(np.deg2rad(elevation_angle))
    division_results = sin_alpha_plus_beta.div(sin_alpha)
    irradiance = I_horiz_Wh * division_results.squeeze()

    #converting snow directions
    m = -80 #W/m2/deg C
    A1 = 0.146
    a1 = 1.102
    snow_height = 10**((np.log10(snow_SWE_mm) - np.log10(A1))/a1)
    snow_height_cm = snow_height/10

    if i == 0:
        C_snow_df.iloc[:, 0] = 0
    else:
        snow_increase = snow_height_cm - old_snow
        for j in range(262):
            if snow_increase.iloc[j] > 1:
                #print(j)
                #print('snow increase is big')
                C_snow_df.iloc[j, 0] = 1
            elif snow_height_cm.iloc[j] < 1:
                C_snow_df.iloc[j, 0] = 0

    for k in range(262):
        if temp_C.iloc[k] <= irradiance.iloc[k]/m:
            pass
        elif temp_C.iloc[k] > irradiance.iloc[k]/m:
            slide = 0.1 * 1.97 * np.sin(np.deg2rad(latitudes.iloc[k, 0]))
            C_snow_df.iloc[k, 0] = C_snow_df.iloc[k, 0] * slide

    F_snow = 1 - C_snow_df.iloc[:, 0] #all nan
    F_snow = F_snow.reindex(correct_index)
    old_snow = snow_height_cm

    #simple calculations
    U = Uc + Uv * v['averaged value'] # W/m^2/K
    T_cell = temp_C + irradiance * alpha * (1 - eta_m) / U # C
    nu = P_dc0 * (1 + gamma * abs(T_cell - 25)) * (1 - f_lid)
    I = irradiance * (1 - f_shade) * (1 - f_soil) # W/m^2
    P_dc = nu * I * A * F_snow # W
    P_dc_inv = P_dc * f_losses
    P_ac = P_dc_inv * nu_inv_ref

    tracking_solar_output.iloc[:, i] = P_ac


tracking_solar_output.to_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\level_2\tracking_solar_output_level_2.csv')
print('done with level 2 calculations :)')