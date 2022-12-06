import tkinter as tk
from tkinter import *
import tkinter.font as TkFont
from tkinter import scrolledtext
import sys
from utils.logger import tkinterLogger

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
        self.CANVASWIDTH = 600
        self.CANVASHEIGHT = 600
        
        self.canvas = Canvas(self, width = self.CANVASWIDTH, height =  self.CANVASHEIGHT, bg = 'white', bd = 0, highlightthickness = 0)
        self.canvas.place(x = 350, rely = 0.5, anchor = CENTER)
        self.circle = None
        
        self.canvas.bind("<Button-1>", self.bindEvent)
        self.canvas.bind('<B1-Motion>', self.bindEvent)
        self.canvas.bind('<Motion>', self.drawCircle)
        
        self.__create_widgets()
        
    def bindEvent(self, event):
        self.controller.onCanvasClick(event)
        self.drawCircle(event)
        
    def drawCircle(self, event, r = 10):
        r = self.radio.get()
        if(self.circle):
            self.canvas.delete(self.circle)
        x, y = event.x, event.y
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        self.circle = self.canvas.create_oval(x0, y0, x1, y1 )
    
    def __create_widgets(self):
        
        # self.canvas = Canvas(self, width = 600, height = 600, bg = 'white', bd = 0, highlightthickness = 0)
        # self.canvas.place(x = 350, rely = 0.5, anchor = CENTER
        
         
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
        
        #FIXME: maxValueSlider not in use
        self.maxValueSlider = tk.Scale(
            self,
            **self.sliderArgs,
            label = 'Max Value',
            from_ = 0,
            to = 255,
            command = self.controller.onConfigSliderChange
        )
        # self.maxValueSlider.place(x = 670, y = 60)
        
        # blockSize % 2 == 1 && blockSize > 1
        self.blockSizeSlider = tk.Scale(
            self,
            **self.sliderArgs,
            label = 'Block Size',
            from_ = 0,
            to = 100,
            command = self.controller.onConfigSliderChange
        )
        self.blockSizeSlider.place(x = 670, y = 60)     
        
        self.constantSlider = tk.Scale(
            self,
            **self.sliderArgs,
            label = 'Constant',
            from_ = 0,
            to = 32,
            command = self.controller.onConfigSliderChange
        )                  
        self.constantSlider.place(x = 670, y = 135)
        
        self.maxValueSlider.set(255)
        self.blockSizeSlider.set(3)
        self.constantSlider.set(1)
        
        self.openFileButton = tk.Button(self, text = "Upload Image", command = self.controller.openImageFile)
        self.openFileButton.place( x = 700, y = 10)
        
        self.resetButton = tk.Button(
            self,
            text = 'Reset Image',
            command = self.controller.resetCanvasImage
        )
        self.resetButton.place( x = 800, y = 10)
        
        self.pointVar = tk.StringVar()
        # self.pointVar.set('testi')
        # self.pointLabel = tk.Label(
        #     self,
        #     textvariable = self.pointVar
        # )
        # self.pointLabel.place(x = 900, y = 200)
        
        filterSizeText = tk.Label(self, text = 'Filter Size:' )
        filterSizeText.place(x = 670, y = 200)
        
        self.filterSizeEntryVar = tk.StringVar()
        self.filterSizeEntryVar.set(2)
        self.filterSizeEntry = tk.Entry(
            self,
            text = self.filterSizeEntryVar,
            width = 3
        )
        self.filterSizeEntry.place(x= 725, y = 202)
        #############################################
        filterKText = tk.Label(self, text = "K:")
        filterKText.place(x = 758, y = 202)
        self.filterKVar = tk.StringVar()
        self.filterKVar.set(2)
        self.filterK_entry = tk.Entry(
            self,
            text = self.filterKVar,
            width = 3
        )
        self.filterK_entry.place(x = 775, y = 202)

        self.calculateButton = tk.Button(
            self,
            text = 'Calculate Path',
            width = 24,
            command = self.controller.onCalculateButtonPress
        )
        self.calculateButton.place(x = 670, y= 305)
        
        self.filterButton = tk.Button(
            self,
            text = 'Filter',
            width = 24,
            command = self.controller.onFilterButtonPress
        )
        self.filterButton.place(x = 670, y= 235)
        
        self.removeFilteredButton = tk.Button(
            self,
            text = "Remove Filtered",
            width = 24,
            state = "disabled",
            command = self.controller.onFilterRemoveButtonPress
        )
        self.removeFilteredButton.place(x = 670, y = 270)
        
        self.eraseButton = tk.Button(
            self,
            text = 'Erase',
            relief = RAISED,
            command = self.controller.onEraseButtonClick
        )
        self.eraseButton.place(x = 150, y = 675)
        
        self.loggingBox = tk.scrolledtext.ScrolledText(
            self,
            height=7,
            width=25 ,
            fg = "white",
            bg = 'black'  
        )
        tkLogger = tkinterLogger(self.loggingBox)
        sys.stdout = tkLogger
        self.loggingBox.place(x = 670, y = 500)
        
        self.dataBaseButton = tk.Button(
            self,
            text = "Send to Database",
            command = self.controller.onDatabaseButtonClick
        )
        self.dataBaseButton.place(x = 670, y = 450)
        
        self.nameInput = tk.Entry(
            self,
            width = 20,
        )
        self.nameInput.place(x = 670, y = 400)
        
        self.radio = tk.IntVar()
        self.radioButtonBig = tk.Radiobutton(
            self,
            text = 'Big',
            variable = self.radio,
            value = 40,
            command = self.controller.onRadioButtonClick
        )
        self.radioButtonBig.place(x=200, y=675)
        self.radioButtonSmall = tk.Radiobutton(
            self,
            text = 'Small',
            variable = self.radio,
            value = 10,
            command = self.controller.onRadioButtonClick
        )
        self.radioButtonSmall.place(x = 225, y = 675)
        
        self.simulateButton = tk.Button(
            self,
            text = 'Simulate',
            command = self.controller.onSimulateButtonClick
        )
        self.simulateButton.place(x = 190, y = 675)
    
    def setSimulatorWindow(self, window):
        window.attributes('-topmost',True)
        simWindow = Label(window)
        simWindow.place(x = 350, rely = 0.5, anchor = CENTER)
        
    def showPointsCallback(self, point):
        self.pointVar.set(point)
        x, y = point[1], point[0]
        self.canvas.create_oval(x, y, x, y, width = 0, fill = 'green')
        self.update()
        
    def filterCallback(self, point: tuple):
        x, y = point[1], point[0]
        self.canvas.create_oval(x, y, x, y, width = 0, fill = 'red')
        
    def getFilterParams(self):
        filterSize = self.filterSizeEntryVar.get()
        k = self.filterKVar.get()
        return int(filterSize), int(k)
    
    def getCanvasSize(self) -> tuple:
        return self.CANVASWIDTH, self.CANVASHEIGHT
      
    def main(self):
        self.mainloop()