import matplotlib.pyplot as plt
import cartopy.crs as ccrs
# set projection
ax = plt.axes(projection=ccrs.Robinson(central_longitude=150))
# plot coastlines & gridlines
ax.coastlines()
ax.gridlines(linestyle='--')
# show figure
plt.show()