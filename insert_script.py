import os
import re

PROJECT_DIR = '/Users/avinash/Pareesan Services Pvt. Ltd./PAREESAN/'
SCRIPT_TAG = '<script src="assets/js/script.js"></script>'

def ensure_script(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if script.js is already present (simple string check)
    if 'src="assets/js/script.js"' in content or "src='assets/js/script.js'" in content:
        print(f"Skipped (Already present): {os.path.basename(file_path)}")
        return

    # If Not Present, Insert before </body>
    # We look for </body> (case insensitive)
    pattern = re.compile(r'</body>', re.IGNORECASE)
    
    if pattern.search(content):
        # Insert script tag before </body>
        new_content = pattern.sub(f'    {SCRIPT_TAG}\n</body>', content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Added script.js to: {os.path.basename(file_path)}")
    else:
        print(f"Skipped (No body tag): {os.path.basename(file_path)}")

def main():
    for root, dirs, files in os.walk(PROJECT_DIR):
        for file in files:
            if file.endswith('.html'):
                ensure_script(os.path.join(root, file))

if __name__ == "__main__":
    main()
