#!/bin/bash

# Input CSV file containing the list of URLs
input_csv="folders-and-leafs.csv"

# Output CSV file with added columns
output_csv="urls_with_depth_order_nav.csv"

# Initialize the output CSV file with headers
echo "URL,Depth,ParentFolderName,nav_order,FileName,FileNameNoSpaces" > "$output_csv"

# Function to calculate the depth of a URL
calculate_depth() {
  local url="$1"
  echo "$url" | awk -F/ '{print NF-1}'
}

# Function to calculate the order within the parent folder
calculate_order_within_parent() {
  local url="$1"
  local parent_folder=$(dirname "$url")
  echo "$parent_folder" | awk -F/ '{print $NF}'
}

# Function to remove non-printable characters from a string
remove_non_printable_characters() {
  local input="$1"
  # Use tr to remove non-printable characters
  echo "$input" | tr -dc '[:print:]\n'
}

# Function to capitalize the first letter of a string using awk
capitalize_first_letter() {
  local input="$1"
  echo "$input" | awk '{print toupper(substr($1,1,1)) tolower(substr($1,2))}'
}

# Function to add depth, parent folder name, nav_order, FileName, and FileNameNoSpaces to the output CSV
add_columns() {
  local input_file="$1"
  local prev_order=""

  while IFS=, read -r url; do
    # Remove non-printable characters from the URL
    url=$(remove_non_printable_characters "$url")
    local depth=$(calculate_depth "$url")
    local parent_folder=$(calculate_order_within_parent "$url")
    local file_name=$(basename "$url")
    local file_name_no_hyphens=$(echo "$file_name" | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2));}1')
    local file_name_no_spaces=$(echo "$file_name_no_hyphens" | sed 's/ //g' | awk '{for(i=1;i<=NF;i++) $i=tolower($i);}1')
    local file_name_no_spaces_capitalized=$(capitalize_first_letter "$file_name_no_spaces")

    if [ "$parent_folder" != "$prev_order" ]; then
      nav_order=0
    else
      ((nav_order++))
    fi

    # Check if nav_order is 0 and remove the column if true
    if [ "$nav_order" -eq 0 ]; then
      nav_order=""
    fi

    # Check if nav_order is not an integer and print it to the console
    if ! [[ "$nav_order" =~ ^[0-9]+$ ]]; then
      echo "nav_order for '$url' is not an integer: $nav_order"
    fi

    # Append the line to the output CSV and include a newline character
    echo -n "$url,$depth,$parent_folder,$nav_order,$file_name_no_hyphens,$file_name_no_spaces_capitalized" >> "$output_csv"
    echo >> "$output_csv"  # Add a newline character to separate entries in the output CSV
    prev_order="$parent_folder"
  done < <(sed '/^[[:space:]]*$/d' "$input_file")
}

# Call the function to add columns to the output CSV
add_columns "$input_csv"

echo "Columns added to '$output_csv'."
