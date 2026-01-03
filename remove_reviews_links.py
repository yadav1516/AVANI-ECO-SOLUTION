import os

PROJECT_DIR = '/Users/avinash/Pareesan Services Pvt. Ltd./PAREESAN/'

def remove_links_in_file(filename):
    if not filename.endswith('.html'):
        return

    file_path = os.path.join(PROJECT_DIR, filename)
    if not os.path.exists(file_path):
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    removed_count = 0
    
    for line in lines:
        if 'reviews.html' in line:
            # We assume it's a link line like <li><a href="reviews.html">...
            # We just skip it to remove it.
            removed_count += 1
            print(f"[{filename}] Removing line: {line.strip()}")
            continue
        new_lines.append(line)

    if removed_count > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"Processed {filename}: Removed {removed_count} links.")

def main():
    print("Starting Removal of reviews.html links...")
    files = [f for f in os.listdir(PROJECT_DIR) if f.endswith('.html')]
    for file in files:
        remove_links_in_file(file)
    print("Done.")

if __name__ == "__main__":
    main()
