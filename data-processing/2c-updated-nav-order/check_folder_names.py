import os
import csv

# Path to the CSV file containing non-integer nav_order data
csv_file = 'non_integer_nav_order_data.csv'

# Initialize a list to store non-integer nav_order data along with associated file paths
non_integer_nav_order_data = []

# Read the CSV file and store the data in a list of dictionaries
with open(csv_file, 'r') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for i, row in enumerate(csv_reader, start=1):
        entry_name = row.get('File Path', '').strip()  # Use 'File Path' as the column name
        nav_order_value = row.get('nav_order', '').strip()

        # Add the entry to the list if nav_order is not an integer
        if not nav_order_value.isdigit():
            non_integer_nav_order_data.append({'File Path': entry_name, 'nav_order': nav_order_value})

        # Debugging: Print which lines have been processed
        print(f"Processed line {i}: File Path: {entry_name}, nav_order: {nav_order_value}")

# Debugging: Print the non-integer nav_order data and associated file paths
for entry in non_integer_nav_order_data:
    print(f"File Path: {entry['File Path']}, nav_order: {entry['nav_order']}")
