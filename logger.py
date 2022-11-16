import tkinter as tk

class tkinterLogger():
    def __init__(self, textbox):
        self.textbox = textbox
        
    def write(self, text):
        self.textbox.insert(tk.END, text)
        self.textbox.see("end")
    def flush(self):
        pass