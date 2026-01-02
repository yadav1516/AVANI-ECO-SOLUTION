
import os
import re

def get_seo_content(filename):
    basename = os.path.splitext(filename)[0]
    # Convert 'rooftop-solar' to 'Rooftop Solar'
    title_text = basename.replace('-', ' ').replace('_', ' ').title()
    
    # Custom tweaks for specific files if needed, but generic is fine for now
    if basename == 'index':
        title = "Pareesan Services Pvt Ltd - Premier Solar EPC & Technology Solutions"
        desc = "Pareesan Services: India's leading Solar EPC company. Industrial, Commercial, and Utility-scale solar solutions with advanced technology and safety standards."
    else:
        title = f"{title_text} - Pareesan Services Pvt Ltd"
        desc = f"Learn more about {title_text} at Pareesan Services Pvt Ltd. We provide top-tier Solar EPC solutions, ensuring quality, safety, and sustainability across India."

    return title, desc

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    filename = os.path.basename(filepath)
    title, desc = get_seo_content(filename)

    # 1. Update or Add Viewport
    if '<meta name="viewport"' not in content:
        # Add after <head>
        head_match = re.search(r'<head>', content, re.IGNORECASE)
        if head_match:
            content = content[:head_match.end()] + '\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">' + content[head_match.end():]
    
    # 2. Update or Add Title
    # Regex to find <title>...</title>
    title_pattern = re.compile(r'<title>(.*?)</title>', re.DOTALL | re.IGNORECASE)
    if title_pattern.search(content):
        # Replace existing
        content = title_pattern.sub(f'<title>{title}</title>', content)
    else:
        # Add after <head> (or viewport if we just added it, regex search refinds)
        head_match = re.search(r'<head>', content, re.IGNORECASE)
        if head_match:
             content = content[:head_match.end()] + f'\n    <title>{title}</title>' + content[head_match.end():]

    # 3. Update or Add Description
    desc_pattern = re.compile(r'<meta\s+name=["\']description["\']\s+content=["\'].*?["\']\s*/?>', re.DOTALL | re.IGNORECASE)
    new_desc_tag = f'<meta name="description" content="{desc}">'
    
    if desc_pattern.search(content):
        content = desc_pattern.sub(new_desc_tag, content)
    else:
         # Add after title
        title_match = title_pattern.search(content)
        if title_match:
             content = content[:title_match.end()] + f'\n    {new_desc_tag}' + content[title_match.end():]
        else:
             # Fallback to after head
            head_match = re.search(r'<head>', content, re.IGNORECASE)
            if head_match:
                 content = content[:head_match.end()] + f'\n    {new_desc_tag}' + content[head_match.end():]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {filename}")

def main():
    root_dir = "."
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith('.html'):
                filepath = os.path.join(dirpath, filename)
                try:
                    update_file(filepath)
                except Exception as e:
                    print(f"Error updating {filepath}: {e}")

if __name__ == "__main__":
    main()
