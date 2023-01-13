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

#sizing info
lcm_height = 300
lcm_width = 928

solar_level_1_height = 25
solar_level_1_width = 58
solar_level_2_height = 12
solar_level_2_width = 32

#loop through and do every timestamp
DATE_TIME_FORMAT = '%m_%d_%Y' + 'T' '%H_%M_%S'
start_datetime = datetime.strptime('01_01_2020T01_00_00', DATE_TIME_FORMAT)
end_datetime = datetime.strptime('12_31_2020T23_00_00', DATE_TIME_FORMAT)
timedelta_index = pd.date_range(start=start_datetime, end=end_datetime, periods=8783) # 24 extra hours hecause 2020 was a leap year
time_in_correct_format = timedelta_index.strftime(DATE_TIME_FORMAT)
#print(time_in_correct_format)

testing_level_1 = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated\Global weather (ERA5)-wind value-01_01_2020T01_00_00.csv')
correct_index_level_1 = testing_level_1['PAIRS polygon ID']

correct_shape_df_level_1 = pd.DataFrame(index = range(1, 1451), columns = ['values'])
correct_shape_df_level_2 = pd.DataFrame(index = range(384), columns = ['values'])

finding_latitudes based on IDs
ID_to_latitude_level_1 = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\shape_info\mit-grid.csv', index_col='id')
latitudes_level_1 = pd.DataFrame(index = correct_index_level_1)
latitudes_level_1['Lat'] = ID_to_latitude_level_1.iloc[:, -2]
optimal_tilt_level_1 = latitudes_level_1 * 0.76 + 3.1

correct_shape_df_level_1['values'] = optimal_tilt_level_1['mean()']
correct_shape_np = correct_shape_df_level_1.to_numpy()
correct_shape_np_final = np.reshape(correct_shape_np, (solar_level_1_height, solar_level_1_width), order='F')
snow_SWE_level_1_high_res = np.repeat(correct_shape_np_final, lcm_width / solar_level_1_width, axis=1)
snow_SWE_level_1_high_res = np.repeat(snow_SWE_level_1_high_res, lcm_height / solar_level_1_height, axis=0)
snow_SWE = np.reshape(snow_SWE_level_1_high_res, (lcm_height * lcm_width), order='F')
#FIX THIS

one_to_365 = pd.Series(range(1, 367))
day = one_to_365.repeat(24)
day = day.reset_index(drop=True)

C_snow_df_level_1 = pd.DataFrame(index = range(lcm_height * lcm_width), columns = ['C snow'])

#tracking_solar_output = pd.DataFrame(index = range(lcm_height * lcm_width), columns = range(8783))

#for the length of the time_in_correct_format object, loop through each element
for i in range(8783):
    print(i)
    current_timestamp = time_in_correct_format[i]

    #collect all hourly data
    v_level_1 = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated//' + 'Global weather (ERA5)-wind value-' + current_timestamp + '.csv') #m/s
    v_level_1 = v_level_1.set_index('PAIRS polygon ID', drop = True)
    I_horiz_level_2 = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated//' + 'Global weather (ERA5)-Solar radiation-' + current_timestamp + '.csv') #J/m^2
    I_horiz_level_2 = I_horiz_level_2.set_index('PAIRS polygon ID', drop = True)
    temp_K_level_1 = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated//' + 'Global weather (ERA5)-Temperature-' + current_timestamp + '.csv')  # K
    temp_K_level_1 = temp_K_level_1.set_index('PAIRS polygon ID', drop = True)
    snow_SWE_level_1 = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated//' + 'Global weather (ERA5)-Snow depth-' + current_timestamp + '.csv')  # m water equivalent
    snow_SWE_level_1 = snow_SWE_level_1.set_index('PAIRS polygon ID', drop = True)

    correct_shape_df_level_1['values'] = v_level_1['mean()']
    correct_shape_np = correct_shape_df_level_1.to_numpy()
    correct_shape_np_final = np.reshape(correct_shape_np, (solar_level_1_height, solar_level_1_width), order='F')
    v_level_1_high_res = np.repeat(correct_shape_np_final, lcm_width / solar_level_1_width, axis=1)
    v_level_1_high_res = np.repeat(v_level_1_high_res, lcm_height / solar_level_1_height, axis=0)
    v = np.reshape(v_level_1_high_res, (lcm_height * lcm_width), order = 'F')

    correct_shape_df_level_1['values'] = temp_K_level_1['mean()']
    correct_shape_np = correct_shape_df_level_1.to_numpy()
    correct_shape_np_final = np.reshape(correct_shape_np, (solar_level_1_height, solar_level_1_width), order='F')
    temp_K_level_1_high_res = np.repeat(correct_shape_np_final, lcm_width / solar_level_1_width, axis=1)
    temp_K_level_1_high_res = np.repeat(temp_K_level_1_high_res, lcm_height / solar_level_1_height, axis=0)
    temp_K = np.reshape(temp_K_level_1_high_res, (lcm_height * lcm_width), order = 'F')

    correct_shape_df_level_1['values'] = snow_SWE_level_1['mean()']
    correct_shape_np = correct_shape_df_level_1.to_numpy()
    correct_shape_np_final = np.reshape(correct_shape_np, (solar_level_1_height, solar_level_1_width), order='F')
    snow_SWE_level_1_high_res = np.repeat(correct_shape_np_final, lcm_width / solar_level_1_width, axis=1)
    snow_SWE_level_1_high_res = np.repeat(snow_SWE_level_1_high_res, lcm_height / solar_level_1_height, axis=0)
    snow_SWE = np.reshape(snow_SWE_level_1_high_res, (lcm_height * lcm_width), order = 'F')

    correct_shape_df_level_2['values'] = I_horiz_level_2['mean()']
    correct_shape_np = correct_shape_df_level_2.to_numpy()
    correct_shape_np_final = np.reshape(correct_shape_np, (solar_level_2_height, solar_level_2_width), order='F')
    I_horiz_level_2_high_res = np.repeat(correct_shape_np_final, lcm_width / solar_level_2_width, axis=1)
    I_horiz_level_2_high_res = np.repeat(I_horiz_level_2_high_res, lcm_height / solar_level_2_height, axis=0)
    I_horiz = np.reshape(I_horiz_level_2_high_res, (lcm_height * lcm_width), order = 'F')

    #unit conversions
    temp_C = temp_K - K_to_C
    I_horiz_Wh = I_horiz * Wh_per_J
    snow_SWE_mm = snow_SWE * 1000

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
        for j in range(931):
            if snow_increase.iloc[j] > 1:
                print(j)
                print('snow increase is big')
                C_snow_df.iloc[j, 0] = 1
            elif snow_height_cm.iloc[j] < 1:
                C_snow_df.iloc[j, 0] = 0

    for k in range(931):
        if temp_C.iloc[k] <= irradiance.iloc[k]/m:
            pass
        elif temp_C.iloc[k] > irradiance.iloc[k]/m:
            slide = 0.1 * 1.97 * np.sin(np.deg2rad(latitudes.iloc[k, 0]))
            C_snow_df.iloc[k, 0] = C_snow_df.iloc[k, 0] * slide

    F_snow = 1 - C_snow_df.iloc[:, 0] #all nan
    F_snow = F_snow.reindex(correct_index)
    old_snow = snow_height_cm

    #simple calculations
    U = Uc + Uv * v # W/m^2/K
    T_cell = temp_C + irradiance * alpha * (1 - eta_m) / U # C
    nu = P_dc0 * (1 + gamma * abs(T_cell - 25)) * (1 - f_lid)
    I = irradiance * (1 - f_shade) * (1 - f_soil) # W/m^2
    P_dc = nu * I * A * F_snow # W
    P_dc_inv = P_dc * f_losses
    P_ac = P_dc_inv * nu_inv_ref

    tracking_solar_output.iloc[:, i] = P_ac


tracking_solar_output.to_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\tracking_solar_output.csv')