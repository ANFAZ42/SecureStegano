import os

file_path = "index.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace numTerms
content = content.replace(
    "const numTerms = Math.floor(Math.random() * 4) + 4;",
    "const numTerms = 10;"
)

# Replace dimensions
content = content.replace(
    "const width = Math.floor(Math.random() * 250) + 200;\n                    const height = Math.floor(Math.random() * 200) + 150;",
    "const width = Math.floor(Math.random() * 400) + 400;\n                    const height = Math.floor(Math.random() * 300) + 300;"
)

# Replace rotation
content = content.replace(
    "const rotation = Math.floor(Math.random() * 30) - 15;",
    "const rotation = 0;"
)

# Replace text font size slightly larger to fit the big windows
content = content.replace(
    "font-size: 11px;",
    "font-size: 14px;"
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Tweaks applied successfully.")
