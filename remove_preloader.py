import os
import re

PROJECT_DIR = '/Users/avinash/Pareesan Services Pvt. Ltd./PAREESAN/'

def remove_preloader(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to match the preloader div and optional surrounding comments
    # Matches:
    # <!-- Preloader --> (Optional)
    # <div class="preloader"> ... </div>
    # Using non-greedy match across lines
    pattern = re.compile(r'<!--\s*Preloader\s*-->\s*<div class="preloader">.*?</div>', re.DOTALL | re.IGNORECASE)
    
    # Also match valid HTML comment based preloader if it was commented out
    pattern_commented = re.compile(r'<!--\s*Preloader.*?<div class="preloader">.*?</div>\s*-->', re.DOTALL | re.IGNORECASE)

    # Simple preloader div match if comments are missing
    pattern_simple = re.compile(r'<div class="preloader">.*?</div>', re.DOTALL | re.IGNORECASE)

    new_content = content
    
    # Try removing commented out first (if user did some work)
    if pattern_commented.search(new_content):
        new_content = pattern_commented.sub('', new_content)
    
    # Then remove standard block
    if pattern.search(new_content):
        new_content = pattern.sub('', new_content)
        
    # Then clean up any remaining simple divs
    if pattern_simple.search(new_content):
        new_content = pattern_simple.sub('', new_content)
        
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Removed preloader from: {os.path.basename(file_path)}")
    else:
        print(f"No preloader found in: {os.path.basename(file_path)}")

def main():
    for root, dirs, files in os.walk(PROJECT_DIR):
        for file in files:
            if file.endswith('.html'):
                remove_preloader(os.path.join(root, file))

if __name__ == "__main__":
    main()
