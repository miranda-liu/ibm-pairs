#finding conversion of mit-grid to mit-grid-level-2
import pandas as pd

testing = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\Spatially_aggregated\Global weather (ERA5)-Temperature-01_01_2020T01_00_00.csv')
correct_index = testing['PAIRS polygon ID']
testing = testing.set_index('PAIRS polygon ID', drop=True)

ID_to_coordinates = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\shape_info\mit-grid.csv', index_col='id')
latitudes = pd.DataFrame(index = correct_index)
latitudes['Lat'] = ID_to_coordinates.iloc[:, -1]
longitudes = pd.DataFrame(index = correct_index)
longitudes['Long'] = ID_to_coordinates.iloc[:, -2]

level_2_coordinates = pd.read_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\shape_info\mit-grid-level-2.csv', index_col='id')
level_2_coordinates = level_2_coordinates.iloc[:384, :6]

conversion = pd.DataFrame(index = correct_index, columns = ['level_2 value'])

for index, row in conversion.iterrows():
    latitude = latitudes.loc[index, 'Lat']
    longitude = longitudes.loc[index, 'Long']
    for i in range(384):
        if longitude > level_2_coordinates.iloc[i, 3] and longitude <= level_2_coordinates.iloc[i, 1] and latitude > level_2_coordinates.iloc[i, 0] and latitude <= level_2_coordinates.iloc[i, 2]:
            conversion.loc[index, 'level_2 value'] = i
            continue

conversion['count'] = testing.iloc[:, 0]

conversion.to_csv(r'C:\Users\ChemeGrad2019\Desktop\IBM_PAIRS\New_data_format\level_2\conversion.csv')