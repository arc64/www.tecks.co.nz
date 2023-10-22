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

# Function to update nav_order in YAML front matter
def update_nav_order_in_markdown(file_path, nav_order):
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
            existing_front_matter = "".join(lines[start_idx+1:end_idx])

            # Attempt to parse the YAML front matter
            try:
                yaml_front_matter = yaml.safe_load(existing_front_matter)
            except yaml.YAMLError as e:
                print(f"Error parsing YAML in {file_path}: {e}")
                return

            # Check if YAML front matter is a dictionary
            if isinstance(yaml_front_matter, dict):
                if 'nav_order' in yaml_front_matter:
                    yaml_front_matter['nav_order'] = nav_order

                # Convert the updated YAML front matter back to a string with proper formatting
                updated_yaml_lines = yaml.dump(yaml_front_matter, default_flow_style=False).splitlines()
                updated_yaml_front_matter =  '\n'.join(updated_yaml_lines) 

                # Replace the original YAML front matter with the updated content
                lines[start_idx+1:end_idx] = [line + '\n' for line in updated_yaml_front_matter.splitlines()]

                # Write the updated content back to the file
                with open(file_path, 'w') as markdown_file:
                    markdown_file.writelines(lines)

            else:
                print(f"YAML front matter in {file_path} is not a dictionary.")
        else:
            print(f"No YAML front matter found in {file_path}.")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# Walk through the directory and update Markdown files
for root, dirs, files in os.walk(base_directory):
    for file in files:
        if file.endswith('.md'):
            parent_folder_name = os.path.basename(root)
            if parent_folder_name in nav_order_data:
                nav_order = nav_order_data[parent_folder_name]
                file_path = os.path.join(root, file)
                update_nav_order_in_markdown(file_path, nav_order)
                print(f"Updated {file_path} with nav_order {nav_order}")
