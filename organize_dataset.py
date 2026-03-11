import os
import pandas as pd
import shutil

# paths
metadata_path = "HAM10000_metadata.csv"
image_folder = "dataset/images"
dataset_folder = "dataset"

# read metadata
data = pd.read_csv(metadata_path)

# create disease folders
labels = data['dx'].unique()

for label in labels:
    os.makedirs(os.path.join(dataset_folder, label), exist_ok=True)

# move images to correct folder
for index, row in data.iterrows():
    
    image_name = row['image_id'] + ".jpg"
    label = row['dx']
    
    source = os.path.join(image_folder, image_name)
    destination = os.path.join(dataset_folder, label, image_name)
    
    if os.path.exists(source):
        shutil.move(source, destination)

print("Dataset organized successfully")