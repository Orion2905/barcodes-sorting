# Importing library
import cv2
from pyzbar.pyzbar import decode

import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.scrolledtext as scrolledtext
from tkinter import colorchooser
from tkinter import simpledialog
from tkinter import filedialog
from tkinter import messagebox
import os
import random

# Other scripts
import printLogger
import csv_options
import start_settings


from tkinter.ttk import *


class PrintLogger(): # create file like object
    def __init__(self, textbox): # pass reference to text widget

        self.textbox = textbox # keep ref

    def write(self, text):
        self.textbox.config(state=tk.NORMAL)
        self.textbox.insert(tk.END, text) # write text to textbox
            # could also scroll to end of textbox here to make sure always visible
        self.textbox.config(state=tk.DISABLED)

    def flush(self): # needed for file like object
        pass


"""
MenuBar with settings and other options
"""


class MenuBar:
    def __init__(self, parent):
        font = ('Corbel', 14)
        font_2 = ('Corbel', 10)

        menubar = tk.Menu(parent.root, font=font)
        parent.root.config(menu=menubar)

        file_dropdown = tk.Menu(menubar, font=font_2, tearoff=0)

        file_dropdown.add_command(label="Background Color") # command=parent.custom_color

        file_dropdown.add_command(label="About")

        file_dropdown.add_command(label="Update Items")

        menubar.add_cascade(label="Settings", menu=file_dropdown)


class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0, width=900, height=350, relief="flat")
        canvas.config(background='#70a1ff')
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview, bg="green")
        self.scrollable_frame = tk.Frame(canvas, bg="#5352ed")


        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

# The main class of the project


class MainApp:
    def __init__(self, root):

        root.geometry("1320x600")
        # root.resizable(False, False)
        root.title("Barcodes Sorting Items") # Window title
        root.config(background='#747d8c')

        self.root = root
        self.photo = PhotoImage(file=r"img/add.png").subsample(2, 2)
        self.photo_2 = PhotoImage(file=r"img/remove.png").subsample(2, 2)


        # Frames
        self.frame2 = ScrollableFrame(root)

        # [Widget section]
        # Title
        title = tk.Label(root, text="Barcodes Sorting Items", font=("Arial", 20, "bold"),
                         pady=20, relief="groove", border=5, padx=20, bg="#ff4757")
        title.pack(pady=10)


        self.show_items()

        # Frame pack
        self.frame2.pack()

        self.select_mod_btn = tk.Button(root, text="Startup settings",
                                        command=self.start_settings, width=1, height=1, font=("Arial", 13, "bold"), bd=4,
                                        bg="#2ed573", fg="#2f3542", border=4)
        self.select_mod_btn.pack(fill="x", padx=200, pady=10)

        csv_button = tk.Button(root, text="csv", command=self.csv_writer).pack()


        # Console
        self.t = scrolledtext.ScrolledText(
            root, height=2, bg="#2f3542", fg="#ced6e0", font=("Arial", 8, "bold"), state=tk.DISABLED
        )
        self.t.pack(fill="both", side=BOTTOM)

        pl = PrintLogger(self.t)
        sys.stdout = pl

        printLogger.message("Welcome back!")

    # [Functions]

    def clear_console(self):
        self.t.config(state=NORMAL)
        self.t.delete(1.0, END)
        self.t.config(state=DISABLED)

    def show_items(self):
        column_list = ["id", "barcode", "description", "itemValue", "QTY"]
        items = csv_options.csv_task("database/items.csv", "r")
        #print(items)

        for column in range(len(column_list)):
            tk.Label(
                self.frame2.scrollable_frame, text=column_list[column], relief="groove", width=17,
                bg="#a4b0be",font=("Arial", 13, "bold"), height=2
            ).grid(column=column, row=0, sticky=(N, E, W), pady=10, padx=2)

        for i in range(len(items)-1):
            for j in range(len(items[i].split(";"))):
                label = tk.Label(
                    self.frame2.scrollable_frame, text=items[i+1].split(";")[j], relief="groove", font=("Arial", 9, "bold"),
                    height=4
                )
                label.grid(column=j, row=i+1, sticky="we", padx=2)
                label.bind("<Button-1>", lambda e, url=label['text']: self.click_on_label(url))

    def select_mode(self):
        with open("config/mode.txt", "r") as f:
            mode = f.readline()

        if mode == "add":
            with open("config/mode.txt", "w") as f:
                f.write("delete")
                self.select_mod_btn['image'] = self.photo_2
        else:
            with open("config/mode.txt", "w") as f:
                f.write("add")
                self.select_mod_btn['image'] = self.photo


    def click_on_label(self, item):
        print(item)

    def csv_writer(self):
        get_id = len(csv_options.csv_task("database/items.csv", "r"))
        csv_options.csv_task("database/items.csv", "a", f"\n{str(get_id-1)};1234567890;test item 1;124;1")
        self.show_items()
        self.root.update()
        self.frame2.update()

    def start_settings(self):
        root = tk.Tk()
        run = start_settings.ChildRoot(root)
        root.mainloop()


# Make one method to decode the barcode
def barcode_reader(image):
    # read the image in numpy array using cv2
    img = cv2.imread(image)

    # Decode the barcode image
    detectedBarcodes = decode(img)

    # If not detected then print the message
    if not detectedBarcodes :
        print("Barcode Not Detected or your barcode is blank/corrupted!")
    else :

        # Traveres through all the detected barcodes in image
        for barcode in detectedBarcodes :

            # Locate the barcode position in image
            (x, y, w, h) = barcode.rect

            # Put the rectangle in image using
            # cv2 to heighlight the barcode
            cv2.rectangle(img, (x - 10, y - 10),
                          (x + w + 10, y + h + 10),
                          (255, 0, 0), 2)

            if barcode.data != "":
                # Print the barcode data
                print(barcode.data)
                print(barcode.type)
                print(barcode)

    # Display the image



if __name__ == "__main__" :
    # Take the image from user
    image = "barcode.png"
    barcode_reader(image)
    root = tk.Tk()
    run = MainApp(root)
    root.mainloop()