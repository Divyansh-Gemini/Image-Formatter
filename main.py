import os
import sys
from PIL import Image
import tkinter as tk
from tkinter import filedialog

def select_folder():
    # create a Tkinter root window & hide it
    root = tk.Tk()
    root.withdraw()

    # ask user to select a folder
    folder_path = filedialog.askdirectory()
    return folder_path

def resize_image(img, width, height):
    # resize image if required
    if width.lower() != 'skip' or height.lower() != 'skip':
        original_width, original_height = img.size

        # calculate new width & height
        try:
            if width.lower() != 'skip':
                new_width = int(width)
                new_height = int(original_height * new_width / original_width)
            
            if height.lower() != 'skip':
                new_height = int(height)
                new_width = int(original_width * new_height / original_height)
        
        except ValueError:
            print("--> height and width must be integers")
            sys.exit(4)

        # resize image
        try:
            img = img.resize((new_width, new_height))
        except ValueError:
            print("--> height and width must be > 0")
            sys.exit(1)
        except MemoryError:
            print("--> Image is too large to process")
            sys.exit(2)
        except OSError:
            print("--> Either file is not an image or it is corrupted")
            sys.exit(3)

    return img

def convert_to_rgb(img):
    # if image has transparent areas, convert it to RGB
    if img.mode in ('RGBA', 'LA'):
        img = img.convert('RGB')
    return img

def change_extension_and_save_image(dirpath, filename, img, extension):
    # save image with the new extension
    base_filename, _ = os.path.splitext(os.path.join(dirpath, filename))
    
    if extension.lower() != 'skip':
        new_file_path = base_filename + '.' + extension
        
        try:
            img.save(new_file_path)
        except ValueError:
            print("--> Invalid extension")
            sys.exit(3)
        
        # delete original image only if the new file path is different
        if new_file_path != os.path.join(dirpath, filename):
            os.remove(os.path.join(dirpath, filename))
    
    else:
        img.save(os.path.join(dirpath, filename))
    
    print(f"Image saved as {os.path.join(dirpath, filename)}")

def main():
    print("##### WELCOME TO IMAGE MODIFIER #####\n")

    folder_path = select_folder()

    # ask for required height / width & extension
    print("--> Type skip to keep the original value.\n")
    width = input("  Enter the required width: ")
    height = input("  Enter the required height: ")
    extension = input("  Enter the required extension: ")

    # iterate over each file & sub-folder in the selected folder
    for dirpath, dirnames, filenames in os.walk(folder_path):
        print(f"\n{dirpath}")

        # iterate over each file in the folder
        for filename in filenames:

            # if file is an image
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                img = Image.open(os.path.join(dirpath, filename))
                img  = resize_image(img, width, height)
                img = convert_to_rgb(img)
                change_extension_and_save_image(dirpath, filename, img, extension)

    print("\n--> Image resizing completed.\n")

if __name__ == "__main__":
    main()
