import customtkinter as ctk
import pyqrcode
import png
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar

root = ctk.CTk()
root.geometry("750x750")
root.title("QR Code Reader | Generator")

def create_code(): 
    input_path = filedialog.asksaveasfilename(title="Save Image",
        filetyp=(("PNG File", ".png"), ("All Files","*.*")))
    
    if input_path:
        if input_path.endswith(".png"):
            get_code =pyqrcode.create(entry.get())
            get_code.png(input_path, scale=8)
        else:
            input_path =f'{input_path}.png'
            get_code =pyqrcode.create(entry.get())
            get_code.png(input_path=8)
            
        global get_image
        get_image = ImageTk.PhotoImage(Image.open(input_path))
        qr_label.configure(image=get_image, padx=20, pady=20)
        finished_label = ctk.CTkLabel(qr_frame, text="Finished", font=ctk.CTkFont(size=12))
        finished_label.pack(pady=10)
        entry.delete(0, ctk.END)
        
    
def read_code():
    # Open a file dialog box to select the image file
    file_path = filedialog.askopenfilename(title="Select Image", filetypes=(("Image Files", "*.png;*.jpg;*.jpeg;*.gif"), ("All Files", "*.*")))
    if file_path:
        # Attempt to decode the QR code in the selected image file
        try:
            with Image.open(file_path) as img:
                qr_code = pyqrcode.decode(img)
                # Display the decoded text in the text box
                text_box.delete("1.0", "end")
                text_box.insert("end", qr_code.data)
                # Show the image with the detected QR code in the GUI
                global qr_image
                qr_image = ImageTk.PhotoImage(img)
                qr_label.configure(image=qr_image, padx=20, pady=20)
                finished_label = ctk.CTkLabel(qr_frame, text="Finished", font=ctk.CTkFont(size=12))
                finished_label.pack(pady=10)
        except pyqrcode.exceptions.DataOverflowError:
            messagebox.showerror("Error", "The QR code in the selected image is too large to decode.")
        except pyqrcode.exceptions.DecodingError:
            messagebox.showerror("Error", "Failed to decode a QR code in the selected image.")

def decode_qr_code():
    image_path = filedialog.askopenfilename(title="Select Image", filetypes=(("PNG files", "*.png"), ("All files", "*.*")))
    if image_path:
        image = cv2.imread(image_path)
        decoded_objects = pyzbar.decode(image)
        for obj in decoded_objects:
            return obj.data.decode("utf-8")
        return "QR Code not found or could not be read"

title_label = ctk.CTkLabel(root, text="Generate and Read QR Code", font=ctk.CTkFont(size=24, weight="bold"))
title_label.pack(padx=10, pady=20)

scrollable_frame = ctk.CTkScrollableFrame(root, width=500, height=500)    
scrollable_frame.pack()

entry = ctk.CTkEntry(scrollable_frame, placeholder_text="Add text or URL")
entry.pack(fill="x", pady=10)

add_button = ctk.CTkButton(root, text="Create Code", width=500, command=create_code)
add_button.pack(pady=10)

read_button = ctk.CTkButton(root, text="Read QR Code", width=500, command=read_code)
read_button.pack(pady=10)

qr_frame = ctk.CTkFrame(scrollable_frame)
qr_frame.pack(padx=10, pady=10)

qr_label = ctk.CTkLabel(qr_frame ,text="" )
qr_label.pack()

text_box_frame = ctk.CTkFrame(root)
text_box_frame.pack(padx=10, pady=10)

text_box_label = ctk.CTkLabel(text_box_frame, text="Decoded QR Code Data:", font=ctk.CTkFont(size=12))
text_box_label.pack()

text_box = ctk.CTkTextbox(text_box_frame, height=5)
text_box.pack(fill="x", pady=10)

root.mainloop()
