import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import sys
import threading
from tkinterdnd2 import TkinterDnD, DND_FILES

# Add the project root to sys.path so it can find the 'src' module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.steganography import SteganographyEngine
from src.analysis import calculate_psnr, calculate_mse, detect_steganography_lsb

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class SecureSteganoApp(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self):
        super().__init__()
        self.TkdndVersion = TkinterDnD._require(self)
        
        self.title("Secure Image Steganography")
        self.geometry("750x650")
        
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Title Label
        self.title_label = ctk.CTkLabel(self, text="Secure Image Steganography", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Create Tabview
        self.tabview = ctk.CTkTabview(self, width=700)
        self.tabview.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        
        # Add tabs
        self.tab_encode = self.tabview.add("Encode")
        self.tab_decode = self.tabview.add("Decode")
        self.tab_analyze = self.tabview.add("Analyze")
        
        self.setup_encode_tab()
        self.setup_decode_tab()
        self.setup_analyze_tab()
        
        # Enable Drag and Drop for the whole window
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.handle_file_drop)
        
    def handle_file_drop(self, event):
        file_path = event.data.strip('{}')
        
        valid_exts = ['.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp']
        if not any(file_path.lower().endswith(ext) for ext in valid_exts):
            messagebox.showwarning("Invalid File", "Please drop a valid image file.")
            return

        current_tab = self.tabview.get()
        if current_tab == "Encode":
            self.enc_img_path.set(file_path)
        elif current_tab == "Decode":
            self.dec_img_path.set(file_path)
        elif current_tab == "Analyze":
            self.ana_img_path.set(file_path)
            
    def setup_encode_tab(self):
        self.enc_img_path = ctk.StringVar()
        
        frame1 = ctk.CTkFrame(self.tab_encode, fg_color="transparent")
        frame1.pack(pady=10, fill="x")
        
        self.btn_select_img = ctk.CTkButton(frame1, text="Select Image", command=self.select_encode_image)
        self.btn_select_img.pack(side="left", padx=10)
        
        self.lbl_enc_img = ctk.CTkLabel(frame1, textvariable=self.enc_img_path, text_color="gray")
        self.lbl_enc_img.pack(side="left", padx=10)
        
        lbl_msg = ctk.CTkLabel(self.tab_encode, text="Secret Message (or drag & drop images anywhere!):")
        lbl_msg.pack(anchor="w", padx=10, pady=(10, 0))
        
        self.txt_message = ctk.CTkTextbox(self.tab_encode, height=150)
        self.txt_message.pack(padx=10, pady=5, fill="x")
        
        lbl_pwd = ctk.CTkLabel(self.tab_encode, text="Password (AES Key):")
        lbl_pwd.pack(anchor="w", padx=10, pady=(10, 0))
        
        self.ent_enc_pwd = ctk.CTkEntry(self.tab_encode, show="*")
        self.ent_enc_pwd.pack(padx=10, pady=5, fill="x")
        
        self.btn_encode = ctk.CTkButton(self.tab_encode, text="Encode & Save", command=self.perform_encode, fg_color="green", hover_color="darkgreen")
        self.btn_encode.pack(pady=15)
        
        self.enc_progress = ctk.CTkProgressBar(self.tab_encode)
        self.enc_progress.pack(pady=5, fill="x", padx=20)
        self.enc_progress.set(0)
        self.enc_progress.pack_forget()
        
        self.lbl_metrics = ctk.CTkLabel(self.tab_encode, text="", font=ctk.CTkFont(weight="bold"))
        self.lbl_metrics.pack(pady=5)
        
    def setup_decode_tab(self):
        self.dec_img_path = ctk.StringVar()
        
        frame1 = ctk.CTkFrame(self.tab_decode, fg_color="transparent")
        frame1.pack(pady=10, fill="x")
        
        self.btn_select_stego = ctk.CTkButton(frame1, text="Select Stego Image", command=self.select_decode_image)
        self.btn_select_stego.pack(side="left", padx=10)
        
        self.lbl_dec_img = ctk.CTkLabel(frame1, textvariable=self.dec_img_path, text_color="gray")
        self.lbl_dec_img.pack(side="left", padx=10)
        
        lbl_pwd = ctk.CTkLabel(self.tab_decode, text="Password:")
        lbl_pwd.pack(anchor="w", padx=10, pady=(10, 0))
        
        self.ent_dec_pwd = ctk.CTkEntry(self.tab_decode, show="*")
        self.ent_dec_pwd.pack(padx=10, pady=5, fill="x")
        
        self.btn_decode = ctk.CTkButton(self.tab_decode, text="Decode", command=self.perform_decode)
        self.btn_decode.pack(pady=15)
        
        self.dec_progress = ctk.CTkProgressBar(self.tab_decode)
        self.dec_progress.pack(pady=5, fill="x", padx=20)
        self.dec_progress.set(0)
        self.dec_progress.pack_forget()
        
        lbl_msg = ctk.CTkLabel(self.tab_decode, text="Decoded Message:")
        lbl_msg.pack(anchor="w", padx=10, pady=(10, 0))
        
        self.txt_decoded = ctk.CTkTextbox(self.tab_decode, height=200, state="disabled")
        self.txt_decoded.pack(padx=10, pady=5, fill="x")

    def setup_analyze_tab(self):
        self.ana_img_path = ctk.StringVar()
        
        frame1 = ctk.CTkFrame(self.tab_analyze, fg_color="transparent")
        frame1.pack(pady=20, fill="x")
        
        self.btn_select_ana = ctk.CTkButton(frame1, text="Select Image to Analyze", command=self.select_analyze_image)
        self.btn_select_ana.pack(side="left", padx=10)
        
        self.lbl_ana_img = ctk.CTkLabel(frame1, textvariable=self.ana_img_path, text_color="gray")
        self.lbl_ana_img.pack(side="left", padx=10)
        
        lbl_info = ctk.CTkLabel(self.tab_analyze, text="Runs a Chi-Square statistical attack to detect randomized LSBs.\nHigh probabilities indicate an anomaly indicative of steganography.", text_color="gray")
        lbl_info.pack(pady=15)
        
        self.btn_analyze = ctk.CTkButton(self.tab_analyze, text="Calculate Probability", command=self.perform_analyze, fg_color="#C850C0", hover_color="#FFCC70")
        self.btn_analyze.pack(pady=20)
        
        self.lbl_ana_result = ctk.CTkLabel(self.tab_analyze, text="", font=ctk.CTkFont(size=36, weight="bold"))
        self.lbl_ana_result.pack(pady=20)
        
        self.lbl_ana_verdict = ctk.CTkLabel(self.tab_analyze, text="", font=ctk.CTkFont(size=18))
        self.lbl_ana_verdict.pack(pady=5)

    def select_encode_image(self):
        filename = filedialog.askopenfilename(title="Select original image", filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff *.webp"), ("All files", "*.*")])
        if filename: self.enc_img_path.set(filename)

    def select_decode_image(self):
        filename = filedialog.askopenfilename(title="Select stego image", filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff *.webp"), ("All files", "*.*")])
        if filename: self.dec_img_path.set(filename)
        
    def select_analyze_image(self):
        filename = filedialog.askopenfilename(title="Select image to analyze", filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff *.webp"), ("All files", "*.*")])
        if filename: self.ana_img_path.set(filename)

    def perform_encode(self):
        img_path = self.enc_img_path.get()
        message = self.txt_message.get("1.0", "end-1c").strip()
        password = self.ent_enc_pwd.get()
        
        if not img_path or not message or not password:
            messagebox.showerror("Error", "Please provide image, message, and password.")
            return
            
        os.makedirs(os.path.join(os.getcwd(), 'data', 'output_images'), exist_ok=True)
        base_name = os.path.basename(img_path)
        name, _ = os.path.splitext(base_name)
        output_path = os.path.join(os.getcwd(), 'data', 'output_images', f"{name}_stego.png")
        
        self.btn_encode.configure(state="disabled")
        self.enc_progress.pack(pady=5, fill="x", padx=20)
        self.enc_progress.set(0)
        self.lbl_metrics.configure(text="")
        
        def encode_thread():
            try:
                def progress_cb(pct):
                    self.after(0, lambda: self.enc_progress.set(pct / 100.0))
                    
                SteganographyEngine.encode(img_path, password, message, output_path, progress_callback=progress_cb)
                
                mse = calculate_mse(img_path, output_path)
                psnr = calculate_psnr(img_path, output_path)
                
                def on_success():
                    self.lbl_metrics.configure(text=f"Success! Image saved to data/output_images/.\nMSE: {mse:.4f} | PSNR: {psnr:.2f} dB", text_color="green")
                    self.btn_encode.configure(state="normal")
                    self.enc_progress.pack_forget()
                    messagebox.showinfo("Success", f"Data encoded successfully!\nSaved as: {output_path}")
                self.after(0, on_success)
                
            except Exception as e:
                def on_error():
                    self.btn_encode.configure(state="normal")
                    self.enc_progress.pack_forget()
                    messagebox.showerror("Error", str(e))
                self.after(0, on_error)

        threading.Thread(target=encode_thread, daemon=True).start()

    def perform_decode(self):
        img_path = self.dec_img_path.get()
        password = self.ent_dec_pwd.get()
        
        if not img_path or not password:
            messagebox.showerror("Error", "Please provide image and password.")
            return
            
        self.btn_decode.configure(state="disabled")
        self.dec_progress.pack(pady=5, fill="x", padx=20)
        self.dec_progress.set(0)
        
        def decode_thread():
            try:
                def progress_cb(pct):
                    self.after(0, lambda: self.dec_progress.set(pct / 100.0))
                    
                decoded_message = SteganographyEngine.decode(img_path, password, progress_callback=progress_cb)
                
                def on_success():
                    self.txt_decoded.configure(state="normal")
                    self.txt_decoded.delete("1.0", "end")
                    self.txt_decoded.insert("1.0", decoded_message)
                    self.txt_decoded.configure(state="disabled")
                    self.btn_decode.configure(state="normal")
                    self.dec_progress.pack_forget()
                self.after(0, on_success)
                
            except Exception as e:
                def on_error():
                    self.btn_decode.configure(state="normal")
                    self.dec_progress.pack_forget()
                    messagebox.showerror("Error", str(e))
                self.after(0, on_error)
                
        threading.Thread(target=decode_thread, daemon=True).start()
        
    def perform_analyze(self):
        img_path = self.ana_img_path.get()
        if not img_path:
            messagebox.showerror("Error", "Please select an image to analyze.")
            return
            
        self.lbl_ana_result.configure(text="Analyzing...", text_color="gray")
        self.lbl_ana_verdict.configure(text="")
        self.btn_analyze.configure(state="disabled")
        
        def analyze_thread():
            try:
                prob = detect_steganography_lsb(img_path)
                prob_perc = prob * 100
                
                def on_success():
                    self.lbl_ana_result.configure(text=f"{prob_perc:.2f}%")
                    if prob > 0.90:
                        self.lbl_ana_result.configure(text_color="red")
                        self.lbl_ana_verdict.configure(text="HIGH PROBABILITY OF HIDDEN PAYLOAD", text_color="red")
                    elif prob > 0.50:
                        self.lbl_ana_result.configure(text_color="orange")
                        self.lbl_ana_verdict.configure(text="SUSPICIOUS ANOMALIES DETECTED", text_color="orange")
                    else:
                        self.lbl_ana_result.configure(text_color="green")
                        self.lbl_ana_verdict.configure(text="APPEARS CLEAN", text_color="green")
                    self.btn_analyze.configure(state="normal")
                self.after(0, on_success)
            except Exception as e:
                def on_error():
                    self.lbl_ana_result.configure(text="Error", text_color="red")
                    self.btn_analyze.configure(state="normal")
                    messagebox.showerror("Error", str(e))
                self.after(0, on_error)
                
        threading.Thread(target=analyze_thread, daemon=True).start()

if __name__ == "__main__":
    app = SecureSteganoApp()
    app.mainloop()
