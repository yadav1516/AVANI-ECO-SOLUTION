import os
import re

# Configuration
target_dir = r"c:\Users\Lenovo\Documents\GitHub\Avani eco solutions\AVANI-ECO-SOLUTION"
extensions = [".html"]

# Replacement mappings
# 1. Phone Update
old_phone_display_pattern = r"\+91\s*9873886002"
new_phone_display = "+91 76686 82912, +91 92178 50708"

# 2. Email Update
old_email = "info@pareesan.com"
new_email = "info@avaniecosolution.com"

# 3. Address Update (Multi-line regex)
# Matches "Unit no 401...Haryana 121009" with flexible whitespace/newlines
old_address_pattern = r"Unit\s+no\s+401.*?,?[\s\r\n]+Erose\s+garden.*?Haryana\s+121009"
new_address = "591, TR 34, Brij Vihar, Lucknow, 226002"

# 4. Tel Link Update (Updating to primary number)
old_tel_link_pattern = r"tel:\+?91[\s-]?9873886002"
new_tel_link = "tel:+917668682912"

def update_files():
    count = 0
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # Replace Phone Display
                content = re.sub(old_phone_display_pattern, new_phone_display, content)
                
                # Replace Tel Link
                content = re.sub(old_tel_link_pattern, new_tel_link, content)
                
                # Replace Email
                content = content.replace(old_email, new_email)
                
                # Replace Address (using re.DOTALL to match across newlines)
                content = re.sub(old_address_pattern, new_address, content, flags=re.DOTALL | re.IGNORECASE)

                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"Updated: {file}")
                    count += 1
    
    print(f"Total files updated: {count}")

if __name__ == "__main__":
    update_files()
