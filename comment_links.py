import os

def comment_out_custom(content, target_str):
    if target_str in content:
        # Check if already commented
        if f"<!-- {target_str} -->" in content:
            return content
        if f"<!--{target_str}-->" in content:
            return content
        
        # Replace
        print(f"Commenting out: {target_str[:20]}...")
        return content.replace(target_str, f"<!-- {target_str} -->")
    return content

def process_files():
    root_dir = "c:\\Users\\Lenovo\\Documents\\GitHub\\Pareesan-Services"
    
    targets = [
        '<a href="solar-in-delhi.html" class="dropdown-item">Solar in Delhi</a>',
        '<a href="solar-in-delhi.html" class="btn btn-outline-dark mt-4">Find Your City</a>',
        '<li><a href="solar-in-delhi.html">Solar in Delhi</a></li>',
        '<a href="solar-in-delhi.html" class="nav-link">Solar in Delhi</a>' # Just in case
    ]

    for filename in os.listdir(root_dir):
        if filename.endswith(".html"):
            filepath = os.path.join(root_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                for target in targets:
                    content = comment_out_custom(content, target)
                
                if content != original_content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"Updated {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    process_files()
