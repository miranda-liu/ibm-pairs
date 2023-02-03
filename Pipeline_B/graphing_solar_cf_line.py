import solar_rf_calculations
import matplotlib.pyplot as plt
import csv

num_places = int(input("Enter number of places to graph: "))

loc_index_list = []
for i in range(num_places):
    loc_index_list.append(int(input("Enter location index: ")))

### add in later function to print out location name corresponding with the index

def graph_solar_CF():

    # hour stamps
    x_axis = []
    total_hours = solar_rf_calculations.years * solar_rf_calculations.hours
    for i in range(total_hours):
        x_axis.append(i + 1)

    # solar CF values
    y_axis = []
    with open('/Users/mirandaliu/Documents/GitHub/ibm-pairs/Pipeline_B/random_solar_capacity_factors.csv') as file_obj:
        csv_reader = csv.reader(file_obj)
        rows = list(csv_reader)

        for i in loc_index_list:
            y_axis.append(rows[i])
    
    for i in y_axis:
        i.pop(0)
    
    y_axis = [[float(s) for s in sublist] for sublist in y_axis]

    count = 1
    for i in y_axis:
        plt.plot(x_axis, i, label = "Line " + str(count))

        ### add code later to match label to city name

        count += 1
    plt.xlabel("Time (Hrs)")
    plt.ylabel("Capacity Factors")
    plt.title("Hourly Solar Capacity Factors")
    plt.legend()
    plt.show()

graph_solar_CF()