import os

# Specify the directory path where you want to remove hyphens
target_directory = './'

def remove_hyphens_from_names(directory_path):
    for root, dirs, files in os.walk(directory_path):
        # Rename directories
        for directory in dirs:
            new_directory = directory.replace('-', '')  # Remove hyphens
            if new_directory != directory:
                old_path = os.path.join(root, directory)
                new_path = os.path.join(root, new_directory)
                os.rename(old_path, new_path)
                print(f'Renamed directory: {old_path} -> {new_path}')

        # Rename files
        for file_name in files:
            new_file_name = file_name.replace('-', '')  # Remove hyphens
            if new_file_name != file_name:
                old_path = os.path.join(root, file_name)
                new_path = os.path.join(root, new_file_name)
                os.rename(old_path, new_path)
                print(f'Renamed file: {old_path} -> {new_path}')

if __name__ == '__main__':
    remove_hyphens_from_names(target_directory)
    print('Hyphens removed from folder and file names in the specified directory and its subdirectories.')
