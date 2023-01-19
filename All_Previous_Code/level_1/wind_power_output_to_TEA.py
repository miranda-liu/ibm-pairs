import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

wind_data = pd.read_csv('/Users/mirandaliu/Documents/GitHub/ibm-pairs/Data/Solar_and_Wind/tracking_wind_output.csv')
wind_data = wind_data.set_index('PAIRS polygon ID', drop = True)
wind_transposed = wind_data.T
yearly_sum = wind_transposed.sum()

print(yearly_sum.min()/2.55/1000000/24/366)
print(yearly_sum.max()/2.55/1000000/24/366)

CAPITAL_FRACTION = [0.8, 0.1, 0.1]
DEPRECIATION = [0.2, 0.32, 0.192, 0.1152, 0.1152, 0.0576]

#calculating CF
optimum_power_output = 2.55 * 1000000 * 366 * 24

cf = yearly_sum / optimum_power_output

#print(cf.min())
#print(cf.max())

cap_reg_mult = 1.289036667 #true for mass
lifetime = 30
grid_cost = 0
fuel_cost = 0

ir = 0.025 #Inflation Rate
i = 0.025470741 #Interest Rate
ic = 0 #Interest During Construction
rre = 0.076147376 # Rate of Return on Equity
df = 0.4 #Debt Fraction
tr = 0.2574 #Tax Rate (Federal and State)

#assuming NREL onshore
OCC = 1242 # $/kW
FOM = 24 # $/kW-year
VOM = 0

economies_of_scale_factor = 3/100

turbine_size = 2.55 #MW
windfarm_size = 2.55 #MW
ref_turbine = 3.4 #MW
ref_windfarm = 600 #MW

turbine_scaling_factor = (turbine_size / ref_turbine) ** economies_of_scale_factor
windfarm_scaling_factor = (windfarm_size / ref_windfarm) ** economies_of_scale_factor

OCC = OCC * turbine_scaling_factor * windfarm_scaling_factor

# Weighted Average Capital Cost
WACC = ((1 + ((1 - df) * ((1 + rre) * (1 + ir) - 1)) + (df * ((1 + i) * (1 + ir) - 1) * (1 - tr))) / (1 + ir)) - 1

# Capital Recovery Factor
CRF = WACC / (1 - (1 / (1 + WACC) ** lifetime))

# Depreciation - calculate the present value of PVD and multiply with dep factor
PVD = 0
for year, dep_rate in enumerate(DEPRECIATION):
    PVD += (1 / ((1 + WACC) * (1 + i)) ** year) * dep_rate

# Project Financing Factor
PFF = (1 - tr * PVD) / (1 - tr)

# Construction Financing Factor depends upon the time taken to construct
CFF = 0
for year, cap_frac in enumerate(CAPITAL_FRACTION):
    CFF += (1 + (1 - tr) * ((1 + ir) ** (year + 0.5) - 1)) * cf

# End of finance based calculations - assembling costs together
CAPEX = CFF * (OCC * cap_reg_mult + grid_cost)
FCR = CRF * PFF

capital = FCR * CAPEX * 1000 / (cf * 8760)
fixed = FOM * 1000 / (cf * 8760)
total = capital + fixed + VOM + fuel_cost # $/MWh
total = total * (1 - 0.063)


LCOE_shape_df = pd.DataFrame(index = range(1, 1451), columns = ['LCOE'])
LCOE_shape_df['LCOE'] = total
LCOE_shape_np = LCOE_shape_df.to_numpy()
LCOE_shape_np_final = np.reshape(LCOE_shape_np, (25, 58), order = 'F')

print(total.min())
print(total.max())

#make a heatmap out of
plt.imshow(LCOE_shape_np_final, cmap='RdPu') #plasma is good for solar
plt.colorbar()
plt.clim(30, 74)
plt.title('Wind LCOE ($/MWh)')
plt.show()

LCOE_shape_df_final = pd.DataFrame(LCOE_shape_np_final)
total.to_csv('/Users/mirandaliu/Documents/GitHub/ibm-pairs/Data/Solar_and_Wind/wind_LCOE_column.csv')
LCOE_shape_df_final.to_csv('/Users/mirandaliu/Documents/GitHub/ibm-pairs/Data/Solar_and_Wind/wind_LCOE.csv')


print('wind power output to TEA is done :)')