import os

file_path = r"c:\Users\Lenovo\Documents\GitHub\Avani eco solutions\AVANI-ECO-SOLUTION\assets\css\style.css"

with open(file_path, 'rb') as f:
    content = f.read()

# Pattern to find: the corrupted comment start
# It appeared as "/ *   L o c a t i o n s" in the view_file, which likely means space-separated chars
# or just look for the known end of the valid file.
# The last valid block was:
#     .client-logo-grid {
#         grid-template-columns: repeat(2, 1fr);
#         gap: 15px;
#     }
# }
# So we look for the last '}' before the corruption.

# Let's try to decode as utf-8 and ignore errors to process string
try:
    text = content.decode('utf-8')
except:
    text = content.decode('latin-1')

# The corruption likely starts after "gap: 15px;\n    }\n}"
# Be careful with line endings.

# Easier approach: Read lines, keeping only those that don't look corrupted.
lines = text.splitlines(keepends=True)
clean_lines = []
for line in lines:
    if "/ *" in line and "L o c a t i o n s" in line:
        # Found the corrupted line. 
        # It might be attached to a valid line like "}\n/ * ..." or "} / *"
        # We need to split it.
        parts = line.split("/ *")
        clean_lines.append(parts[0] + "\n")
        break
    else:
        clean_lines.append(line)

# Reconstruct
new_content = "".join(clean_lines)

# Append the new CSS
append_css = """
/* Locations Map Full Width Update */
.locations-section .container-fluid {
    width: 100%;
    padding: 0;
    max-width: 100%;
}

.locations-grid {
    width: 100%;
    margin: 0;
    display: flex;
    justify-content: center;
}

.location-map {
    width: 100%;
    text-align: center;
}

.india-map {
    width: 100%;
    height: auto;
    max-width: 100%;
    display: block;
    margin: 0 auto;
}
"""

final_content = new_content + append_css

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(final_content)

print("Fixed style.css")
