import os
import csv
import yaml

# Path to the directory containing your Markdown files
base_directory = './'

# Path to the CSV file (updated to 'urls_with_depth_order_nav.csv')
csv_file = 'urls_with_depth_order_nav.csv'

# Read the CSV file and store the data in a dictionary
nav_order_data = {}
with open(csv_file, 'r') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for row in csv_reader:
        nav_order_value = row.get('nav_order', '').strip()
        file_name = row.get('FileNameNoSpaces', '').strip()

        # Strip ".md" extension if present
        if file_name.endswith('.md'):
            file_name = file_name[:-3]  # Remove the last 3 characters (".md")

        if nav_order_value and file_name:
            nav_order_data[file_name] = int(nav_order_value)

# Initialize counters for files modified and total files
files_modified_count = 0
total_files_count = len(nav_order_data)

# Initialize the list to store files that were not modified
files_not_modified = []

# Initialize the list to store files with non-integer nav_order values
non_integer_nav_order_files = []

# Function to update nav_order in YAML front matter
def update_nav_order_in_markdown(file_path, nav_order):
    global files_modified_count  # Use the global counter variable
    print(f"Processing file: {file_path}")

    try:
        with open(file_path, 'r') as markdown_file:
            lines = markdown_file.readlines()

        # Find the start and end of YAML front matter
        start_idx, end_idx = None, None
        for i, line in enumerate(lines):
            if line.strip() == '---':
                if start_idx is None:
                    start_idx = i
                else:
                    end_idx = i
                    break

        # Check if YAML front matter exists
        if start_idx is not None and end_idx is not None:
            # Extract the existing YAML front matter
            existing_front_matter = "".join(lines[start_idx + 1:end_idx])

            # Attempt to parse the YAML front matter
            try:
                yaml_front_matter = yaml.safe_load(existing_front_matter)
            except yaml.YAMLError as e:
                print(f"Error parsing YAML in {file_path}: {e}")
                return

            # Check if YAML front matter is a dictionary
            if isinstance(yaml_front_matter, dict):
                if 'nav_order' in yaml_front_matter:
                    nav_order_value = yaml_front_matter['nav_order']
                    if not isinstance(nav_order_value, int):
                        # Print both file path and expected matched path from the input CSV
                        print(f"Error: {file_path} - Expected nav_order: {nav_order} from CSV, Found: {nav_order_value}")
                        non_integer_nav_order_files.append(file_path)

                    yaml_front_matter['nav_order'] = nav_order

                    # Convert the updated YAML front matter back to a string with proper formatting
                    updated_yaml_lines = yaml.dump(yaml_front_matter, default_flow_style=False).splitlines()
                    updated_yaml_front_matter = '\n'.join(updated_yaml_lines)

                    # Replace the original YAML front matter with the updated content
                    lines[start_idx + 1:end_idx] = [line + '\n' for line in updated_yaml_front_matter.splitlines()]

                    # Write the updated content back to the file
                    with open(file_path, 'w') as markdown_file:
                        markdown_file.writelines(lines)

                    # Increment the counter for files modified
                    files_modified_count += 1
                    print(f"Updated {file_path} with nav_order {nav_order}")
                else:
                    # If 'nav_order' not present in YAML, add it with the provided value
                    yaml_front_matter['nav_order'] = nav_order

                    # Convert the updated YAML front matter back to a string with proper formatting
                    updated_yaml_lines = yaml.dump(yaml_front_matter, default_flow_style=False).splitlines()
                    updated_yaml_front_matter = '\n'.join(updated_yaml_lines)

                    # Replace the original YAML front matter with the updated content
                    lines[start_idx + 1:end_idx] = [line + '\n' for line in updated_yaml_front_matter.splitlines()]

                    # Write the updated content back to the file
                    with open(file_path, 'w') as markdown_file:
                        markdown_file.writelines(lines)

                    # Increment the counter for files modified
                    files_modified_count += 1
                    print(f"Updated {file_path} with nav_order {nav_order}")
            else:
                print(f"YAML front matter in {file_path} is not a dictionary.")
                # Add the file to the list of files that were not modified
                files_not_modified.append(file_path)
        else:
            print(f"No YAML front matter found in {file_path}.")
            # Add the file to the list of files that were not modified
            files_not_modified.append(file_path)

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        # Add the file to the list of files that were not modified
        files_not_modified.append(file_path)

# Walk through the directory and update Markdown files
for root, dirs, files in os.walk(base_directory):
    for file in files:
        if file.endswith('.md'):
            parent_folder_name = os.path.basename(root)
            if parent_folder_name in nav_order_data:
                nav_order = nav_order_data[parent_folder_name] + 1  # Start from 1
                file_path = os.path.join(root, file)
                update_nav_order_in_markdown(file_path, nav_order)
            else:
                print(f"Filename: {file}, {parent_folder_name}")


# Create a CSV file for files that were not modified
if files_not_modified:
    with open('failed_to_update.csv', 'w', newline='') as failed_csv:
        csv_writer = csv.writer(failed_csv)
        csv_writer.writerow(['Failed Files'])
        for file_path in files_not_modified:
            csv_writer.writerow([file_path])

    print(f"List of files that were not modified saved in 'failed_to_update.csv'.")
else:
    print(f"All {total_files_count} files were successfully updated.")
    print(f"Number of files modified: {files_modified_count}")

# Print non-integer nav_order files
if non_integer_nav_order_files:
    print("Files with non-integer nav_order values:")
    for file_path in non_integer_nav_order_files:
        print(file_path)
