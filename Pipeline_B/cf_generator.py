import random
import pandas as pd

years = int(input("Enter the number of years: "))
length = int(input("Enter length of granularity matrix: "))
width = int(input("Enter width of granularity matrix: "))

# all_cfs represents a full year of capacity factors in hourly increments
all_cfs = []
hours_per_year = 10

for i in range(length * width):
    temp_location = []
    for j in range(years):
        for k in range(hours_per_year):
            # generate random cf in percentage form
            num = random.random() * 100
            temp_location.append(num) # each row in df represents a location, columns represent time periods
    all_cfs.append(temp_location)

# dict = {'Capacity Factors': all_cfs}
df = pd.DataFrame(all_cfs) 
df.to_csv('/Users/mirandaliu/Documents/GitHub/ibm-pairs/Pipeline_B/random_capacity_factors.csv') 