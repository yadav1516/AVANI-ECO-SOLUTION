
import os

directory = '/Users/avinash/Pareesan Services Pvt. Ltd./PAREESAN'
# The target string is unique: "Get QuoteQuote" and it's missing the closing </a>
# We want to replace "Get QuoteQuote" with "Get Quote</a>"
# But we should be careful. Let's look at the context from projects.html:
# <a href="..." ...>Get QuoteQuote
# <button ...
#
# We will replace '>Get QuoteQuote' with '>Get Quote</a>'

def fix_quote_typo(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if file has the typo
    if 'Get QuoteQuote' in content:
        # Replace the typo and add closing tag
        new_content = content.replace('>Get QuoteQuote', '>Get Quote</a>')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed {os.path.basename(filepath)}")
    else:
        # print(f"No typo in {os.path.basename(filepath)}")
        pass

for filename in os.listdir(directory):
    if filename.endswith('.html'):
        fix_quote_typo(os.path.join(directory, filename))
