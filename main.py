import qrcode
import re
import sys
import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image
from colorama import init, Fore, Style
from itertools import cycle

init(autoreset=True)

# Clear the terminal screen cross-platform
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# ASCII logo
ASCII_LOGO = r"""
  ______   _______    ______             __            __       
 /      \ |       \  /      \           |  \          |  \      
|  $$$$$$\| $$$$$$$\|  $$$$$$\ __    __  \$$  _______ | $$   __ 
| $$  | $$| $$__| $$| $$  | $$|  \  |  \|  \ /       \| $$  /  \
| $$  | $$| $$    $$| $$  | $$| $$  | $$| $$|  $$$$$$$| $$_/  $$
| $$ _| $$| $$$$$$$\| $$ _| $$| $$  | $$| $$| $$      | $$   $$ 
| $$/ \ $$| $$  | $$| $$/ \ $$| $$__/ $$| $$| $$_____ | $$$$$$\ 
 \$$ $$ $$| $$  | $$ \$$ $$ $$ \$$    $$| $$ \$$     \| $$  \$$\
  \$$$$$$\ \$$   \$$  \$$$$$$\  \$$$$$$  \$$  \$$$$$$$ \$$   \$$
      \$$$                \$$$                                  
"""

def print_rainbow_logo():
    colors = cycle([Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA])
    for line in ASCII_LOGO.splitlines():
        colored_line = ''
        for char in line:
            if char == ' ':
                colored_line += ' '
            else:
                colored_line += next(colors) + char
        print(colored_line)

# Validate URL
def is_valid_url(url):
    regex = re.compile(
        r'^(https?://)'
        r'([a-zA-Z0-9.-]+)\.[a-zA-Z]{2,}'
        r'(/[\w\-.~:/?#[\]@!$&\'()*+,;=]*)?$'
    )
    return re.match(regex, url) is not None

# Validate text
def is_valid_text(text):
    return all(c.isalnum() or c.isspace() or c in '.,;:!?@#&()-_=+[]{}<>*/\\\'\"' for c in text)

# File dialog for saving
def save_qr_image(img):
    tk.Tk().withdraw()
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG Image", "*.png"), ("JPEG Image", "*.jpg")],
        title="Save QR Code"
    )
    if file_path:
        img.save(file_path)
        print(Fore.GREEN + f"\nQR Code saved to: {file_path}\n")
    else:
        print(Fore.YELLOW + "\nSave cancelled.\n")

# Generate QR code without any logo
def create_qr(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    return img

# Handle QR generation menu
def make_qr_code():
    clear_console()
    print(Fore.WHITE + "1. Make URL QR Code")
    print(Fore.WHITE + "2. Make Text QR Code")
    print(" ")
    choice = input(Fore.CYAN + "Choose an option (1 or 2): ").strip()

    if choice == '1':
        url = input(Fore.CYAN + "Enter a valid URL (include http:// or https://): ").strip()
        if not is_valid_url(url):
            print(Fore.RED + "Invalid URL format!")
        else:
            img = create_qr(url)
            save_qr_image(img)

    elif choice == '2':
        text = input(Fore.CYAN + "Enter text: ").strip()
        if not is_valid_text(text):
            print(Fore.RED + "Invalid text input! Only alphanumerics and common punctuation allowed.")
        else:
            img = create_qr(text)
            save_qr_image(img)
    else:
        print(Fore.RED + "Invalid choice!")

    input(Fore.YELLOW + "\nPress Enter to return to menu...")
    clear_console()

# Main menu loop
def main():
    while True:
        clear_console()
        print_rainbow_logo()
        print(" ")
        print(Fore.WHITE + "1. Make QR Code")
        print(Fore.WHITE + "2. Exit")
        print(" ")
        choice = input(Fore.CYAN + "Choose an option (1 or 2): ").strip()

        if choice == '1':
            make_qr_code()
        elif choice == '2':
            clear_console()
            print(Fore.YELLOW + "Goodbye!")
            sys.exit()
        else:
            print(Fore.RED + "Invalid input. Please choose 1 or 2.\n")
            input(Fore.YELLOW + "Press Enter to try again...")
            clear_console()

if __name__ == "__main__":
    main()
