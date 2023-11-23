import os
import csv

# Specify the paths to Example A and Example B directories
example_a_path = "./Origin"
example_b_path = "./Destination"

# Define a function to copy text from source to destination
def copy_text(source_file, dest_file):
    try:
        with open(source_file, "r") as source:
            with open(dest_file, "w") as dest:
                dest.write(source.read())
        return True
    except Exception as e:
        return False

# List to hold paths of files that couldn't be copied
failed_copies = []

# Traverse Example B directory and copy text from Example A to Example B
for root, dirs, files in os.walk(example_b_path):
    for file in files:
        if file.endswith(".md") and file != ".DS_Store":
            # For index.md files
            if file == "index.md":
                relative_path = os.path.relpath(root, example_b_path)
                source_path = os.path.join(
                    example_a_path,
                    relative_path.replace(" ", "").replace("-", ""),
                )
                source_file = os.path.join(source_path, "index.md")
                dest_file = os.path.join(root, "index.md")
                
                if not os.path.exists(source_file) or not copy_text(source_file, dest_file):
                    failed_copies.append((source_file, dest_file))

            # For other .md files in Example B
            else:
                # Modify the file name to get the corresponding folder name in Example A
                folder_name = file.replace(".md", "").replace(" ", "").replace("-", "")
                relative_path = os.path.relpath(root, example_b_path)
                
                # Remove spaces and hyphens from each folder name in the path
                path_parts = relative_path.split(os.path.sep)
                modified_path = os.path.sep.join(part.replace(" ", "").replace("-", "") for part in path_parts)
                
                source_path = os.path.join(
                    example_a_path,
                    modified_path,
                    folder_name)
                source_file = os.path.join(source_path, "index.md")
                
                dest_file = os.path.join(root, file)

                if not os.path.exists(source_file) or not copy_text(source_file, dest_file):
                    failed_copies.append((source_file, dest_file))

# Write the failed file paths to a CSV file
with open("failed_copies.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Source File", "Destination File"])
    writer.writerows(failed_copies)

# If there are failed copies, print message
if failed_copies:
    print(f"Some files couldn't be copied. See 'failed_copies.csv' for details.")
else:
    print("All files were successfully copied.")
