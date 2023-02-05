# ibm-pairs
# MITEI UROP

Onboarding info: https://drive.google.com/drive/folders/1eEDbx0iKATmOoVPijliRgdBJNy3x8YZu?usp=sharing

Dropbox: https://www.dropbox.com/scl/fo/ja83hkbetvplj52he0tt3/h?dl=0&rlkey=wevg21lm0dj980j9blngt9lio

# Reference papers

1. https://reader.elsevier.com/reader/sd/pii/S0960148116310680?token=5B4A271B23F4FAC3793E7DD40DD6A879245B4B8E9939938C42B6C041E2FBE775F43BB38C7CFF7A4D4ECBB7F7C54C490A&originRegion=us-east-1&originCreation=20230111163203

2. https://reader.elsevier.com/reader/sd/pii/S1364032120304421?token=F571F500D91C3EE7C25892FA2A1AEEA3F0EFB285BE13C6BE2D72018B41CB9A16D71A925247F0D40CA1E4449D2D183647&originRegion=us-east-1&originCreation=20230111224702

3. https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8547649

## Reference for CF calculations

1. https://github.com/patrickbrown4/zephyr/blob/main/zephyr/pv.py (Photovoltaic, lines 426-584)
2. https://github.com/patrickbrown4/zephyr/blob/main/zephyr/wind.py (Wind, lines 421-592)


# Order to run files in Pipeline B:

1. solar_cf_generator.py
    - Generates random capacity factors for solar
    - Returns list of capacity factors or csv file (random_solar_capacity_factors.csv)
2. wind_cf_generator.py
    - Generates random capacity factors for wind
    - Returns list of capacity factors or csv file (random_wind_capacity_factors.csv)
3. solar_rf_calculations.py
    - Calculates reliability factors for solar
    - Returns 3d array of reliability factors or csv file (solar_reliability_factors.csv)
4. wind_rf_calculations.py
    - Calculates reliability factors for wind
    - Returns 3d array of reliability factors or csv file (wind_reliability_factors.csv)
5. graphing_solar_rf.py
    - Graphs solar reliability factors (mean, standard deviation) on heat maps
6. graphing_solar_rf_line.py
    - Graphs solar reliability factors of multiple locations as line graph
7. graphing_wind_rf.py
    - Graphs wind reliability factors (mean, standard deviation) on heat maps
8. graphing_wind_rf_line.py
    - Graphs wind reliability factors of multiple locations as line graph
9. combining_wind_solar_cf.py
    - Combines CF profiles of solar and wind, then calculates a combined RF
    - Returns combined_capacity_factors.csv, combined_reliability_factors.csv, and 3d array of combined RFs
10. graphing_solar_cf_line.py
    - Graphs solar CFs over time as line graph
11. graphing_wind_cf_line.py
    - Graphs wind CFs over time as line graph
12. graphing_combined_rf.py
    - Graphs combined wind and solar reliability factors (mean, standard deviation) on heat maps
