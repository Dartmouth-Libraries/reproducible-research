# R spatial, point-in-polygon 

# setwd('~/Desktop/bears_parks/') # mac

# tip, always comment your code! 

setwd('C:/Users/usr/Desktop/bears_parks')
print(" Mac: setwd('~/Desktop/bears_parks/' ")
print(" PC: setwd('C:/Users/usr/Desktop/bears_parks')")
print(" Another method - in RStudio, click More > Go to working directory  ")

# install package 
install.packages("leaflet")
library(leaflet)
longitude_x <- -72.2900578
latitude_y <- 43.703016

m <- leaflet() %>%
  addTiles()  # add OpenStreetMap map tiles
# draw the map
m  # Print the map

m <- leaflet() %>%
  addTiles() %>%  # add OpenStreetMap map tiles
  addMarkers(lng=longitude_x, lat=latitude_y, popup="Dartmouth College!")
m  # Print the map

# tip, use Control Return key combination to run the line from a script!

# three basic steps, create a map widget by calling leaflet().
# Add layers (i.e., features) to the map by using layer functions (e.g. addTiles, addMarkers, addPolygons) to modify the map widget, repeat as desired.
# Print the map widget to display it.

m <- leaflet() %>%
  addTiles() %>%  # add OpenStreetMap map tiles
  addMarkers(lng=174.768, lat=-36.852, popup="The birthplace of R")
m  # Print the map

# ---------------------------
getwd()     

# tip - in RStudio, click More > Go to working directory to go to the working directory! 

# create a string variable for our results directory
resultsdir <- paste(getwd(),"/results", sep = "")

# built-in "unzip" function 
unzip(zipfile = "data/nationalparks.zip", exdir = resultsdir)

# built-in read.csv function 
bears <- read.csv('data/bear-sightings.csv')

# ---------------------------------------------
# use sp package's coordinates function to set the 
#  coordinates for the bears csv, and convert it in 
#  to a "formal class spatialpointsdataframe

#install.packages("sp")

#  tip, use a statement like this to install only if needed! 
if(!require("sp")) install.packages("sp")

# initialize the package's library: 
library(sp)

# coordinates" function from the "sp" package 
coordinates(bears) <- c('longitude','latitude')

#--------------------------------------------------
# let's see if the "bear-sightings" csv has valid coordinates in it - do the coordinates land in Alaska? 
# this line checks to see if a package is installed already 
"maps" %in% rownames(installed.packages()) == TRUE

if(!require("maps")) install.packages("maps")
library(maps)
# plot the coordinates of the bears 
plot(coordinates(bears))
# use the "maps" package to add a coarsely-drawn map layer for context 
map("world", region="usa", add=TRUE)  # from the "maps" package 

# ------------
"rgdal" %in% rownames(installed.packages()) == TRUE
if(!require("rgdal")) install.packages("rgdal")
library(rgdal)   
# GDAL = geospatial data abstraction library. Open source! 
# Check out their website at https://www.osgeo.org/ and https://www.gdal.org/

# get the working directory 
getwd()

# OGR stands for Open Geographic Reference 
parks <- readOGR('.', '10m_us_parks_area')   
ourprojection <- proj4string(parks)
print(ourprojection)

# --
# use the sp package's proj4string to set the projection of 
#  the new "bears" spatial data frame to the same projection as the parks dataset  
proj4string(bears) <- proj4string(parks)
# the 'over' function 
insidePark <- !is.na(over(bears, as(parks, "SpatialPolygons")))
# view in Rstudio environment window 
# Spatial analysis goal #1 - get the fraction of bears inside a park! 
mean(insidePark)

# use 'cat' to concatenate a string and send it to our console
# did we all get the same result? 

cat("Percent inside parks: ", 100*mean(insidePark), ' percent ')
# let's create a visualization for output: 
slices <- c(mean(insidePark), 1-mean(insidePark)) 
lbls <- c("Bears in the parks", "Bears outside the parks")
pct <- round(slices/sum(slices)*100,2)

lbls <- paste(lbls, pct)                 # add percents to labels 
lbls <- paste(lbls,"%",sep="")      # add % to labels 
pie(slices,labels = lbls, col=rainbow(length(lbls)),
    main="Bear Sightings")
# let's save a copy of this great plot in to our 'results' folder 
dev.copy(jpeg,'../results/myplot.jpg')
dev.off()     # dev.off tells R Studio to send the plot out rather than plot it

# use 'over' again, this time with parks as a SpatialPolygonsDataFrame
# store the park name as an attribute of the bears data
bears$park <- over(bears, parks)$Unit_Name
# write a csv file with bear names and the name of the park (if found) 
write.csv(bears, "../results/bears-by-park.csv", row.names=FALSE)

# hang in there, almost done! 
library(maps)
plot(coordinates(bears))
map("world", region="usa", add=TRUE)  # from the "maps" package 
plot(parks, border="green", add=TRUE)

# set the colors for the points inside and outside the park 
points(bears[insidePark,],pch=16,col="red")
points(bears[!insidePark,], pch=1,col="green")
# send the plot to our results folder 
dev.copy(jpeg,'../results/mymap.jpg')
dev.off()

# end of point-in-polygon analysis 
### ------------------------------


