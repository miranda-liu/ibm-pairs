from matplotlib import pyplot as plt
import numpy as np

plt.rcParams['figure.figsize'] = (8, 6)
ax = plt.axes(projection = '3d')
#ax.scatter3D(lat, long, value, s = 10)
ax.set_xlabel('Latitude')
ax.set_ylabel('Longitude')
ax.set_zlabel('Irradiance Value (Units)')

ax.view_init(45, 45)
plt.show()