# Secure Image Steganography Tool

A dual-layer security application that encrypts sensitive data using **AES-256** and hides it within images using **LSB Steganography** via OpenCV.

## 🚀 Features
- **AES-256 Encryption**: Ensures data remains unreadable even if detected.
- **LSB Embedding**: Low-distortion hiding technique.
- **Distortion Analysis**: Built-in PSNR and MSE calculators to measure image integrity.
- **Secure Key Management**: Password-based key derivation (PBKDF2).

## 🛠️ Tech Stack
- **Language**: Python 3.9+
- **Image Processing**: OpenCV
- **Cryptography**: PyCryptodome
- **GUI**: CustomTkinter

## 📋 Installation
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🕹️ Usage
1. Run `python src/main_gui.py`.
2. Select an image and enter your secret message.
3. Provide a strong password (this generates your AES key).
4. Click **Encode** to generate the "stego-image."
5. To retrieve the data, use the **Decode** tab with the same password.

## 📊 Evaluation Metrics
- **MSE**: Measures the average squared difference between the original and stego-image.
- **PSNR**: High values (>30dB) indicate that the hidden data is virtually invisible.
