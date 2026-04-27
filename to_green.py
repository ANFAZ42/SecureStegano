import os

file_path = "index.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace variables
content = content.replace("--primary: #00E5FF;", "--primary: #00FF41;")
content = content.replace("rgba(0, 229, 255,", "rgba(0, 255, 65,")

# Replace gradients
content = content.replace("#0077FF", "#008F11") # darker green
content = content.replace("rgba(0, 119, 255,", "rgba(0, 143, 17,")
content = content.replace("#00F0FF", "#00FF41")
content = content.replace("#0088FF", "#00FF41")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Turned green.")
