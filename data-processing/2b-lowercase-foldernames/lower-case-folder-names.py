import os

# Function to lowercase folder names recursively
def lowercase_folder_names(root_directory):
    for root, dirs, files in os.walk(root_directory, topdown=False):
        for dir_name in dirs:
            original_path = os.path.join(root, dir_name)
            lowercased_path = os.path.join(root, dir_name.lower())

            # Rename the folder to lowercase
            os.rename(original_path, lowercased_path)

if __name__ == "__main__":
    # Use the current directory as the root directory
    root_directory = './'

    # Call the function to lowercase folder names
    lowercase_folder_names(root_directory)

    print("Folder names in the current directory have been lowercased.")
