import os

PROJECT_DIR = '/Users/avinash/Pareesan Services Pvt. Ltd./PAREESAN/'
EXCLUDE_FILES = ['index.html']

def fix_html_file(filename):
    if filename in EXCLUDE_FILES:
        return

    file_path = os.path.join(PROJECT_DIR, filename)
    if not os.path.exists(file_path):
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    modified = False

    # 1. Add projects-page class (Fixes Header Overlap & Nav Color)
    # We look for <body ...> that does NOT already have projects-page
    if 'class="projects-page"' not in content:
        if '<body class=' in content:
            # Append to existing class
            content = content.replace('<body class="', '<body class="projects-page ')
            modified = True
        elif '<body>' in content:
            # Add class attribute
            content = content.replace('<body>', '<body class="projects-page">')
            modified = True

    # 2. Ensure Main Script is present (Fixes Mobile Menu)
    if '<script src="assets/js/script.js"></script>' not in content:
        if '</body>' in content:
            content = content.replace('</body>', '<script src="assets/js/script.js"></script>\n</body>')
            modified = True

    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed: {filename}")
    else:
        print(f"Skipped (Already Good): {filename}")

def main():
    print("Starting Global HTML Fix...")
    files = [f for f in os.listdir(PROJECT_DIR) if f.endswith('.html')]
    for file in files:
        fix_html_file(file)
    print("Global Fix Complete.")

if __name__ == "__main__":
    main()
