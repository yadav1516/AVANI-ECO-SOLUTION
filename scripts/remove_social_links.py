import os
import re

# Directory to search
root_dir = r"c:\Users\Lenovo\Documents\GitHub\Avani eco solutions\AVANI-ECO-SOLUTION"

# Regex patterns for the links to remove
# Twitter
twitter_pattern = re.compile(
    r'<a\s+href="javascript:void\(0\)"\s+aria-label="Twitter">\s*<i\s+class="fab\s+fa-twitter">\s*</i>\s*</a>',
    re.IGNORECASE | re.DOTALL
)

# YouTube
youtube_pattern = re.compile(
    r'<a\s+href="https://www\.youtube\.com/@PareesanServices"\s+aria-label="YouTube"\s+target="_blank">\s*<i\s+class="fab\s+fa-youtube">\s*</i>\s*</a>',
    re.IGNORECASE | re.DOTALL
)

def process_files():
    count = 0
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".html"):
                filepath = os.path.join(subdir, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()

                    new_content = content
                    
                    # Remove Twitter
                    new_content = twitter_pattern.sub('', new_content)
                    
                    # Remove YouTube
                    new_content = youtube_pattern.sub('', new_content)

                    if new_content != content:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Updated: {filepath}")
                        count += 1
                except Exception as e:
                    print(f"Error processing {filepath}: {e}")

    print(f"Total files updated: {count}")

if __name__ == "__main__":
    process_files()
