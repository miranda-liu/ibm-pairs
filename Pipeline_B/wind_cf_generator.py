import random
import pandas as pd

# vre_type = input("Solar or wind: ")
years = int(input("(WIND) Enter the number of years: "))
length = int(input("(WIND) Enter length of granularity matrix: "))
width = int(input("(WIND) Enter width of granularity matrix: "))

# all_cfs represents a full year of capacity factors in hourly increments
all_wind_cfs = []
hours_per_year = 10 # remember to switch back to 8760 for final code

for i in range(length * width):
    temp_location = []
    for j in range(years):
        for k in range(hours_per_year):
            # generate random cf in percentage form
            num = random.random() * 100
            temp_location.append(num) # each row in df represents a location, columns represent time periods
    all_wind_cfs.append(temp_location)

# dict = {'Capacity Factors': all_cfs}
df = pd.DataFrame(all_wind_cfs) 
df.to_csv('/Users/mirandaliu/Documents/GitHub/ibm-pairs/Pipeline_B/random_wind_capacity_factors.csv') 


# representing cf data in a 3d list (each inner list represents one location's cf hourly)
def wind_cf_list():
    return all_wind_cfs

# print(cf_list())