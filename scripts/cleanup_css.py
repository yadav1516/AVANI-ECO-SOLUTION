import os

file_path = r"c:\Users\Lenovo\Documents\GitHub\Avani eco solutions\AVANI-ECO-SOLUTION\assets\css\style.css"

# Read the content
# We suspect mixed encoding or binary garbage. Let's read as binary first.
with open(file_path, 'rb') as f:
    content = f.read()

# Try to decode as much as possible.
try:
    text = content.decode('utf-8')
except UnicodeDecodeError:
    # If utf-8 fails, try latin-1 which maps bytes 1-1 usually
    text = content.decode('latin-1')

# We know the file was good up until the "@media (max-width: 768px)" block for clients.
# Let's look for ".client-logo-grid" and the closing brace of that media query.
marker = ".client-logo-grid"
idx = text.rfind(marker)

if idx == -1:
    print("Could not find marker. modifying blindly?")
    # Fallback: look for ".footer" block start which is usually near end, but we added stuff after footer?
    # Actually the style file structure had footer at the end? 
    # Let's look for the last known good structure we saw in Step 184/259.
    # It seems the file ends with specific media queries.
    pass

# Let's find the closing brace of the media query containing .client-logo-grid
# It looks like:
#     .client-logo-grid {
#         grid-template-columns: repeat(2, 1fr);
#         gap: 15px;
#     }
# }
# So we look for the first "}" after .client-logo-grid, then the next "}" (closing the media query).

idx_brace1 = text.find("}", idx)
idx_brace2 = text.find("}", idx_brace1 + 1)

if idx_brace2 != -1:
    # Good content ends at idx_brace2 + 1
    clean_content = text[:idx_brace2+1]
else:
    # If we can't find it, we might be in trouble. Use a safe fallback?
    # Let's try to just find the marker and cut before the corruption we saw which started with "/ * L o c..."
    # If we can't find clear braces, maybe search for the corruption pattern?
    corrupt_idx = text.find("/ *   L o c a t i o n s")
    if corrupt_idx != -1:
         clean_content = text[:corrupt_idx]
    else:
         # If we can't find corruption pattern either, maybe just truncate after the marker block assuming standard length?
         # Or just use the original content if it was readable.
         clean_content = text

# Now Clean the content of any trailing null bytes or weird spacing if present at the end
clean_content = clean_content.rstrip()

# New CSS to Append (Map Fix + Process Fix)
new_css = """

/* =========================================
   FIXES APPENDED BY ASSISTANT 
   ========================================= */

/* 1. Map Layout Fix (Centered, constrained) */
.locations-grid {
    display: flex;
    justify-content: center;
    width: 100%;
    margin-top: 30px;
}

.location-map {
    width: 100%;
    text-align: center;
    max-width: 1200px;
    margin: 0 auto;
}

.india-map {
    width: auto;
    height: auto;
    max-width: 100%;
    display: block;
    margin: 0 auto;
}

/* 2. Process Grid Fix (6 items in one line) */
@media (min-width: 992px) {
    .process-section .process-grid {
        display: grid !important;
        grid-template-columns: repeat(6, 1fr) !important;
        gap: 15px !important;
        width: 100% !important;
        max-width: 100% !important;
    }
    
    .process-section .process-card {
        margin: 0 !important;
        width: 100% !important;
    }
    
    /* Adjust internal elements for compact fit */
    .process-section .process-img {
        height: 120px;
    }
    
    .process-section h3 {
        font-size: 1rem;
    }
}
"""

final_content = clean_content + new_css

# Write back as utf-8
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(final_content)

print("Cleaned and updated style.css")
