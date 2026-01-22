# library & dataset
# vs code choose python environment, for example choose Python 3.12.2 /usr/local/bin/python3 Global Env

import seaborn as sns

## histogram
df = sns.load_dataset('iris')

# Plot the histogram / distribution thanks to the displot function
sns.displot( data=df["sepal_length"] )

## histogram with kde line 

# library & dataset
import pandas as pd
import matplotlib.pyplot as plt

df = sns.load_dataset('iris')

# Plot the histogram thanks to the displot function, add kde line 
sns.displot( data=df["sepal_length"], kde=True )


## scatterplot
plt.rcParams["figure.dpi"] = 300
df = sns.load_dataset('iris')
 
# Use the 'hue' argument to provide a factor variable
# plot by species, scatterplot, x is length y, is width
sns.scatterplot(
   x="sepal_length",
   y="sepal_width",
   data=df,
   hue='species',
)

plt.show()

## scatterplot with markers 

# library & dataset
import seaborn as sns
import matplotlib.pyplot as plt
df = sns.load_dataset('iris')
 
# Plot with specified markers for each species
sns.scatterplot(
    x="sepal_length",
    y="sepal_width",
    data=df,
    hue='species',
    style='species',
)

plt.show()

##

#Some common plot types: 

#Distribution Plot / Histogram 

#Joint Plot

#KDE Plot

#Pair Plot 

#Box Plot / Box and whisker plot 

#Violin Plot 

#Strip Plot 

#Swarm Plot 

#Matrix Plots 

#Heatmaps 

penguins_upload = pd.read_csv("penguins_export.csv")

# Seaborn’s stripplot shows every individual observation.
sns.stripplot(
    data=penguins_upload,
    x="species",
    y="body_mass_g",
    jitter=True,                 # spreads points a little for readability
    palette=["#1f77b4", "#ff7f0e", "#2ca02c"],  # blue, orange, green
    size=8,
    edgecolor="gray",
    linewidth=0.5,
)

plt.title("Penguin Body Mass by Species")
plt.ylabel("Body mass (g)")
plt.xlabel("Species")
plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()