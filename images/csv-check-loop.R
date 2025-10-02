



# set working directory 
# getwd [1] "/Volumes/lib-RDS/Gaughan/Randell/results" 
# 
dirname(rstudioapi::getActiveDocumentContext()$path)
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
getwd()

print('wd:')
print(getwd())
dir_path <- "../results"
#setwd(dir_path)

# Set the directory containing the CSV files
csv_dir <- "../results"

# Get a list of CSV files in the directory
csv_files <- list.files(path = csv_dir, pattern = "\\.csv$", full.names = TRUE)

for (file in csv_files) {
  # Read the CSV file into a dataframe
  df <- read.csv(file)
  
  # Print a message indicating which file we're processing
  cat("First 5 rows and first 5 columns of", basename(file), ":\n")
  
  # Subset first 5 rows and first 5 columns (handle cases with fewer columns)
  n_cols <- min(ncol(df), 7)
  preview <- df[1:3, 1:n_cols]
  
  # Print the preview
  print(preview)
  
  cat("\n")  # Add a blank line for readability between files
}



# # Loop over each CSV file
# for (file in csv_files) {
#   # Read the CSV file into a dataframe
#   df <- read.csv(file)
#   
#   # Print a message indicating which file we're processing
#   cat("First rows of", basename(file), ":\n")
#   
#   # Print the first 5 rows
#   print(head(df, 3))
#   
#   cat("\n")  # Add a blank line for readability between files
# }

