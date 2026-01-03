import os

# List of files that need the 'projects-page' class to fix header overlap and nav visibility
TARGET_FILES = [
    'about.html',
    'careers.html',
    'partners.html',
    'reviews.html',
    'team.html',
    'clients.html',
    'load-calculator.html',
    'privacy.html', # If exists
    'terms.html'    # If exists
]

PROJECT_DIR = '/Users/avinash/Pareesan Services Pvt. Ltd./PAREESAN/'

def fix_page(filename):
    file_path = os.path.join(PROJECT_DIR, filename)
    
    if not os.path.exists(file_path):
        print(f"Skipping (Not Found): {filename}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already has the class
    if 'class="projects-page"' in content:
        print(f"Skipping (Already Fixed): {filename}")
        return

    # Replace <body> with <body class="projects-page">
    # We look for <body> strictly to avoid messing up if attributes exist (though most don't)
    if '<body>' in content:
        new_content = content.replace('<body>', '<body class="projects-page">')
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed Layout: {filename}")
    else:
        print(f"Skipping (No clean <body> tag): {filename}")

def main():
    print("Starting Internal Page Layout Fix...")
    for file in TARGET_FILES:
        fix_page(file)
    print("Done.")

if __name__ == "__main__":
    main()
