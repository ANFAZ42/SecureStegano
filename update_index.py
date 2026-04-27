import os

file_path = "index.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace window HTML
old_html = """    <!-- ENCODE WINDOW -->
    <div class="glass-window main-window active-window" id="encode-window">
        <div class="window-header">
           <span class="window-title">SecureStegano » ENCODE</span>
           <button class="info-btn" onclick="openModal()" title="How it works">ⓘ</button>
        </div>
        <div class="window-body">
            <div class="form-group">
                <label>Target Image (carrier) - Drop Here</label>
                <input type="file" id="encode-image" accept="image/*">
            </div>
            <div class="form-group">
                <label>Secret Payload (message)</label>
                <textarea id="secret-message" rows="4" placeholder="Enter text to securely hide within the image..."></textarea>
            </div>
            <div class="form-group">
                <label>Encryption Key (AES-256)</label>
                <input type="password" id="encode-password" placeholder="Enter a secure password...">
            </div>
            <button class="action-btn" onclick="executeEncode()">Encrypt & Hide</button>
        </div>
        <div class="window-footer">
           <button class="switch-btn" onclick="toggleMode('decode')">Switch to Decode ➔</button>
        </div>
    </div>

    <!-- DECODE WINDOW -->
    <div class="glass-window main-window hidden-window" id="decode-window">
        <div class="window-header">
           <span class="window-title">SecureStegano » DECODE</span>
           <button class="info-btn" onclick="openModal()" title="How it works">ⓘ</button>
        </div>
        <div class="window-body">
            <div class="form-group">
                <label>Encoded Image (stego-image) - Drop Here</label>
                <input type="file" id="decode-image" accept="image/*">
            </div>
            <div class="form-group">
                <label>Decryption Key (AES-256)</label>
                <input type="password" id="decode-password" placeholder="Enter the secure password...">
            </div>
            <button class="action-btn" onclick="executeDecode()">Extract & Decrypt</button>
            <div class="form-group" style="margin-top: 25px;">
                <label>Extracted Payload</label>
                <textarea id="decoded-message" rows="4" placeholder="Decoded message will appear here..." readonly style="background: rgba(0,0,0,0.8);"></textarea>
            </div>
        </div>
        <div class="window-footer">
           <button class="switch-btn" onclick="toggleMode('encode')">Switch to Encode ➔</button>
        </div>
    </div>"""

new_html = """    <!-- ENCODE WINDOW -->
    <div class="glass-window main-window active-window" id="encode-window">
        <div class="window-header">
           <span class="window-title">SecureStegano » ENCODE</span>
           <button class="info-btn" onclick="openModal()" title="How it works">ⓘ</button>
        </div>
        <div class="window-body">
            <div class="form-group">
                <label>Target Image (carrier) - Drop Here</label>
                <input type="file" id="encode-image" accept="image/*">
            </div>
            <div class="form-group">
                <label>Secret Payload (message)</label>
                <textarea id="secret-message" rows="4" placeholder="Enter text to securely hide within the image..."></textarea>
            </div>
            <div class="form-group">
                <label>Encryption Key (AES-256)</label>
                <input type="password" id="encode-password" placeholder="Enter a secure password...">
            </div>
            <button class="action-btn" onclick="executeEncode()">Encrypt & Hide</button>
            <div id="encode-progress-box" style="display:none; margin-top:20px; border:1px solid var(--primary); height: 25px; position:relative; background: rgba(0,0,0,0.5);">
                 <div id="encode-progress-fill" style="width:0%; height:100%; background:var(--primary); opacity:0.4; transition: width 0.2s;"></div>
                 <div id="encode-progress-text" style="position:absolute; top:0; left:0; width:100%; text-align:center; font-size:12px; line-height:25px; color:#fff; font-weight:bold; letter-spacing:1px;">[0%] INITIATING SEQUENCE...</div>
            </div>
        </div>
        <div class="window-footer">
           <button class="switch-btn" onclick="toggleMode('analyze')">Switch to Analyze</button>&nbsp;&nbsp;&nbsp;&nbsp;
           <button class="switch-btn" onclick="toggleMode('decode')">Switch to Decode ➔</button>
        </div>
    </div>

    <!-- DECODE WINDOW -->
    <div class="glass-window main-window hidden-window" id="decode-window">
        <div class="window-header">
           <span class="window-title">SecureStegano » DECODE</span>
           <button class="info-btn" onclick="openModal()" title="How it works">ⓘ</button>
        </div>
        <div class="window-body">
            <div class="form-group">
                <label>Encoded Image (stego-image) - Drop Here</label>
                <input type="file" id="decode-image" accept="image/*">
            </div>
            <div class="form-group">
                <label>Decryption Key (AES-256)</label>
                <input type="password" id="decode-password" placeholder="Enter the secure password...">
            </div>
            <button class="action-btn" onclick="executeDecode()">Extract & Decrypt</button>
            <div id="decode-progress-box" style="display:none; margin-top:20px; border:1px solid var(--primary); height: 25px; position:relative; background: rgba(0,0,0,0.5);">
                 <div id="decode-progress-fill" style="width:0%; height:100%; background:var(--primary); opacity:0.4; transition: width 0.2s;"></div>
                 <div id="decode-progress-text" style="position:absolute; top:0; left:0; width:100%; text-align:center; font-size:12px; line-height:25px; color:#fff; font-weight:bold; letter-spacing:1px;">[0%] BYPASSING SECURITY...</div>
            </div>
            <div class="form-group" style="margin-top: 25px;">
                <label>Extracted Payload</label>
                <textarea id="decoded-message" rows="4" placeholder="Decoded message will appear here..." readonly style="background: rgba(0,0,0,0.8);"></textarea>
            </div>
        </div>
        <div class="window-footer">
           <button class="switch-btn" onclick="toggleMode('analyze')">Switch to Analyze</button>&nbsp;&nbsp;&nbsp;&nbsp;
           <button class="switch-btn" onclick="toggleMode('encode')">Switch to Encode ➔</button>
        </div>
    </div>
    
    <!-- ANALYZE WINDOW -->
    <div class="glass-window main-window hidden-window" id="analyze-window">
        <div class="window-header">
           <span class="window-title">SecureStegano » ANALYZE</span>
           <button class="info-btn" onclick="openModal()" title="How it works">ⓘ</button>
        </div>
        <div class="window-body">
            <div class="form-group">
                <label>Image for Analysis (Chi-Square LSB Detection) - Drop Here</label>
                <input type="file" id="analyze-image" accept="image/*">
            </div>
            <button class="action-btn" onclick="executeAnalyze()">Run Chi-Square Scan</button>
            <div class="form-group" id="analyze-result-container" style="display:none; margin-top: 15px;">
                <label>Scan Results</label>
                <div style="background: rgba(0,0,0,0.8); border: 1px solid var(--primary); padding: 15px; text-align: center;">
                    <div style="font-size: 0.9rem; margin-bottom: 10px; color: #aaa;">Probability of LSB Modification</div>
                    <div id="analyze-perc" style="font-size: 3rem; font-weight: bold; font-family: monospace;">0.00%</div>
                    <div id="analyze-verdict" style="margin-top: 10px; font-weight: bold; text-transform: uppercase;">CLEAN</div>
                </div>
            </div>
        </div>
        <div class="window-footer">
           <button class="switch-btn" onclick="toggleMode('encode')">Switch to Encode</button>&nbsp;&nbsp;&nbsp;&nbsp;
           <button class="switch-btn" onclick="toggleMode('decode')">Switch to Decode ➔</button>
        </div>
    </div>"""

content = content.replace(old_html, new_html)

# Replace JS logic
js_start = content.find("// --- Window Toggling Logic ---")
new_js = """// --- Window Toggling Logic ---
        function toggleMode(targetMode) {
            const encodeWin = document.getElementById('encode-window');
            const decodeWin = document.getElementById('decode-window');
            const analyzeWin = document.getElementById('analyze-window');
            
            [encodeWin, decodeWin, analyzeWin].forEach(win => {
                if(win) {
                    win.classList.remove('active-window');
                    win.classList.add('hidden-window');
                    win.classList.remove('drag-active');
                }
            });
            
            if (targetMode === 'decode') {
                decodeWin.classList.remove('hidden-window');
                decodeWin.classList.add('active-window');
            } else if (targetMode === 'analyze') {
                analyzeWin.classList.remove('hidden-window');
                analyzeWin.classList.add('active-window');
            } else {
                encodeWin.classList.remove('hidden-window');
                encodeWin.classList.add('active-window');
            }
        }

        // --- Modal Logic ---
        function openModal() {
            document.getElementById('info-modal').classList.add('active');
            const wins = [document.getElementById('encode-window'), document.getElementById('decode-window'), document.getElementById('analyze-window')];
            wins.forEach(win => {
                if(win && win.classList.contains('active-window')) {
                    win.style.opacity = '0.3';
                    win.style.pointerEvents = 'none';
                }
            });
        }

        function closeModal() {
            document.getElementById('info-modal').classList.remove('active');
            const wins = [document.getElementById('encode-window'), document.getElementById('decode-window'), document.getElementById('analyze-window')];
            wins.forEach(win => {
                if(win && win.classList.contains('active-window')) {
                    win.style.opacity = '';
                    win.style.pointerEvents = '';
                }
            });
        }

        // --- Async Job Polling ---
        function pollJobProgress(jobId, uiPrefix, downloadUrl, successMsg, payloadCallback) {
            const interval = setInterval(async () => {
                try {
                    const res = await fetch(`/progress/${jobId}`);
                    const data = await res.json();
                    
                    if(data.error) {
                        clearInterval(interval);
                        showNotification('Job Error: ' + data.error, true);
                        resetButtonState(uiPrefix);
                        return;
                    }
                    
                    const pbox = document.getElementById(`${uiPrefix}-progress-box`);
                    const pfill = document.getElementById(`${uiPrefix}-progress-fill`);
                    const ptext = document.getElementById(`${uiPrefix}-progress-text`);
                    
                    pbox.style.display = 'block';
                    pfill.style.width = data.progress + '%';
                    ptext.innerText = `[${data.progress}%] EXTRACTING DATA...`;
                    
                    if(data.status === 'completed') {
                        clearInterval(interval);
                        ptext.innerText = `[100%] OPERATION SUCCESSFUL`;
                        pfill.style.background = '#00FF41';
                        
                        setTimeout(() => {
                            pbox.style.display = 'none';
                            resetButtonState(uiPrefix);
                            showNotification(successMsg);
                        }, 1000);
                        
                        if(uiPrefix === 'encode') {
                            const a = document.createElement('a');
                            a.style.display = 'none';
                            a.href = downloadUrl;
                            a.download = `stego_image.png`;
                            document.body.appendChild(a);
                            a.click();
                            window.URL.revokeObjectURL(downloadUrl);
                        } else if(uiPrefix === 'decode' && payloadCallback) {
                            payloadCallback(data.message);
                        }
                    } else if(data.status === 'error') {
                        clearInterval(interval);
                        ptext.innerText = `[ERROR] OPERATION FAILED`;
                        pfill.style.background = '#FF2A55';
                        setTimeout(() => {
                            pbox.style.display = 'none';
                            resetButtonState(uiPrefix);
                            showNotification('Job Error: ' + data.error, true);
                        }, 1000);
                    }
                } catch(err) {
                    // Just log and continue, likely a network hiccup
                    console.error("Polling error: ", err);
                }
            }, 1000);
        }

        function resetButtonState(uiPrefix) {
            const btn = document.querySelector(`#${uiPrefix}-window .action-btn`);
            if(uiPrefix === 'encode') btn.innerText = 'Encrypt & Hide';
            else if(uiPrefix === 'decode') btn.innerText = 'Extract & Decrypt';
            else if(uiPrefix === 'analyze') btn.innerText = 'Run Chi-Square Scan';
            btn.style.color = '';
            btn.style.backgroundColor = '';
        }

        function setButtonActiveState(uiPrefix, text) {
            const btn = document.querySelector(`#${uiPrefix}-window .action-btn`);
            btn.innerText = text;
            btn.style.color = '#000';
            btn.style.backgroundColor = '#00FF41';
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
            const fileInput = document.getElementById('analyze-image');
            
            if(!fileInput.files || !fileInput.files[0]) {
                showNotification('Please load an image to analyze.', true);
                return;
            }
            
            setButtonActiveState('analyze', 'SCANNING...');
            
            const formData = new FormData();
            formData.append('image', fileInput.files[0]);
            
            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    body: formData
                });
                
                if(response.ok) {
                    const data = await response.json();
                    const prob = (parseFloat(data.probability) * 100).toFixed(2);
                    
                    document.getElementById('analyze-result-container').style.display = 'block';
                    const percEl = document.getElementById('analyze-perc');
                    const verdictEl = document.getElementById('analyze-verdict');
                    
                    percEl.innerText = prob + '%';
                    if (parseFloat(data.probability) > 0.90) {
                        percEl.style.color = '#FF2A55';
                        verdictEl.innerText = 'HIGH PROBABILITY OF HIDDEN PAYLOAD';
                        verdictEl.style.color = '#FF2A55';
                        showNotification('Alert: Potential steganography detected.', true);
                    } else if (parseFloat(data.probability) > 0.50) {
                        percEl.style.color = '#FFD700';
                        verdictEl.innerText = 'SUSPICIOUS ANOMALIES DETECTED';
                        verdictEl.style.color = '#FFD700';
                    } else {
                        percEl.style.color = '#00FF41';
                        verdictEl.innerText = 'APPEARS CLEAN';
                        verdictEl.style.color = '#00FF41';
                    }
                } else {
                    const text = await response.text();
                    try {
                        const err = JSON.parse(text);
                        showNotification('Server Error: ' + err.error, true);
                    } catch(e) {
                        showNotification('Server Error: ' + text, true);
                    }
                }
            } catch (error) {
                showNotification('Network Error: ' + error.message, true);
            }
            
            resetButtonState('analyze');
        }"""
content = content[:js_start] + new_js + "\n    </script>\n</body>\n</html>\n"

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
