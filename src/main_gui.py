import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import sys
from tkinterdnd2 import TkinterDnD, DND_FILES

# Add the project root to sys.path so it can find the 'src' module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.steganography import SteganographyEngine
from src.analysis import calculate_psnr, calculate_mse

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class SecureSteganoApp(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self):
        super().__init__()
        self.TkdndVersion = TkinterDnD._require(self)
        
        self.title("Secure Image Steganography")
        self.geometry("700x600")
        
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Title Label
        self.title_label = ctk.CTkLabel(self, text="Secure Image Steganography", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Create Tabview
        self.tabview = ctk.CTkTabview(self, width=650)
        self.tabview.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        
        # Add tabs
        self.tab_encode = self.tabview.add("Encode")
        self.tab_decode = self.tabview.add("Decode")
        
        self.setup_encode_tab()
        self.setup_decode_tab()
        
        # Enable Drag and Drop for the whole window
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.handle_file_drop)
        
    def handle_file_drop(self, event):
        # Clean up the file path (TkinterDnD2 sometimes wraps in {})
        file_path = event.data.strip('{}')
        
        # Basic validation to ensure it's an image
        valid_exts = ['.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp']
        if not any(file_path.lower().endswith(ext) for ext in valid_exts):
            messagebox.showwarning("Invalid File", "Please drop a valid image file.")
            return

        current_tab = self.tabview.get()
        if current_tab == "Encode":
            self.enc_img_path.set(file_path)
        elif current_tab == "Decode":
            self.dec_img_path.set(file_path)
            
    def setup_encode_tab(self):
        # Image Selection
        self.enc_img_path = ctk.StringVar()
        
        frame1 = ctk.CTkFrame(self.tab_encode, fg_color="transparent")
        frame1.pack(pady=10, fill="x")
        
        self.btn_select_img = ctk.CTkButton(frame1, text="Select Image", command=self.select_encode_image)
        self.btn_select_img.pack(side="left", padx=10)
        
        self.lbl_enc_img = ctk.CTkLabel(frame1, textvariable=self.enc_img_path, text_color="gray")
        self.lbl_enc_img.pack(side="left", padx=10)
        
        # Secret Message
        lbl_msg = ctk.CTkLabel(self.tab_encode, text="Secret Message (or drag & drop images anywhere!):")
        lbl_msg.pack(anchor="w", padx=10, pady=(10, 0))
        
        self.txt_message = ctk.CTkTextbox(self.tab_encode, height=150)
        self.txt_message.pack(padx=10, pady=5, fill="x")
        
        # Password
        lbl_pwd = ctk.CTkLabel(self.tab_encode, text="Password (AES Key):")
        lbl_pwd.pack(anchor="w", padx=10, pady=(10, 0))
        
        self.ent_enc_pwd = ctk.CTkEntry(self.tab_encode, show="*")
        self.ent_enc_pwd.pack(padx=10, pady=5, fill="x")
        
        # Action Button
        self.btn_encode = ctk.CTkButton(self.tab_encode, text="Encode & Save", command=self.perform_encode, fg_color="green", hover_color="darkgreen")
        self.btn_encode.pack(pady=20)
        
        # Analysis Metrics
        self.lbl_metrics = ctk.CTkLabel(self.tab_encode, text="", font=ctk.CTkFont(weight="bold"))
        self.lbl_metrics.pack(pady=5)
        
    def setup_decode_tab(self):
        # Stego Image Selection
        self.dec_img_path = ctk.StringVar()
        
        frame1 = ctk.CTkFrame(self.tab_decode, fg_color="transparent")
        frame1.pack(pady=10, fill="x")
        
        self.btn_select_stego = ctk.CTkButton(frame1, text="Select Stego Image", command=self.select_decode_image)
        self.btn_select_stego.pack(side="left", padx=10)
        
        self.lbl_dec_img = ctk.CTkLabel(frame1, textvariable=self.dec_img_path, text_color="gray")
        self.lbl_dec_img.pack(side="left", padx=10)
        
        # Password
        lbl_pwd = ctk.CTkLabel(self.tab_decode, text="Password:")
        lbl_pwd.pack(anchor="w", padx=10, pady=(10, 0))
        
        self.ent_dec_pwd = ctk.CTkEntry(self.tab_decode, show="*")
        self.ent_dec_pwd.pack(padx=10, pady=5, fill="x")
        
        # Action Button
        self.btn_decode = ctk.CTkButton(self.tab_decode, text="Decode", command=self.perform_decode)
        self.btn_decode.pack(pady=20)
        
        # Decoded Message
        lbl_msg = ctk.CTkLabel(self.tab_decode, text="Decoded Message:")
        lbl_msg.pack(anchor="w", padx=10, pady=(10, 0))
        
        self.txt_decoded = ctk.CTkTextbox(self.tab_decode, height=200, state="disabled")
        self.txt_decoded.pack(padx=10, pady=5, fill="x")

    def select_encode_image(self):
        filename = filedialog.askopenfilename(title="Select original image", filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff *.webp"), ("All files", "*.*")])
        if filename:
            self.enc_img_path.set(filename)

    def select_decode_image(self):
        filename = filedialog.askopenfilename(title="Select stego image", filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff *.webp"), ("All files", "*.*")])
        if filename:
            self.dec_img_path.set(filename)

    def perform_encode(self):
        img_path = self.enc_img_path.get()
        message = self.txt_message.get("1.0", "end-1c").strip()
        password = self.ent_enc_pwd.get()
        
        if not img_path or not message or not password:
            messagebox.showerror("Error", "Please provide image, message, and password.")
            return
            
        # Ensure data/output_images exists
        os.makedirs(os.path.join(os.getcwd(), 'data', 'output_images'), exist_ok=True)
        base_name = os.path.basename(img_path)
        name, _ = os.path.splitext(base_name)
        output_path = os.path.join(os.getcwd(), 'data', 'output_images', f"{name}_stego.png")
        
        try:
            SteganographyEngine.encode(img_path, password, message, output_path)
            
            # Calculate metrics
            mse = calculate_mse(img_path, output_path)
            psnr = calculate_psnr(img_path, output_path)
            
            self.lbl_metrics.configure(text=f"Success! Image saved to data/output_images/.\nMSE: {mse:.4f} | PSNR: {psnr:.2f} dB", text_color="green")
            messagebox.showinfo("Success", f"Data encoded successfully!\nSaved as: {output_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def perform_decode(self):
        img_path = self.dec_img_path.get()
        password = self.ent_dec_pwd.get()
        
        if not img_path or not password:
            messagebox.showerror("Error", "Please provide image and password.")
            return
            
        try:
            decoded_message = SteganographyEngine.decode(img_path, password)
            self.txt_decoded.configure(state="normal")
            self.txt_decoded.delete("1.0", "end")
            self.txt_decoded.insert("1.0", decoded_message)
            self.txt_decoded.configure(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    app = SecureSteganoApp()
    app.mainloop()

