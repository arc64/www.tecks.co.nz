import os

# Specify the paths to Example A and Example B directories
example_a_path = "./Origin"
example_b_path = "./Destination"

# Define a function to copy text from source to destination
def copy_text(source_file, dest_file):
    with open(source_file, "r") as source:
        with open(dest_file, "w") as dest:
            dest.write(source.read())

# Traverse Example B directory and copy text from Example A to Example B
for root, dirs, files in os.walk(example_b_path):
    for file in files:
        if file.endswith(".md") and file != ".DS_Store":
            # For index.md files
            if file == "index.md":
                relative_path = os.path.relpath(root, example_b_path)
                source_path = os.path.join(
                    example_a_path,
                    relative_path.capitalize().replace(" ", "").replace("-", ""),
                )
                source_file = os.path.join(source_path, "index.md")
                dest_file = os.path.join(root, "index.md")
                
                if os.path.exists(source_file):
                    copy_text(source_file, dest_file)

            # For other .md files in Example B
            else:
                # Modify the file name to get the corresponding folder name in Example A
                folder_name = file.replace(".md", "").capitalize().replace(" ", "").replace("-", "")
                relative_path = os.path.relpath(root, example_b_path)
                
                # Capitalize the first letter of each folder name
                path_parts = relative_path.split(os.path.sep)
                capitalized_path = os.path.sep.join(part.capitalize().replace(" ", "").replace("-", "") for part in path_parts)
                
                source_path = os.path.join(
                    example_a_path,
                    capitalized_path,
                    folder_name)
                source_file = os.path.join(source_path, "index.md")
                
                dest_file = os.path.join(root, file)

                print(f"Source File (Example A): {source_file}")
                print(f"Destination File (Example B): {dest_file}")

                if os.path.exists(source_file):
                    copy_text(source_file, dest_file)
