import os

file_path = "index.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# CSS injection
css_hacker = """
        /* Hacker Terminal Animations */
        .hacker-term {
            position: absolute;
            background: rgba(0, 5, 0, 0.9);
            border: 1px solid var(--primary);
            color: var(--primary);
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            padding: 10px;
            overflow: hidden;
            z-index: 9999;
            box-shadow: 0 0 15px rgba(0, 255, 65, 0.3);
            border-top: 15px solid var(--primary);
            border-radius: 4px;
            pointer-events: none;
            word-wrap: break-word;
            line-height: 1.3;
        }
        .hacker-term::before {
            content: "CMD / SYS // OVERRIDE";
            position: absolute;
            top: -14px; left: 5px; color: black; font-weight: bold; font-size: 10px;
        }
"""
content = content.replace("/* Toast Notifications */", css_hacker + "\n        /* Toast Notifications */")

# JS Injection
js_start = content.find("// --- API Interactions ---")

new_js = """// --- Hacker Movie Sequence ---
        function triggerHackerSequence(type) {
            return new Promise(resolve => {
                const terms = [];
                const numTerms = Math.floor(Math.random() * 4) + 4; // 4 to 7 terms
                
                const dummyTexts = [
                    "Bypassing mainframe security protocols...",
                    "Injecting LSB sequence vector 0x0FA9...",
                    "Establishing parallel SSL tunnel...",
                    "Overriding local hash sum validations...",
                    "Decrypting AES-256 ghost node padding...",
                    "[WARN] Firewall heartbeat dropped",
                    "Parsing hexadecimal buffer matrices...",
                    "Allocating virtual cipher blocks...",
                    "Mounting shadow filesystem..."
                ];
                
                for(let i=0; i<numTerms; i++) {
                    const term = document.createElement('div');
                    term.className = 'hacker-term';
                    
                    const width = Math.floor(Math.random() * 250) + 200;
                    const height = Math.floor(Math.random() * 200) + 150;
                    term.style.width = width + 'px';
                    term.style.height = height + 'px';
                    
                    const top = Math.floor(Math.random() * (window.innerHeight - height));
                    const left = Math.floor(Math.random() * (window.innerWidth - width));
                    term.style.top = top + 'px';
                    term.style.left = left + 'px';
                    
                    const rotation = Math.floor(Math.random() * 30) - 15; // -15 to +15 deg
                    term.style.transform = `rotate(${rotation}deg) scale(0)`;
                    term.style.transition = 'transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
                    
                    document.body.appendChild(term);
                    terms.push(term);
                    
                    // Pop in animation
                    setTimeout(() => { term.style.transform = `rotate(${rotation}deg) scale(1)`; }, i * 150);
                    
                    // Spitting code
                    let lineCount = 0;
                    const streamInterval = setInterval(() => {
                        if (lineCount > 15) { term.innerHTML = ''; lineCount = 0; }
                        
                        if (Math.random() > 0.7) {
                            const prog = Math.floor(Math.random() * 100);
                            const bars = "||||||||||||||||||||".substring(0, Math.floor(prog / 5));
                            term.innerHTML += `<div>[${bars.padEnd(20, '.')} ${prog}%]</div>`;
                        } else {
                            const hex = Array.from({length: 8}, () => Math.floor(Math.random()*16).toString(16)).join('').toUpperCase();
                            const msg = dummyTexts[Math.floor(Math.random() * dummyTexts.length)];
                            term.innerHTML += `<div>${type.substring(0,3)}_${hex}: ${msg}</div>`;
                        }
                        term.scrollTop = term.scrollHeight;
                        lineCount++;
                    }, Math.random() * 100 + 50);
                    
                    term.dataset.interval = streamInterval;
                }
                
                // End sequence after 4 seconds
                setTimeout(() => {
                    terms.forEach(term => {
                        clearInterval(term.dataset.interval);
                        term.style.transform = `scale(0)`;
                        setTimeout(() => term.remove(), 300);
                    });
                    resolve();
                }, 4000);
            });
        }

        // --- API Interactions ---
        async function executeEncode() {
            const fileInput = document.getElementById('encode-image');
            const messageInput = document.getElementById('secret-message');
            const passwordInput = document.getElementById('encode-password');
            
            if(!fileInput.files || !fileInput.files[0] || !messageInput.value || !passwordInput.value) {
                showNotification('Please provide image, message, and password.', true);
                return;
            }
            
            // Trigger 4s Movie Hack Sequence First
            document.getElementById('encode-window').style.opacity = '0.1';
            await triggerHackerSequence('ENC');
            document.getElementById('encode-window').style.opacity = '1';
            
            setButtonActiveState('encode', 'INITIALIZING...');
            
            const formData = new FormData();
            formData.append('image', fileInput.files[0]);
            formData.append('message', messageInput.value);
            formData.append('password', passwordInput.value);
            
            try {
                const response = await fetch('/encode', {
                    method: 'POST',
                    body: formData
                });
                
                if(response.ok) {
                    const data = await response.json();
                    const pbox = document.getElementById('encode-progress-box');
                    pbox.style.display = 'block';
                    pollJobProgress(data.job_id, 'encode', `/download/${data.job_id}`, 'Encode complete! Image generated.');
                } else {
                    resetButtonState('encode');
                    const text = await response.text();
                    try {
                        const err = JSON.parse(text);
                        showNotification('Server Error: ' + err.error, true);
                    } catch(e) {
                        showNotification('Server Error: ' + text, true);
                    }
                }
            } catch (error) {
                resetButtonState('encode');
                showNotification('Network Error: ' + error.message, true);
            }
        }

        async function executeDecode() {
            const fileInput = document.getElementById('decode-image');
            const passwordInput = document.getElementById('decode-password');
            
            if(!fileInput.files || !fileInput.files[0]) {
                showNotification('Please load an image to decode.', true);
                return;
            }
            if(!passwordInput.value) {
                showNotification('Please enter your AES password.', true);
                return;
            }
            
            // Trigger 4s Movie Hack Sequence First
            document.getElementById('decode-window').style.opacity = '0.1';
            await triggerHackerSequence('DEC');
            document.getElementById('decode-window').style.opacity = '1';
            
            setButtonActiveState('decode', 'ANALYZING...');
            
            const formData = new FormData();
            formData.append('image', fileInput.files[0]);
            formData.append('password', passwordInput.value);
            
            try {
                const response = await fetch('/decode', {
                    method: 'POST',
                    body: formData
                });
                
                if(response.ok) {
                    const data = await response.json();
                    document.getElementById('decoded-message').value = '';
                    const pbox = document.getElementById('decode-progress-box');
                    pbox.style.display = 'block';
                    pollJobProgress(data.job_id, 'decode', null, 'Data successfully decrypted!', (msg) => {
                        document.getElementById('decoded-message').value = msg;
                    });
                } else {
                    resetButtonState('decode');
                    const text = await response.text();
                    try {
                        const err = JSON.parse(text);
                        showNotification('Server Error: ' + err.error, true);
                    } catch(e) {
                        showNotification('Server Error: ' + text, true);
                    }
                }
            } catch (error) {
                resetButtonState('decode');
                showNotification('Network Error: ' + error.message, true);
            }
        }
        
        async function executeAnalyze() {
"""
content = content[:js_start] + new_js + content[content.find("async function executeAnalyze() {") + 33:]

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Injected successfully.")
