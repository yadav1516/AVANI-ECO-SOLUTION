import os

def update_navbar(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Target entry point in the navbar
        target_string = '                        <a href="om-services.html" class="dropdown-item">O&M Services</a>'
        
        # New items to add
        new_items = '\n                        <a href="pv-modules.html" class="dropdown-item">PV Modules</a>\n                        <a href="inverters.html" class="dropdown-item">Inverters</a>'
        
        # Check if already updated
        if '<a href="pv-modules.html" class="dropdown-item">PV Modules</a>' in content:
            print(f"Skipping {filepath}: Already updated")
            return

        if target_string in content:
            new_content = content.replace(target_string, target_string + new_items)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {filepath}")
        else:
            print(f"Warning: Target string not found in {filepath}")

    except Exception as e:
        print(f"Error processing {filepath}: {e}")

# Get all html files
files = [f for f in os.listdir('.') if f.endswith('.html')]

for file in files:
    update_navbar(file)
