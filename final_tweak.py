import os

file_path = "index.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add CSS for the center alert
css_alert = """
        .center-hacker-alert {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 10, 0, 0.95);
            border: 2px solid var(--primary);
            color: var(--primary);
            font-family: 'JetBrains Mono', monospace;
            font-size: 18px;
            font-weight: bold;
            padding: 30px;
            min-width: 400px;
            text-align: center;
            z-index: 10000;
            box-shadow: 0 0 30px var(--primary-dim);
            border-top: 20px solid var(--primary);
            border-radius: 4px;
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        .center-hacker-alert::before {
            content: "SYSTEM_ALERT.EXE";
            position: absolute;
            top: -19px; left: 10px; color: black; font-weight: bold; font-size: 14px;
        }
"""
content = content.replace("/* Hacker Terminal Animations */", css_alert + "\n        /* Hacker Terminal Animations */")


# Add JS function for the center alert
js_alert = """
        function showCenterHackerAlert(message) {
            const alertBox = document.createElement('div');
            alertBox.className = 'center-hacker-alert';
            alertBox.innerText = `> ${message}`;
            document.body.appendChild(alertBox);
            
            setTimeout(() => { alertBox.style.opacity = '1'; }, 50);
            
            setTimeout(() => {
                alertBox.style.opacity = '0';
                setTimeout(() => alertBox.remove(), 300);
            }, 6000);
        }
        
"""
js_target = "// --- Hacker Movie Sequence ---"
content = content.replace(js_target, js_alert + js_target)

# Update pollJobProgress
content = content.replace(
    "showNotification(successMsg);",
    "showCenterHackerAlert(successMsg);"
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Center alert created.")
