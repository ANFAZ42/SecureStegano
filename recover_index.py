import os
import re

log_path = r"C:\Users\Soundharya G\.gemini\antigravity\brain\7bd8e6e3-53e6-4476-8a94-79e575591d00\.system_generated\logs\overview.txt"

with open(log_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

html_lines = []
capturing = False
for line in lines:
    if line.strip() == "1: <!DOCTYPE html>":
        capturing = True
        # Clear in case it finds multiple view_files, we want the first or last? The first one is fine.
        html_lines = []
    
    if capturing:
        html_lines.append(line)
        if line.strip() == "799: </html>":
            break

# Now strip the "1: ", "2: " prefixes
clean_html = []
for line in html_lines:
    # Regex to match start of line digits followed by colon and space
    clean_line = re.sub(r'^\d+:\s', '', line)
    clean_html.append(clean_line)

recovered_html = "".join(clean_html)

# Apply State 2 (Remove "Switch to Analyze")
recovered_html = recovered_html.replace(
'''           <button class="switch-btn" onclick="toggleMode('analyze')">Switch to Analyze</button>&nbsp;&nbsp;&nbsp;&nbsp;
           <button class="switch-btn" onclick="toggleMode('decode')">Switch to Decode ➔</button>''',
'''           <button class="switch-btn" onclick="toggleMode('decode')">Switch to Decode ➔</button>'''
)

recovered_html = recovered_html.replace(
'''           <button class="switch-btn" onclick="toggleMode('analyze')">Switch to Analyze</button>&nbsp;&nbsp;&nbsp;&nbsp;
           <button class="switch-btn" onclick="toggleMode('encode')">Switch to Encode ➔</button>''',
'''           <button class="switch-btn" onclick="toggleMode('encode')">Switch to Encode ➔</button>'''
)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(recovered_html)

print(f"Recovered State 2: {len(clean_html)} lines.")
