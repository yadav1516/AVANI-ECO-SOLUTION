import os
import re

PROJECT_DIR = '/Users/avinash/Pareesan Services Pvt. Ltd./PAREESAN/'

def cleanup_debris(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Target the specific debris block found in projects.html, blog.html etc.
    # It usually looks like a sequence of closing divs and the p tag
    # Whitespace might vary
    
    # Pattern 1: The exact block seen in previous files
    #             </div>
    #             <p class="loader-text">Energizing the Future...</p>
    #         </div>
    #     </div>
    
    # We will look for the text "Energizing the Future..." and aggressively clean up surrounding divs if they match the broken structure.
    # But to be safe and simple, we simply remove lines that contain "loader-text" or "Energizing the Future..." 
    # and the specific closing div sequence if it forms that block.
    
    # Regex to match the debris block loosely
    pattern = re.compile(r'\s*</div>\s*<p class="loader-text">Energizing the Future\.\.\.</p>\s*</div>\s*</div>', re.DOTALL)
    
    # Also match just the P tag if divs were already removed?
    pattern_text = re.compile(r'<p class="loader-text">Energizing the Future\.\.\.</p>')
    
    new_content = content
    
    if pattern.search(new_content):
        new_content = pattern.sub('', new_content)
    
    if pattern_text.search(new_content):
        new_content = pattern_text.sub('', new_content)
        
    # Also clean up any loose "</div>" that might have been left if the pattern didn't match perfectly, 
    # but that is risky. Let's stick to the text identifier which is unique.
    
    # Check for "preloader" class just in case
    pattern_loader = re.compile(r'<div class="preloader">.*?</div>', re.DOTALL | re.IGNORECASE)
    if pattern_loader.search(new_content):
        new_content = pattern_loader.sub('', new_content)

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Cleaned debris in: {os.path.basename(file_path)}")
    else:
        print(f"No debris found in: {os.path.basename(file_path)}")

def main():
    for root, dirs, files in os.walk(PROJECT_DIR):
        for file in files:
            if file.endswith('.html'):
                cleanup_debris(os.path.join(root, file))

if __name__ == "__main__":
    main()
