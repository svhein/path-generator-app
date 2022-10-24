import tkinter as tk
from tkinter import *
import tkinter.font as TkFont


class View(tk.Tk):
    
    def __init__(self, Controller):
        super().__init__()
        self.id = '1'
        self.title('Path Generator App')
        self.geometry('1280x720')
        self.configure(bg = 'lavender')
        self.resizable(width = False, height = False)
        self.image = None
        self.controller = Controller
        
        self._create_widgets()
        
    
    def _create_widgets(self):
        
        self.canvas = Canvas(self, width = 600, height = 600, bg = 'white', bd = 0, highlightthickness = 0)
        self.canvas.place(x = 350, rely = 0.5, anchor = CENTER)
        
        self.font10 = TkFont.Font(
            size = 8
        )
        
        self.canvasSlider_X = tk.Scale(
            self,
            orient = 'horizontal',
            length = 600,
            activebackground = 'white',
            from_ = 0,
            to = 600,
            font = self.font10,
            command = self.controller.onCanvasSliderChange
        )
        self.canvasSlider_X.place( x = 48, y = 19) 
        
        self.canvasSlider_Y = tk.Scale(
            self,
            orient = 'vertical',
            length = 600,
            activebackground = 'white',
            from_ = 0,
            to = 600,
            font = self.font10,
            command = self.controller.onCanvasSliderChange
        )
        self.canvasSlider_Y.place(x = 5, y = 58) 
        
        self.sliderFont = TkFont.Font(
            family = 'helvetica',
            size = 10,
            weight = 'bold'
        )
        
        # CONFIG SLIDERS #
        
        self.sliderArgs = {
            'font': self.sliderFont,
            'orient': 'horizontal',
            'length': 175,
            'activebackground': 'gray' 
            }
        
        self.maxValueSlider = tk.Scale(
            self,
            **self.sliderArgs,
            label = 'Max Value',
            from_ = 0,
            to = 255,
            command = self.controller.onConfigSliderChange
        )
        self.maxValueSlider.place(x = 670, y = 60)
        
        # blockSize % 2 == 1 && blockSize > 1
        self.blockSizeSlider = tk.Scale(
            self,
            **self.sliderArgs,
            label = 'Block Size',
            from_ = 0,
            to = 100,
            command = self.controller.onConfigSliderChange
        )
        self.blockSizeSlider.place(x = 860, y = 60)     
        
        self.constantSlider = tk.Scale(
            self,
            **self.sliderArgs,
            label = 'Constant',
            from_ = 0,
            to = 32,
            command = self.controller.onConfigSliderChange
        )                  
        self.constantSlider.place(x = 1050, y = 60)
        
        self.maxValueSlider.set(225)
        self.blockSizeSlider.set(9)
        self.constantSlider.set(1)
        
        self.openFileButton = tk.Button(self, text = "Upload Image", command = self.controller.openImageFile)
        self.openFileButton.place( x = 700, y = 10)
        
        self.resetButton = tk.Button(
            self,
            text = 'Reset Image',
            command = self.controller.resetCanvasImage
        )
        self.resetButton.place( x = 800, y = 10)
        
        # self.saveButton = tk.Button(
        #     self,
        #     text = 'save',
        #     command = self.convert
        # )
        # self.saveButton.place(x = 900, y = 10)
        
        self.wordInput = tk.Entry(
            self,
            width = 20
        )
        self.wordInput.place( x = 770, y = 500)
      
    def main(self):
        self.mainloop()