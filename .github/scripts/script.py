import os
import yaml
import json
import re

repository_path = '.'  # root of your repository

def is_md_file(filename):
    return filename.endswith('.md')

def extract_frontmatter(md_content):
    pattern = r'^---\s*\n(.*?)\n---\s*\n'
    matches = re.search(pattern, md_content, re.DOTALL | re.MULTILINE)
    return matches.group(1) if matches else None

all_data = []  # list to store all frontmatter data

print("Script started!")

# Ensure output directory exists
os.makedirs('output', exist_ok=True)

# Walk through the repository
for subdir, _, files in os.walk(repository_path):
    for file in files:
        if is_md_file(file):
            file_path = os.path.join(subdir, file)
            print(f"Found MD file: {file_path}")
            with open(file_path, 'r') as f:
                content = f.read()
                frontmatter = extract_frontmatter(content)
                if frontmatter:
                    data = yaml.safe_load(frontmatter)
                    
                    # Check if 'ignore' is present and set to true, or if it's absent, then skip processing
                    if data.get('ignore', True):  
                        print(f"Skipped {file_path} because it is marked for ignoring or doesn't have the 'ignore' flag.")
                        continue
                    
                    # Remove the 'ignore' key from data
                    data.pop('ignore', None)

                    all_data.append(data)
                    output_path = os.path.splitext(file_path)[0] + '-frontmatter.json'
                    with open(output_path, 'w') as f:
                        json.dump(data, f, indent=4)
                    print(f"Written data to {output_path}")

                else:
                    print(f"No frontmatter in: {file_path}")

print(f"Writing to output/output.json with {len(all_data)} entries...")
# Save all data to output/output.json
absolute_output_path = os.path.join(repository_path, 'output', 'output.json')
with open(absolute_output_path, 'w') as outfile:
    json.dump(all_data, outfile, indent=4)
    print("Written to output/output.json")
