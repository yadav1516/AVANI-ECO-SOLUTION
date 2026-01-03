import os

SERVICE_FILES = [
    'solar-epc.html',
    'installation.html',
    'om-services.html'
]

PROJECT_DIR = '/Users/avinash/Pareesan Services Pvt. Ltd./PAREESAN/'

def fix_service_page(filename):
    file_path = os.path.join(PROJECT_DIR, filename)
    if not os.path.exists(file_path):
        print(f"File not found: {filename}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add projects-page class
    if 'class="projects-page"' not in content:
        if '<body class=' in content:
             content = content.replace('<body class="', '<body class="projects-page ')
        else:
             content = content.replace('<body>', '<body class="projects-page">')

    # 2. Ensure Scripts
    if '<script src="assets/js/script.js"></script>' not in content:
        content = content.replace('</body>', '<script src="assets/js/script.js"></script>\n</body>')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed Structure: {filename}")

def main():
    print("Starting Service Page Fix...")
    for file in SERVICE_FILES:
        fix_service_page(file)
    print("Done.")

if __name__ == "__main__":
    main()
