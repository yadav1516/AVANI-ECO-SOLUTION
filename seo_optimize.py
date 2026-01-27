
import os
import re
from datetime import date

ROOT_DIR = r"c:\Users\Lenovo\Documents\GitHub\Avani eco solutions\AVANI-ECO-SOLUTION"
DOMAIN = "https://avaniecosolution.com"  # Assuming this based on email, can be changed.

def get_page_title(filename):
    name = filename.replace(".html", "").replace("-", " ").title()
    if name == "Index":
        return "Avani Eco Solutions Pvt. Ltd. | Leading Solar EPC Solutions Provider"
    return f"{name} - Avani Eco Solutions Pvt. Ltd."

def get_meta_description(filename):
    name = filename.replace(".html", "").replace("-", " ").title()
    if name == "Index":
        return "Avani Eco Solutions Pvt. Ltd. offers end-to-end Solar EPC solutions for residential, commercial, and industrial clients. Switch to solar today and save."
    elif name == "Residential":
        return "Switch to zero electricity bills with Avani Eco Solutions. Hassle-free residential solar installation with government subsidy and easy finance."
    else:
        return f"Learn about {name} at Avani Eco Solutions Pvt. Ltd. We provide top-tier solar services including EPC, Installation, and O&M for a sustainable future."

def process_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        original_content = content
        
        # 1. Fix "Pvt. Ltd. Pvt Ltd" typo
        content = re.sub(r"Pvt\.? Ltd\.? Pvt\.? Ltd", "Pvt. Ltd.", content, flags=re.IGNORECASE)
        
        # 2. Update Title
        filename = os.path.basename(filepath)
        new_title = get_page_title(filename)
        # Regex to find <title>...</title>
        title_pattern = re.compile(r"<title>(.*?)</title>", re.DOTALL | re.IGNORECASE)
        if title_pattern.search(content):
            content = title_pattern.sub(f"<title>{new_title}</title>", content)
        
        # 3. Update Meta Description
        new_desc = get_meta_description(filename)
        desc_pattern = re.compile(r'<meta name="description" content="(.*?)">', re.DOTALL | re.IGNORECASE)
        if desc_pattern.search(content):
            content = desc_pattern.sub(f'<meta name="description" content="{new_desc}">', content)
        
        # 4. Update Meta Keywords (Generic addition)
        keywords = "solar energy, solar epc, solar installation, avani eco solutions, renewable energy, solar power"
        kw_pattern = re.compile(r'<meta name="keywords" content="(.*?)">', re.DOTALL | re.IGNORECASE)
        if kw_pattern.search(content):
            pass # Keep specific keywords if they exist, or valid existing ones
        else:
            # Add keywords if missing (inside head)
            head_end = content.find("</head>")
            if head_end != -1:
                content = content[:head_end] + f'    <meta name="keywords" content="{keywords}">\n' + content[head_end:]

        if content != original_content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Updated: {filename}")
        else:
            print(f"No changes: {filename}")
            
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def generate_sitemap():
    print("Generating Sitemap...")
    files = [f for f in os.listdir(ROOT_DIR) if f.endswith(".html")]
    sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    today = date.today().isoformat()
    
    for f in files:
        url = f"{DOMAIN}/{f}"
        if f == "index.html":
            url = f"{DOMAIN}/"
            priority = "1.00"
        else:
            priority = "0.80"
            
        sitemap_content += "   <url>\n"
        sitemap_content += f"      <loc>{url}</loc>\n"
        sitemap_content += f"      <lastmod>{today}</lastmod>\n"
        sitemap_content += f"      <priority>{priority}</priority>\n"
        sitemap_content += "   </url>\n"
        
    sitemap_content += '</urlset>'
    
    with open(os.path.join(ROOT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_content)
    print("Sitemap generated.")

    # Update robots.txt
    robots_content = f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml"
    with open(os.path.join(ROOT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots_content)
    print("robots.txt updated.")

def main():
    for root, dirs, files in os.walk(ROOT_DIR):
        if "node_modules" in root or ".git" in root:
            continue
        for file in files:
            if file.endswith(".html"):
                process_file(os.path.join(root, file))
    
    generate_sitemap()

if __name__ == "__main__":
    main()
