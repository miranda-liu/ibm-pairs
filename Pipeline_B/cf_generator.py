import random
import csv
import pandas as pd

years = int(input("Enter the number of years: "))
length = int(input("Enter length of granularity matrix: "))
width = int(input("Enter width of granularity matrix: "))

# all_cfs represents a full year of capacity factors in hourly increments
all_cfs = []

for i in range(years):
    for j in range(8760):
        for k in range(length * width):
            # generate random cf in percentage form
            num = random.random() * 100
            all_cfs.append(num)

# field = ["Capacity Factors"]   

# with open('random_cf.csv', 'w') as f:
#     csv_writer = csv.writer(f)
#     csv_writer.writerow(field)
#     csv_writer.writerow(all_cfs)

dict = {'Capacity Factors': all_cfs}
df = pd.DataFrame(dict) 
df.to_csv('/Users/mirandaliu/Documents/GitHub/ibm-pairs/Pipeline_B/random_capacity_factors.csv') 
