import os
import re
import yaml

def get_title_from_index_md(folder_path):
    """Extract the title from the index.md file in the given folder."""
    index_md_path = os.path.join(folder_path, 'index.md')
    if os.path.exists(index_md_path):
        with open(index_md_path, 'r') as file:
            content = file.read()
            front_matter = re.search(r'^---\s+(.*?)\s+---', content, re.DOTALL)
            if front_matter:
                data = yaml.safe_load(front_matter.group(1))
                return data.get('title')
    return None

def update_markdown_file(file_path, parent_title):
    """Update the YAML front matter of a Markdown file by adding a parent field."""
    with open(file_path, 'r') as file:
        content = file.read()

    front_matter_match = re.search(r'^---\s+(.*?)\s+---', content, re.DOTALL)
    if front_matter_match:
        front_matter = yaml.safe_load(front_matter_match.group(1))
        front_matter['parent'] = parent_title
        updated_front_matter = yaml.safe_dump(front_matter)
        updated_content = re.sub(r'^---\s+.*?\s+---', f'---\n{updated_front_matter}---', content, flags=re.DOTALL)

        with open(file_path, 'w') as file:
            file.write(updated_content)

def process_folder(folder_path):
    """Process all Markdown files in a folder, updating their YAML front matter with the parent title."""
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            process_folder(item_path)
        elif item.endswith('.md'):
            parent_title = None
            if item != 'index.md':
                # For non-index.md files, get title from index.md in the same directory
                parent_title = get_title_from_index_md(folder_path)
            else:
                # For index.md files, get title from index.md in the parent directory
                parent_folder_path = os.path.abspath(os.path.join(folder_path, os.pardir))
                parent_title = get_title_from_index_md(parent_folder_path)
            
            if parent_title:
                update_markdown_file(item_path, parent_title)

# Start processing from the current directory
root_directory = './'  # Current directory
process_folder(root_directory)
