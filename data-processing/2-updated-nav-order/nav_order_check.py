import os
import yaml
import csv

# Path to the directory containing your Markdown files
base_directory = './'

# Initialize counters for counting files, printing nav_order, and non-integer nav_order values
file_count = 0
non_integer_count = 0

# Initialize a list to store file path and nav_order pairs with non-integer nav_order values
non_integer_data = []

# Function to print nav_order from YAML front matter and count non-integer values
def print_nav_order_from_markdown(file_path):
    global file_count, non_integer_count, non_integer_data  # Use global variables
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

            # Check if YAML front matter is a dictionary and 'nav_order' key exists
            if isinstance(yaml_front_matter, dict) and 'nav_order' in yaml_front_matter:
                nav_order = yaml_front_matter['nav_order']
                if isinstance(nav_order, int):
                    print(f"Nav Order for {file_path}: {nav_order}")
                else:
                    print(f"Non-integer Nav Order for {file_path}: {nav_order}")
                    non_integer_count += 1
                    non_integer_data.append((file_path, nav_order))
            else:
                print(f"No 'nav_order' found in YAML front matter of {file_path}.")
        else:
            print(f"No YAML front matter found in {file_path}.")

        file_count += 1  # Increment the counter for files processed

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# Walk through the directory and print nav_order from Markdown files
for root, dirs, files in os.walk(base_directory):
    for file in files:
        if file.endswith('.md'):
            file_path = os.path.join(root, file)
            print_nav_order_from_markdown(file_path)

print(f"Total files processed: {file_count}")
print(f"Total non-integer nav_order values found: {non_integer_count}")

# Save file path and nav_order pairs with non-integer values to a CSV file
if non_integer_data:
    with open('non_integer_nav_order_data.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['File Path', 'Nav Order'])
        csv_writer.writerows(non_integer_data)

print(f"File paths and nav_order pairs with non-integer values saved to 'non_integer_nav_order_data.csv'.")
