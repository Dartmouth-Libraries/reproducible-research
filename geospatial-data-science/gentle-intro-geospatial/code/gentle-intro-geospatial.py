# geospatial overlay / points-in-polygons data analysis and visualization 

#!pip install geopandas

# import standard python libraries
import pandas as pd
import matplotlib.pyplot as plt
# immport spatial & geospatial libraries
import geopandas as gpd
import shapely

# read in the CSV file with the bear sighting locations directly from the web
points_csv = pd.read_csv('https://rcweb.dartmouth.edu/homes/f002d69/workshops/data/bear-sightings.csv')

#download zip file from web, and upload
#https://rcweb.dartmouth.edu/~f002d69/workshops/index_python_spatial.html
# colab options:  
# from google.colab import files
# Upload the shapefile from your Mac desktop
#uploaded = files.upload()
# upload 'nationalparks.zip' file downloaded from dartgo.org/python-spatial
# Get the file name
#file_name = list(uploaded.keys())[0]

# Load the shapefile into GeoDataFrame
polygons_shapefile_zipped = gpd.read_file(file_name)

# Display the first three rows of the nationa parks shapefile
print(polygons_shapefile_zipped.head(3))

# convert the points to a geopandas 'geodataframe'
points = gpd.GeoDataFrame(
    points_csv, geometry=gpd.points_from_xy(points_csv.longitude, points_csv.latitude)
)
points.head(2)

points.crs = 'EPSG:4326'  # Replace with the CRS of your data if different
# Reproject the points to match the CRS of the polygons
points = points.to_crs(polygons_shapefile_zipped.crs)
# confirm the coordinate system / spatial reference
points.crs.to_epsg()

# Perform the point-in-polygon overlay
points_in_polygons = gpd.sjoin(points, polygons_shapefile_zipped, predicate='within')
points_in_polygons.head(2)

# Plot the polygons
polygons_shapefile_zipped.plot(edgecolor='k', facecolor='none', alpha=0.5)

points.plot(marker='o', color='blue', markersize=3,ax=plt.gca())

# Plot the points within polygons
points_in_polygons.plot(marker='o', color='red', markersize=5, ax=plt.gca())

# Show the map
plt.axis('off')
plt.show()

# create a folium map, complete with in-notebook zoom tools
map = folium.Map(location=[62.65822, -148.95602],
    zoom_start=5,
    control_scale=True)
# loop through points
for index, row in points.iterrows():
    folium.CircleMarker(location=[ row.latitude,row.longitude], radius =5).add_to(map)
# loop through points in polygons, color them gray
for index, row in points_in_polygons.iterrows():
    folium.CircleMarker(location=[ row.latitude,row.longitude], color = 'gray',fill=True, fill_opacity=1).add_to(map)
# display the map with points-in-polygons red, and the points outside polygons in blue 
map
