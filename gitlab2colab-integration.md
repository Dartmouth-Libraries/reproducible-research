# Gitlab/Hub to Google Colab Integration

+ Do you want to teach a course using a Google Colab Notebook and would you like to pull data from Gitlab or GitHub?
+ Are you teaching using our JupyterHub platform (jhub.dartmouth.edu), but would like to create a backup option?

If you answer yes to either of these questions, you are in the right place.

## Opening your Jupyter Notebook in Colab


1. Upload your Jupyter Notebook to a Google Drive folder of your choosing.
2. Open the notebook from within your Google Drive folder. It will be automatically opened in Colab.
3. Try running your cell(s) that import Python libraries / packages to see if there are any libraries not already installed in Colab.
    a. If the running of these import commands raises any errors, you can insert a cell above the import cell to install the missing packages, for example:
        `!pip install nltk`

## Importing Data into Colab

The remainder of this guide will outline three principle ways you and your students can import data into a Colab notebook.

## Option 1: Importing Data from Github/lab into Colab

1. First, go to the repo in GitHub/Lab that has your data. 
    + Select the down arrow next to the download icon.
    + Right-click or Command-Click on the zip button and select copy link
    ![text](images/zip-link.png)
2. 	Insert a cell in your notebook that gets and unzips the data from your GitHub/Lab account.
	+ ! wget [paste copied link here]
	+ ! unzip [insert just the name (not the full path) of the zipped file]
	+ Example:
    ```
    ! wget https://git.dartmouth.edu/lib-digital-strategies/RDS/datasets/inaugural-addresses/-/archive/master/inaugural-addresses-master.zip
	! unzip inaugural-addresses-master.zip
    ```
					
	+ You can now access the data from the unzipped version of the folder using the folder directory on the left side of your Colab notebook
        + *Note:* For any code cells in your notebook that imports this data using relative or absolute paths, you may need to modify these filepaths to reflect the location of this data relative within your Colab notebook. 

## Option 2: Importing Data from Dropbox into Colab

1. Open Dropbox and navigate to the folder or file you want to share
2. Right-click / Command-click the folder and select copy link
3. In Colab, insert the following into a cell to import an entire folder:
	
    ```
    !wget -O [dropbox link]`
    ```
4. To import one file at  a time:

    ```
    !wget -O [name of specific file, i.e. gapminder.csv] [dropbox link]
    ```


## Option 3: Have participants download data from you and then upload it to Colab

You may also ask workshop participants to download the data onto their own computers and then upload that data into Colab manually. 

1. First, add a cell at the top of your Colab notebook that contains:

```
from google.colab import files
files.upload()

```
2. Share your data with students (i.e. through link to Google Drive folder)
2. Instruct students to download the files onto their own computer and save it in a folder created just for this workshop.
3. 


*This guide created by Jeremy Mikecz, Research Data Services, Dartmouth Library*

