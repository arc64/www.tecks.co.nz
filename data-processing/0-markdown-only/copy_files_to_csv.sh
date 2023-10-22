#!/bin/bash

# Define the root directory where your files are located
root_directory="./"

# Define the output CSV file
output_csv="output.csv"

# Initialize the CSV file with headers
echo "File Path,Content" > "$output_csv"

# Use the 'find' command to locate files within the root directory and its subdirectories
find "$root_directory" -type f -name "*.md" -print | while read -r file_path; do
  # Use 'cat' to read the file content
    content=$(cat "$file_path")
      
        # Escape double quotes within the content
          content="${content//\"/\\\"}"
          
            # Append the file path and content to the CSV file
              echo "\"$file_path\",\"$content\"" >> "$output_csv"
              done
              
              echo "CSV file '$output_csv' created."
