import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import numpy as np
from tkinter import font as tkFont


def read_text_file(text_path):
    with open(text_path, 'r') as file:
        return file.read()

def write_text_file(output_path, text):
    with open(output_path, 'w') as file:
        file.write(text)

def is_ascii_list_valid(char_list):
    for char in char_list:
        if not isinstance(char, str) or len(char) != 1 or ord(char) > 127:
            return False
    return True

def encode_text_in_image(image_path, text, output_path):
    image = Image.open(image_path)
    pixels = np.array(image, dtype=np.uint8)

    print("Pixels:", pixels)


    binary_text = ''.join(format(ord(char), '08b') for char in text) + '00000000' 

    num_pixels = pixels.size // 3
    if len(binary_text) > num_pixels * 3:
        raise ValueError("Text is too long to hide in the image.")

    idx = 0
    for i in range(pixels.shape[0]):
        for j in range(pixels.shape[1]):
            if idx >= len(binary_text):
                break
            for k in range(3):  
                if idx >= len(binary_text):
                    break
                pixel_val = pixels[i, j, k]
                bit = int(binary_text[idx])

                print(f"Original pixel value: {pixel_val}, Bit to encode: {bit}")

                print('--------',pixel_val, bit)
                new_pixel_val = (int(pixel_val) & ~1) | bit 
                if new_pixel_val < 0 or new_pixel_val > 255:
                    print(f"Invalid pixel value: {new_pixel_val}")

                pixels[i, j, k] = new_pixel_val
                idx += 1

    encoded_image = Image.fromarray(pixels)
    encoded_image.save(output_path)

def decode_text_from_image(image_path):
    image = Image.open(image_path)
    pixels = np.array(image, dtype=np.uint8)

    binary_text = ''
    for i in range(pixels.shape[0]):
        for j in range(pixels.shape[1]):
            for k in range(3):  
                pixel_val = pixels[i, j, k]
                binary_text += str(pixel_val & 1)

    chars = []
    for i in range(0, len(binary_text), 8):
        byte = binary_text[i:i+8]
        if byte == '00000000':  
            break
        chars.append(chr(int(byte, 2)))

    isValidText = is_ascii_list_valid(chars)

    if not isValidText:
        messagebox.showwarning("Invalid Text", "The image does not contain valid hidden text.")
        return  

    return ''.join(chars)

def upload_photo_and_text():
    root = tk.Tk()
    root.withdraw()

    photo_path = filedialog.askopenfilename(
        title="Select a Photo",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.gif")]
    )
    
    if not photo_path:
        print("No photo selected")
        return

    print(f"Selected photo: {photo_path}")

    text_path = filedialog.askopenfilename(
        title="Select a Text Document",
        filetypes=[("Text Files", "*.txt")]
    )
    
    if not text_path:
        print("No text document selected")
        return

    print(f"Selected text document: {text_path}")

    text = read_text_file(text_path)
    
    output_path = 'result.png'
    encode_text_in_image(photo_path, text, output_path)
    
    print(f"Encoded image saved as: {output_path}")

    root.quit()

def extract_text_from_image():
    root = tk.Tk()
    root.withdraw()

    photo_path = filedialog.askopenfilename(
        title="Select a Photo with Hidden Text",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.gif")]
    )
    
    if not photo_path:
        print("No photo selected")
        return

    print(f"Selected photo: {photo_path}")

    hidden_text = decode_text_from_image(photo_path)

    if not hidden_text:
        root.quit()
        return

    output_text_path = 'result.txt'
    write_text_file(output_text_path, hidden_text)
    
    print(f"Extracted text saved as: {output_text_path}")

    root.quit()

def choose_operation():
    root = tk.Tk()
    root.title("PVD Algorithm - Choose Operation")
    root.geometry("400x250")  
    root.eval('tk::PlaceWindow . center') 

    title_font = tkFont.Font(family="Helvetica", size=16, weight="bold")
    button_font = tkFont.Font(family="Helvetica", size=12)

    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack(expand=True)

    label = tk.Label(frame, text="Choose what you want to do:", font=title_font)
    label.pack(pady=10)

    encode_button = tk.Button(frame, text="Hide Text in Image", font=button_font, bg="#4CAF50", fg="black", padx=10, pady=5, 
                                command=lambda: [root.destroy(), upload_photo_and_text()])
    encode_button.pack(pady=5, fill=tk.X)

    decode_button = tk.Button(frame, text="Extract Text from Image", font=button_font, bg="#2196F3", fg="black", padx=10, pady=5, 
                                command=lambda: [root.destroy(), extract_text_from_image()])
    decode_button.pack(pady=5, fill=tk.X)

    root.mainloop()

choose_operation()
