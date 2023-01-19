import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

solar_data = pd.read_csv('/Users/mirandaliu/Documents/GitHub/ibm-pairs/Data/Solar_and_Wind/tracking_solar_output.csv')
solar_data = solar_data.set_index('PAIRS polygon ID', drop = True)
solar_transposed = solar_data.T
yearly_sum = solar_transposed.sum()
#calculating CF
optimum_power_output = 50000000 * 366 * 24

cf = yearly_sum / optimum_power_output

#setting VOM:
VOM_non_fuel = 0
VOM_fuel = 0
LCOE_VOM = VOM_non_fuel + VOM_fuel

#setting FOM
FOM = 21.37447402
LCOE_FOM = FOM / (cf * 8760)

#setting capex
OCC = 1194.776032

CapRegMult = 1
L = 30

#setting capex grid
GF = 0
OnSpurCost = 0
OffSpurCost = 0
GCC = GF + OnSpurCost + OffSpurCost

#setting general finance
i = 0.025
IR_nom = 4/100
IR = (IR_nom - i) / (1 + i)
TR = 0.2574
DF = 0.735
RROE_nom = 0.078
RROE = (RROE_nom - i) / (1 + i)
WACC = ((1+((1-DF)*((1+RROE)*(1+i)-1)) + (DF*((1+IR)*(1+i)-1)*(1-TR))) / (1+i)) - 1
CRF = WACC / (1 - (1 / (1 + WACC)**L))

#setting project finance
M = 6
FD_y1 = 0.2
FD_y2 = 0.32
FD_y3 = 0.192
FD_y4 = 0.1152
FD_y5 = 0.1152
FD_y6 = 0.0576

f_y1 = 1 / ((1 + WACC) * (1 + i))**1
f_y2 = 1 / ((1 + WACC) * (1 + i))**2
f_y3 = 1 / ((1 + WACC) * (1 + i))**3
f_y4 = 1 / ((1 + WACC) * (1 + i))**4
f_y5 = 1 / ((1 + WACC) * (1 + i))**5
f_y6 = 1 / ((1 + WACC) * (1 + i))**6

PVD = FD_y1 * f_y1 + FD_y2 * f_y2 + FD_y3 * f_y3 + FD_y4 * f_y4 + FD_y5 * f_y5 + FD_y6 * f_y6
ProFinFactor = (1 - TR * PVD) / (1 - TR)

FRC = CRF * ProFinFactor

#setting capex - construction finance
C = 1
FC = 1
LDC = 0.8

IDC = 0.035

AI = 1 + ((1 + IDC) ** (0+0.5) - 1)
EDC = 1 - LDC

EPC = 0.02
CEC = EPC + RROE_nom
AEC = 1 + ((1 + CEC) ** (0 + 0.5) - 1)
ConFinFactor = (FC * AI * LDC) + (FC * AEC * EDC)

#finding capex
CAPEX = (OCC * CapRegMult + GCC) * ConFinFactor

#finding outputs
LCOE_capex = FRC * CAPEX / (cf * 8760) #$/KWh
LCOE = LCOE_capex + LCOE_FOM + LCOE_VOM #$/KWh
#print(LCOE)

# final adjustments for efficiency
efficiency_ref = 0.20
LCOE_capex = LCOE_capex * efficiency_ref / 0.26
LCOE_FOM = LCOE_FOM * efficiency_ref / 0.26
LCOE_VOM = LCOE_VOM * efficiency_ref / 0.26

LCOE = (LCOE_capex + LCOE_FOM + LCOE_VOM) * 1000 # $/MWh

LCOE.to_csv('/Users/mirandaliu/Documents/GitHub/ibm-pairs/Data/Solar_and_Wind/solar_LCOE_column.csv')

LCOE_shape_df = pd.DataFrame(index = range(1, 1451), columns = ['LCOE'])
LCOE_shape_df['LCOE'] = LCOE
LCOE_shape_np = LCOE_shape_df.to_numpy()
LCOE_shape_np_final = np.reshape(LCOE_shape_np, (25, 58), order = 'F')

#make a heatmap out of
plt.imshow(LCOE_shape_np_final, cmap='RdPu') #plasma is good for solar
plt.colorbar()
# plt.clim(35, 62)
plt.title('Solar LCOE ($/MWh)')
plt.show()

LCOE_shape_df_final = pd.DataFrame(LCOE_shape_np_final)
LCOE_shape_df_final.to_csv('/Users/mirandaliu/Documents/GitHub/ibm-pairs/Data/Solar_and_Wind/solar_LCOE.csv')


print('solar power output to TEA is done :)')

