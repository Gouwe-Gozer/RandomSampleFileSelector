# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 12:49:46 2024

@author: Gouwe-Gozer
"""
###############################################################################
# 15/03/2024

# This script loads files listed in a folder (or subfolders of a folder), sets
# certain requirements for the files and then takes a random subsample of the
# files.
# The file names can then be written to a csv-file and/or the files can be copied 
# to a different folder.

###############################################################################

                          ### Loading packages ###
                  
try: # First see if the packages are already installed
    import os
    import random
    import shutil
    import pandas as pd
    from datetime import datetime
except ModuleNotFoundError: # Else install the packages first
#    !pip install random shutil os datetime
    import os
    import random
    import shutil
    import pandas as pd
    from datetime import datetime
    
    # This will still give a ModuleNotFoundError. Kernel needs to be restarted:
    # Console > restart kernel or Crtl + . 
    # Then rerun the code above

#############################   Variables   ###################################

# Specify the folder where your files are located
input_folder = 'C:/Users/User/Documents/main_folder/'

# Are your files nested? 
# i.e. are the files listed in subfolders of the input_folder?
nested = True

# What sample size do you want?
sample_size = 120


# Do you want to save the names of your subsample in a csv?
write_to_csv = True
# If so, list the directory you wish to save the csv to
output_csv = "C:/Users/User/Documents/"

csv_name = "subsample"

# Do you want to copy the selected files to a new folder?
copy_to_new_dir = True
# If so, list the directory you wish to save the csv to
output_folder = "C:/Users/User/Documents/subset_folder/"


                  #### File name requirements ####

# Do you only want to select certain file types/ a certain file type?
extension_requirement = True

extension = ".png"

# Do you only want to select files that contain a certain string?
name_requirement = True

# File name must contain (not case sensitive):
must_contain = "parrot"

# Alternatively, do you want to exclude any files based on there file name
exclude = True
# if so
cannot_contain = "donkey"


                      ### End of variable section ###
                      
     ### The script should not require any user input after these lines ###
###############################################################################
###############################################################################

# Create custom error to notify the end user of errors
class GouweGozerSays(Exception):
    """Custom exception class to notify the end-user"""
    pass

file_list = []
relative_path_list = []
if nested:
    # Use os.walk to list all files within the input folder and all subfolders.
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if (extension_requirement == False or file.lower().endswith(extension)) and \
                (name_requirement == False or (must_contain in file.lower()) and \
                 (exclude == False or cannot_contain not in file.lower())):
                file_list.append(file)
                # Construct the full path of the file using 'root'
                relative_path = os.path.join(root, file)
                relative_path_list.append(relative_path)

else:
    # Use os.listdir to list all files within the input folder
    for file in os.listdir(input_folder):
            if (extension_requirement == False or file.lower().endswith(extension)) and \
                (name_requirement == False or (must_contain in file.lower()) and \
                 (exclude == False or cannot_contain not in file.lower())):
                file_list.append(file)


print(f"I found a total of {len(file_list)} files in the folder that met your specifications. Does that seem right to you?")

subsample = random.sample(file_list, sample_size)

print(f"I created a random subsample of {sample_size} from all the files that I found. That's {(sample_size/len(file_list))*100}% of all the files! ")


if nested:
    subsample_paths = []
    # Iterate over the subsample of filenames
    for filename in subsample:
        # Iterate over the relative paths to find a match
        for path in relative_path_list:
            # Extract the filename from the path
            file_name_from_path = path.split("\\")[-1]
            # Check if the filename matches the subsample filename
            if filename == file_name_from_path:
                # If it matches, add the path to the list of selected paths
                subsample_paths.append(path)
                break  # Move to the next filename in the subsample


if copy_to_new_dir:
    if os.listdir(output_folder):
        raise MinnertSays(f"The output folder ({output_folder}) is not empty. Make sure you move or delete all current files before copying the subset files to the folder. This way the output folder only contians your subset. ")
    if nested:
        # Iterate over each file and copy it to the destination folder
        for i in range(0, len(subsample)):
            source_file_path = os.path.join(subsample_paths[i])
            destination_file_path = os.path.join(output_folder, subsample[i])
            shutil.copy(source_file_path, destination_file_path)
    else:
        for file in subsample:
            source_file_path = os.path.join(input_folder, file)
            destination_file_path = os.path.join(output_folder, file)
            shutil.copy(source_file_path, destination_file_path)
    
    print(f"{len(os.listdir(output_folder))} files copied to {output_folder}")             


if write_to_csv:
    
    csv_subsample = pd.DataFrame({
        'file name': subsample,
        })
    
    # Set name for csv
    today = datetime.today().date()
    today_string = today.strftime("%Y%m%d") + "_"
    # set path to csv
    file_name_csv = output_csv + today_string + csv_name + ".csv"

    csv_subsample.to_csv(file_name_csv, index=False)
    
    print(f"list of subsample file names written to {file_name_csv}") 
 
