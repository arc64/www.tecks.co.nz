import os

# Specify the paths to Example A and Example B directories
example_a_path = "path/to/ExampleA"
example_b_path = "path/to/ExampleB"

# Define a function to copy text from source to destination
def copy_text(source_file, dest_file):
    with open(source_file, "r") as source:
        with open(dest_file, "w") as dest:
            dest.write(source.read())

# Traverse Example A directory and copy text to Example B
for root, dirs, files in os.walk(example_a_path):
    for file in files:
        if file == "index.md":
            # Get the corresponding path in Example B with adjusted folder names
            relative_path = os.path.relpath(root, example_a_path)
            dest_path = os.path.join(
                example_b_path,
                relative_path.capitalize().replace(" ", "").replace("-", ""),
            )

            # Check if the corresponding folder in Example B exists
            if os.path.exists(dest_path):
                if os.path.isdir(dest_path):
                    # It's a folder with nested content, so copy to 'index.md'
                    dest_file = os.path.join(dest_path, "index.md")
                    if os.path.exists(dest_file):
                        copy_text(os.path.join(root, file), dest_file)
                else:
                    # It's a page with no children, so copy to 'folder-name.md'
                    dest_file = os.path.join(
                        example_b_path,
                        relative_path.capitalize().replace(" ", "").replace("-", "") + ".md",
                    )
                    copy_text(os.path.join(root, file), dest_file)
