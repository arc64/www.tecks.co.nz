import os
import csv

# Specify the root directory to check for empty files
root_directory = "./"

# Function to check if a file is empty
def is_file_empty(file_path):
    return os.path.exists(file_path) and os.stat(file_path).st_size == 0

# List to hold paths of empty files
empty_files = []

# Traverse the directory structure
for root, dirs, files in os.walk(root_directory):
    for file in files:
        file_path = os.path.join(root, file)
        if is_file_empty(file_path):
            empty_files.append(file_path)

# Write the paths of empty files to a CSV file
csv_file_path = "empty_files.csv"
with open(csv_file_path, "w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Empty File Path"])
    for file_path in empty_files:
        csv_writer.writerow([file_path])

# Print a message with the results
if empty_files:
    print(f"Empty files found. See '{csv_file_path}' for details.")
else:
    print("No empty files found.")
