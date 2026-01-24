import os
import re

def rebrand_files():
    # Define replacements
    text_replacements = [
        ("Pareesan Services Pvt. Ltd.", "Avani Eco Solutions Pvt. Ltd."),
        ("Pareesan Services", "Avani Eco Solutions Pvt. Ltd."),
        ("Pareesan", "Avani Eco Solutions Pvt. Ltd.")
    ]
    
    logo_replacements = [
        ("assets/img/general/logo_nav.png", "assets/img/general/avani_logo.png"),
        ("assets/img/general/logo_transparent.png", "assets/img/general/avani_logo.png")
    ]

    # Iterate over all files in the current directory
    for filename in os.listdir('.'):
        if filename.endswith(".html"):
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
            
            original_content = content
            
            # Apply text replacements
            for old, new in text_replacements:
                content = content.replace(old, new)
            
            # Apply logo replacements
            for old, new in logo_replacements:
                content = content.replace(old, new)
            
            if content != original_content:
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f"Updated {filename}")

if __name__ == "__main__":
    rebrand_files()
