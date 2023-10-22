#!/bin/bash

# Define the root directory where your Markdown files are located
root_directory="/path/to/your/root/directory"

# Function to check if a directory has subdirectories
has_subdirectories() {
  local dir="$1"
  if [ -n "$(find "$dir" -mindepth 1 -type d)" ]; then
    return 0 # Directory has subdirectories
  else
    return 1 # Directory does not have subdirectories
  fi
}

# Function to add YAML front matter to a Markdown file
add_yaml_front_matter() {
  local file="$1"
  local title=$(grep -m 1 "^# " "$file" | sed 's/# //')
  local parent_folder=$(echo "$file" | awk -F/ '{print tolower($(NF-1))}')
  local has_children

  if has_subdirectories "$(dirname "$file")"; then
    has_children="true"
  else
    has_children="false"
  fi

  # Construct the YAML front matter
  local yaml_front_matter="---
layout: default
title: \"$title\"
parent_folder: \"$parent_folder\"
has_children: $has_children
---"

  # Prepend the YAML front matter to the Markdown file
  echo -e "$yaml_front_matter\n$(cat "$file")" > "$file"
}

# Find and process Markdown files in the specified directory and its subdirectories
find "$root_directory" -type f -name "*.md" | while read -r markdown_file; do
  add_yaml_front_matter "$markdown_file"
  echo "YAML front matter added to '$markdown_file'."
done