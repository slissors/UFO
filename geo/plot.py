import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point

# Load data
data_path = "geo/test_weather.csv"
shape_path = "geo/Shapefiles/cb_2018_us_state_500k.shp"
ufo_path = "geo/yearly_coordinates/sightings_coordinates_2014.csv"

# Read CSV and shapefile data
df = pd.read_csv(data_path)
shape = gpd.read_file(shape_path)
udf = pd.read_csv(ufo_path)

# Exclude non-mainland areas
shape = shape[~shape['STUSPS'].isin(['HI', 'AK', 'PR', 'AS', 'VI', 'MP', 'GU'])]

# Create GeoDataFrames for weather balloons and UFO sightings
geometry_balloons = [Point(xy) for xy in zip(df['city_longitude'], df['city_latitude'])]
geo_bdf = gpd.GeoDataFrame(df, geometry=geometry_balloons)

geometry_ufo = [Point(xy) for xy in zip(udf['city_longitude'], udf['city_latitude'])]
geo_udf = gpd.GeoDataFrame(udf, geometry=geometry_ufo)

# Set CRS to EPSG:4326
geo_bdf.set_crs(epsg=4326, inplace=True)
geo_udf.set_crs(epsg=4326, inplace=True)
shape.to_crs(epsg=4326, inplace=True)

# Convert GeoDataFrames to projected CRS (EPSG:5070, NAD83 / Conus Albers)
projected_crs = "EPSG:5070"
geo_bdf_projected = geo_bdf.to_crs(projected_crs)
geo_udf_projected = geo_udf.to_crs(projected_crs)
shape_projected = shape.to_crs(projected_crs)

# Create buffers around weather balloons with a 5-mile radius
buffer_distance = 5 * 1609.34  # 5 miles in meters
geo_bdf_projected['buffer'] = geo_bdf_projected.buffer(buffer_distance)

# Extract the buffer geometries and convert them back to EPSG:4326 for plotting
buffers = geo_bdf_projected[['buffer']].copy()
buffers.set_geometry('buffer', inplace=True)
buffers.to_crs(epsg=4326, inplace=True)

# Perform spatial overlay to keep only UFO points within US borders
points_within_us = gpd.overlay(geo_udf_projected, shape_projected, how='intersection')

# Convert points_within_us back to EPSG:4326 for plotting
points_within_us = points_within_us.to_crs(epsg=4326)

# Plot the data
fig, ax = plt.subplots(figsize=(15, 15))
shape.plot(ax=ax, color='white', edgecolor='black')
geo_bdf.plot(ax=ax, color='blue', markersize=10, alpha=0.6, label='Weather Balloons')
points_within_us.plot(ax=ax, color='red', markersize=5, alpha=0.6, label='UFO Sightings')
buffers.boundary.plot(ax=ax, color='blue', linewidth=2, label='5-Mile Radius')

# Add titles and labels
ax.set_title('Weather Balloons and UFO Sightings in the United States with 5-Mile Radius Circles', fontsize=20)
ax.set_xlabel('Longitude', fontsize=15)
ax.set_ylabel('Latitude', fontsize=15)
ax.legend()

# Show plot
plt.show()
