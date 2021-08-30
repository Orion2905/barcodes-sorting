# Importing library
import cv2
from pyzbar.pyzbar import decode

import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.scrolledtext as scrolledtext

# Other scripts
import printLogger
import csv_options


class ScrollableFrame_x(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self, borderwidth=0, highlightthickness = 0, relief="groove", width=1000, height=280, bg="#c8d6e5")
        scrollbar = ttk.Scrollbar(self, orient="horizontal", command=canvas.xview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(xscrollcommand=scrollbar.set)

        canvas.pack(side="top", fill="both", expand=True)
        scrollbar.pack(side="bottom", fill="both")

class ChildRoot:
    def __init__(self, root):
        root.geometry("800x250")
        root.resizable(False, False)
        root.title("Barcodes Sorting Items") # Window title
        root.config(background='#747d8c')
        
        self.frame = ScrollableFrame_x(root)
        self.frame_2 = tk.Frame(self.frame.scrollable_frame)
        self.frame_3 = tk.Frame(root)
        self.combo_frame = tk.Frame(self.frame_2)

        for i in range(100):
            tk.Label(self.combo_frame, text="ciao").grid(row=0, column=i)

        self.frame_2.pack()
        self.frame_3.pack()
        self.combo_frame.pack()
        self.frame.pack()
