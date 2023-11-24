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

def format_title(title):
    """Format the title for YAML, including escaping single quotes."""
    if title == "Welcome to Teacher Education's Core Knowledge and Skills.":
        return "'Welcome to Teacher Education''s Core Knowledge and Skills.'"
    return title

def update_markdown_file(file_path, hierarchy_titles):
    """Update the YAML front matter of a Markdown file by adding hierarchy fields."""
    with open(file_path, 'r') as file:
        content = file.read()

    front_matter_match = re.search(r'^---\s+(.*?)\s+---', content, re.DOTALL)
    if front_matter_match:
        front_matter = yaml.safe_load(front_matter_match.group(1))
        for depth, title in hierarchy_titles.items():
            front_matter[depth] = format_title(title)
        updated_front_matter = yaml.safe_dump(front_matter)
        updated_content = re.sub(r'^---\s+.*?\s+---', f'---\n{updated_front_matter}---', content, flags=re.DOTALL)

        with open(file_path, 'w') as file:
            file.write(updated_content)

def build_hierarchy_titles(folder_path, depth, is_index_md):
    """Build a dictionary of titles for each level in the hierarchy."""
    titles = {}
    current_folder = folder_path
    hierarchy_levels = ['parent', 'grand_parent', 'great_grand_parent', 
                        'great_great_grand_parent', 'great_great_great_grand_parent',
                        'great_great_great_great_grand_parent']

    # For non-index.md files, set the immediate parent to the title of index.md in the same directory
    if not is_index_md:
        immediate_parent_title = get_title_from_index_md(current_folder)
        if immediate_parent_title:
            titles['parent'] = immediate_parent_title

    # Start building hierarchy from the current or parent folder depending on the file type
    start_depth = 0 if is_index_md else 1

    for i in range(start_depth, depth):
        parent_folder = os.path.abspath(os.path.join(current_folder, os.pardir))
        title = get_title_from_index_md(parent_folder)
        if title:
            level = hierarchy_levels[min(i, len(hierarchy_levels) - 1)]
            if level not in titles:  # Prevent overwriting existing titles
                titles[level] = title
        current_folder = parent_folder

    # Assign the top-most level title
    top_most_title = "Welcome to Teacher Education's Core Knowledge and Skills."
    if depth >= len(hierarchy_levels):
        titles[hierarchy_levels[-1]] = top_most_title
    else:
        level = hierarchy_levels[depth]
        titles[level] = top_most_title

    return titles

def process_folder(folder_path, depth=0, file_count=0):
    """Process all Markdown files in a folder, updating their YAML front matter with hierarchy titles."""
    files_in_current_folder = 0

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            file_count = process_folder(item_path, depth + 1, file_count)
        elif item.endswith('.md'):
            files_in_current_folder += 1
            file_count += 1
            is_index_md = item == 'index.md'
            hierarchy_titles = build_hierarchy_titles(folder_path, depth, is_index_md)
            update_markdown_file(item_path, hierarchy_titles)

    return file_count

# Start processing from the current directory
root_directory = './'  # Current directory
total_files = process_folder(root_directory)
print(f"Total Markdown files processed: {total_files}")
