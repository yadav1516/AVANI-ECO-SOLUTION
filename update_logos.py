
import os
import re

directory = '/Users/avinash/Pareesan Services Pvt. Ltd./PAREESAN'
logo_primary = 'images/logo_primary.png'
logo_transparent = 'images/logo_transparent.png'

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 1. Update Footer Logo (Always Transparent)
    # Pattern: <img ... class="footer-logo">
    # We replace the src attribute.
    # Regex designed to find img tag with class="footer-logo" and capture text before and after src
    content = re.sub(
        r'(<img[^>]*class=["\']footer-logo["\'][^>]*src=["\'])([^"\']+)(["\'])',
        r'\1' + logo_transparent + r'\3',
        content, flags=re.IGNORECASE
    )
    # Also handle if src comes before class
    content = re.sub(
        r'(<img[^>]*src=["\'])([^"\']+)(["\'][^>]*class=["\']footer-logo["\'])',
        r'\1' + logo_transparent + r'\3',
        content, flags=re.IGNORECASE
    )

    # 2. Update Mobile Logo (User requested Transparent Everywhere)
    content = re.sub(
        r'(<img[^>]*class=["\']mobile-logo["\'][^>]*src=["\'])([^"\']+)(["\'])',
        r'\1' + logo_transparent + r'\3',
        content, flags=re.IGNORECASE
    )
    content = re.sub(
        r'(<img[^>]*src=["\'])([^"\']+)(["\'][^>]*class=["\']mobile-logo["\'])',
        r'\1' + logo_transparent + r'\3',
        content, flags=re.IGNORECASE
    )

    # 3. Update Favicon (User requested Transparent Everywhere)
    content = re.sub(
        r'(<link[^>]*rel=["\']icon["\'][^>]*href=["\'])([^"\']+)(["\'])',
        r'\1' + logo_transparent + r'\3',
        content, flags=re.IGNORECASE
    )

    # 4. Update Header Logo
    # Logic: User requested SPECIAL Wide Logo for Header/Nav ONLY.
    
    logo_nav = 'images/logo_nav.png'
    target_logo = logo_nav
    
    # Replace logo-img
    content = re.sub(
        r'(<img[^>]*class=["\']logo-img["\'][^>]*src=["\'])([^"\']+)(["\'])',
        r'\1' + target_logo + r'\3',
        content, flags=re.IGNORECASE
    )
    content = re.sub(
        r'(<img[^>]*src=["\'])([^"\']+)(["\'][^>]*class=["\']logo-img["\'])',
        r'\1' + target_logo + r'\3',
        content, flags=re.IGNORECASE
    )

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {os.path.basename(filepath)}")
    else:
        print(f"No changes for {os.path.basename(filepath)}")

for filename in os.listdir(directory):
    if filename.endswith('.html'):
        update_file(os.path.join(directory, filename))
