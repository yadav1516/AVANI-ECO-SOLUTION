import os
import re

PROJECT_DIR = '/Users/avinash/Pareesan Services Pvt. Ltd./PAREESAN/'

# The CORRECT Mobile Menu HTML (Matches Desktop Nav)
MOBILE_MENU_HTML = """    <div class="mobile-menu-overlay"></div>
    <div class="mobile-menu">
        <div class="mobile-menu-header">
            <!-- Logo Removed as per user request -->
            <button class="close-menu" aria-label="Close Menu"><i class="fas fa-times"></i></button>
        </div>
        <ul class="mobile-nav-links">
            <li class="mobile-dropdown">
                <a href="javascript:void(0)">About Us <i class="fas fa-chevron-down"></i></a>
                <ul class="mobile-submenu">
                    <li><a href="about.html">Who We Are</a></li>
                    <li><a href="team.html">Our Team</a></li>
                    <li><a href="clients.html">Our Clients</a></li>
                    <li><a href="careers.html">Careers</a></li>
                </ul>
            </li>
            <li class="mobile-dropdown">
                <a href="javascript:void(0)">Services <i class="fas fa-chevron-down"></i></a>
                <ul class="mobile-submenu">
                    <li><a href="solutions.html">Our Solutions</a></li>
                    <li><a href="solar-epc.html">Solar EPC</a></li>
                    <li><a href="installation.html">Installation</a></li>
                    <li><a href="om-services.html">O&M Services</a></li>
                </ul>
            </li>
            <li><a href="projects.html">Projects</a></li>
            <li><a href="catalogue.html">Catalogue</a></li>
            <li class="mobile-dropdown">
                <a href="javascript:void(0)">Calculators <i class="fas fa-chevron-down"></i></a>
                <ul class="mobile-submenu">
                    <li><a href="calc.html">Solar ROI Calculator</a></li>
                    <li><a href="load-calculator.html">Load Calculator</a></li>
                </ul>
            </li>
            <li><a href="blog.html">Blog</a></li>
        </ul>
        <div class="mobile-menu-actions">
            <a href="contact.html" class="btn btn-outline-dark btn-block mb-3" style="width: 100%; border-radius: 50px; text-align: center; display: block; margin-bottom: 15px;">Contact Us</a>
            <a href="consultation.html" class="btn btn-primary btn-block" style="width: 100%; border-radius: 50px; text-align: center; display: block;">Get Free Consultation</a>
        </div>
    </div>"""

def update_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to capture the existing mobile menu block
    # Matches from <div class="mobile-menu-overlay"> to the closing </div> of .mobile-menu
    # We look for the pattern: Overlay -> Mobile Menu Header -> ... -> End of Mobile Menu
    
    # Simpler approach: Match everything from <div class="mobile-menu-overlay"> to <div class="mobile-menu">...</div>
    # Using a non-greedy match for the content inside, but ensuring we capture the full block.
    # Since HTML parsing with regex is fragile, we will match the SPECIFIC known structures or a broad block if consistent.
    
    # Strategy: Replace the entire block starting from `<!-- Mobile Menu Overlay -->` or just `<div class="mobile-menu-overlay">` 
    # up to the closing `</div>` of the mobile menu.
    
    pattern = re.compile(r'<div class="mobile-menu-overlay"></div>\s*<div class="mobile-menu">.*?</ul>\s*(<div class="mobile-menu-actions">.*?</div>\s*)?</div>', re.DOTALL)
    
    if pattern.search(content):
        new_content = pattern.sub(MOBILE_MENU_HTML.strip(), content)
        
        # If the file content changed, write it back
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated: {os.path.basename(file_path)}")
        else:
            print(f"No changes needed: {os.path.basename(file_path)}")
    else:
        # Fallback for files that might not match exact formatting
        print(f"Skipped (Pattern not found): {os.path.basename(file_path)}")

def main():
    for root, dirs, files in os.walk(PROJECT_DIR):
        for file in files:
            if file.endswith('.html'):
                update_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
