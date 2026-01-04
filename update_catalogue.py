import os

def comment_out_catalogue(directory):
    desktop_target = '<li><a href="catalogue.html" class="nav-link">Catalogue</a></li>'
    desktop_replacement = '<!-- <li><a href="catalogue.html" class="nav-link">Catalogue</a></li> -->'
    
    mobile_target = '<li><a href="catalogue.html">Catalogue</a></li>'
    mobile_replacement = '<!-- <li><a href="catalogue.html">Catalogue</a></li> -->'
    
    modified_files = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    new_content = content
                    if desktop_target in new_content:
                        new_content = new_content.replace(desktop_target, desktop_replacement)
                    
                    if mobile_target in new_content:
                        new_content = new_content.replace(mobile_target, mobile_replacement)
                        
                    if new_content != content:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        modified_files.append(file)
                        print(f"Modified: {file}")
                        
                except Exception as e:
                    print(f"Error processing {file}: {e}")

    print(f"Total files modified: {len(modified_files)}")

if __name__ == "__main__":
    current_directory = os.getcwd()
    print(f"Scanning directory: {current_directory}")
    comment_out_catalogue(current_directory)
