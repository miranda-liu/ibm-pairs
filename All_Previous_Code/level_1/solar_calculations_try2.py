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

testing = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated\Global weather (ERA5)-wind value-01_01_2020T01_00_00.csv')
correct_index = testing['PAIRS polygon ID']

tracking_solar_output = pd.DataFrame(index = correct_index, columns = range(8783))

#finding_latitudes based on IDs
ID_to_latitude = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\shape_info\mit-grid.csv', index_col='id')
#columns_names = ID_to_latitude.columns
latitudes = pd.DataFrame(index = correct_index)
latitudes['value'] = ID_to_latitude.iloc[:, -2]
sin_latitudes = np.sin(np.deg2rad(latitudes))
cos_latitudes = np.cos(np.deg2rad(latitudes))
optimal_tilt = latitudes * 0.76 + 3.1 #degrees
optimal_tilt_rad = np.deg2rad(optimal_tilt)
longitudes = pd.DataFrame(index = correct_index)
longitudes['value'] = ID_to_latitude.iloc[:, -1]

one_to_365 = pd.Series(range(1, 367))
day = one_to_365.repeat(24)
day = day.reset_index(drop=True)

hour = list(range(24))*366

k_d = pd.DataFrame(index = correct_index, columns = ['value'])
k_d = k_d.squeeze()

DNI = pd.DataFrame(index = correct_index, columns = ['value'])
DNI = DNI.squeeze()

POA_dir = pd.DataFrame(index = correct_index, columns = ['value'])
POA_dir = POA_dir.squeeze()

POA_diff_refl = pd.DataFrame(index = correct_index, columns = ['diffuse fraction'])
POA_diff_refl = POA_diff_refl.squeeze()

C_snow_df = pd.DataFrame(index=correct_index, columns=['C snow'])

#for the length of the time_in_correct_format object, loop through each element
for i in range(8783):
    print(i)
    current_timestamp = time_in_correct_format[i]

    #collect all hourly data
    v = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated//' + 'Global weather (ERA5)-wind value-' + current_timestamp + '.csv') #m/s
    v = v.set_index('PAIRS polygon ID', drop=True)
    I_horiz = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated//' + 'Global weather (ERA5)-Solar radiation-' + current_timestamp + '.csv') #J/m^2
    I_horiz = I_horiz.set_index('PAIRS polygon ID', drop=True)
    temp_K = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated//' + 'Global weather (ERA5)-Temperature-' + current_timestamp + '.csv')  # K
    temp_K = temp_K.set_index('PAIRS polygon ID', drop=True)
    snow_SWE = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated//' + 'Global weather (ERA5)-Snow depth-' + current_timestamp + '.csv')  # m water equivalent
    snow_SWE = snow_SWE.set_index('PAIRS polygon ID', drop = True)
    snow_density = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated//' + 'Global weather (ERA5)-Snow density-' + current_timestamp + '.csv')  #kg m-3
    snow_density = snow_SWE.set_index('PAIRS polygon ID', drop = True)


    #unit conversions
    temp_C = temp_K['mean()'] - K_to_C
    I_horiz_Wh = I_horiz['mean()'] * Wh_per_J
    snow_SWE_mm = snow_SWE['mean()'] * 1000

    #irradiance_conversion based on tilt
    declination_angle = 23.45 * math.sin(math.radians(360/365 * (284 + day[i])))    #degrees
    elevation_angle = 90 - latitudes + declination_angle #degrees
    sin_alpha_plus_beta = np.sin(np.deg2rad(elevation_angle) + optimal_tilt_rad)
    sin_alpha = np.sin(np.deg2rad(elevation_angle))
    GHI = I_horiz_Wh * sin_alpha_plus_beta.div(sin_alpha).squeeze()

    #fancier attempt to convert to POA irradiance
    E_sc = 1367 #W/m^2
    b_rad = 2 * math.pi * day[i] / 365
    year_fraction = 2 * math.pi / 366 * (day[i] - 1 + hour[i]) #radians
    eqtime = 229.18 * (0.000075 + 0.001868 * math.cos(year_fraction) - 0.032077 * math.sin(year_fraction) - 0.014615 * math.cos(2 * year_fraction)) - 0.040849 * math.sin(2 * year_fraction)
    time_offset = eqtime + 4 * longitudes
    tst = hour[i] * 60 + time_offset
    hour_angle = tst / 4 - 180 #degrees
    R_av_over_R_sq = 1.00011 + 0.034221 * math.cos(b_rad) + 0.00128 * math.sin(b_rad) + 0.000719 * math.cos(2 * b_rad) + 0.000077 * math.sin(2 * b_rad)
    E_a = E_sc * R_av_over_R_sq
    solar_zenith = np.arccos(np.sin(np.deg2rad(declination_angle)) * sin_latitudes + np.cos(np.deg2rad(declination_angle)) * cos_latitudes * np.cos(np.deg2rad(hour_angle))) #radians
    cos_solar_zenith = np.cos(solar_zenith).squeeze()
    GHI_over_E_a = GHI / E_a
    k_t = GHI_over_E_a / cos_solar_zenith
    angle_of_incidence = np.arccos(np.cos(declination_angle) * np.cos(np.deg2rad(latitudes - optimal_tilt)) * np.cos(np.deg2rad(hour_angle)) + np.sin(declination_angle) * np.sin(np.deg2rad(latitudes - optimal_tilt))) #radians

    for m in range(931):
        index_value = correct_index[m]
        if k_t[index_value] < 0.22:
            k_d[index_value] = 1 - 0.09 * k_t[index_value]
        elif k_t[index_value] >= 0.22 and k_t[index_value] <= 0.8:
            k_d[index_value] = 0.9511 - 0.1604 * k_t[index_value] + 4.388 * k_t[index_value]**2
        elif k_t[index_value] > 0.8:
            k_d[index_value] = 0.165

    elevation_angle = elevation_angle.squeeze()
    DHI = GHI * k_d
    DNI = GHI - DHI / np.sin(np.deg2rad(elevation_angle))

    POA_dir = DNI * np.cos(angle_of_incidence.squeeze())
    POA_diff_refl = GHI * 0.2 * (1 - np.cos(optimal_tilt_rad.squeeze()))
    irradiance = POA_dir + POA_diff_refl

    #converting snow directions
    m = -80 #W/m2/deg C
    #A1 = 0.146
    #a1 = 1.102
    #snow_height = 10**((np.log10(snow_SWE_mm) - np.log10(A1))/a1) # from: https://tc.copernicus.org/articles/13/1767/2019/
    snow_height = snow_SWE / snow_density
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
    U = Uc + Uv * v['mean()'] # W/m^2/K
    T_cell = temp_C + irradiance * alpha * (1 - eta_m) / U # C
    nu = P_dc0 * (1 + gamma * abs(T_cell - 25)) * (1 - f_lid)
    I = irradiance * (1 - f_shade) * (1 - f_soil) # W/m^2
    P_dc = nu * I * A * F_snow # W
    P_dc_inv = P_dc * f_losses
    P_ac = P_dc_inv * nu_inv_ref

    tracking_solar_output.iloc[:, i] = P_ac


tracking_solar_output.to_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\level_1\tracking_solar_output.csv')