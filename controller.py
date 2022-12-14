from tkinter import RAISED, SUNKEN
from view import View
from model import Model
from simulator import Simulator
from tkinter.filedialog import askopenfilename
from PIL import Image

class Controller():
    def __init__(self):
        self.view = View(self)
        self.model = Model(self.view.showPointsCallback,
                           self.view.filterCallback,
                           self.view.nameInput.get)
        
        self.simulator = Simulator(self.view, self.view.getCanvasSize())
        self.eraserSize = None
    
         
    def main(self):
        self.view.main()
        
    def openImageFile(self):
        pathToImage = askopenfilename(
                filetypes = (
                    [("jpg files", '*.jpg')]
                )
        )
        # scale image to fit the canvas
        img = Image.open(pathToImage)
        self.model.setImage(img)  
        self.model.imageOriginal = img
        self.view.canvasSlider_X.set(self.model.getWidth())
        self.view.canvasSlider_Y.set(self.model.getHeight())
        img = self.model.scale_image()
        # self.save_image()
        self.view.canvas.create_image(300, 300, image = img)    
        print(img.size)
        # self.save_canvas_as_image()
        
    def onCanvasSliderChange(self, value):
        self.model.setWidth(self.view.canvasSlider_X.get())
        self.model.setHeight(self.view.canvasSlider_Y.get())
        self.view.canvas.delete("all")
        self._newImg = self.model.get_Tk_Image()
        self.view.canvas.create_image(300,300, image = self._newImg)
        
    def onConfigSliderChange(self, value):
    
        maxValue = self.view.maxValueSlider.get()
        blockSize = self.view.blockSizeSlider.get()
        constant = self.view.constantSlider.get()
        while not (blockSize % 2 == 1 and blockSize > 1):
            blockSize += 1
        self.view.blockSizeSlider.set(blockSize)
        self.configImg = self.model.convert_to_grayscale(maxValue, blockSize, constant) 
        self.view.canvas.create_image(300, 300, image = self.configImg)
        
    def resetCanvasImage(self):
        self.view.canvas.delete('all')
        self.model.setImage(self.model.imageOriginal)
        self.view.canvasSlider_X.set(self.model.getWidth())
        self.view.canvasSlider_Y.set(self.model.getHeight())
        self.resetImg = self.model.get_Tk_Image()
        self.view.canvas.create_image(300, 300, image = self.resetImg)
        
    def onCalculateButtonPress(self):
        self.model.calculatePath()
        
    def onFilterButtonPress(self):
        threshold, k = self.view.getFilterParams()
        self.model.filter(threshold, k)
        self.view.removeFilteredButton.config(state = 'normal')
        
    def onFilterRemoveButtonPress(self):
        pointsRemovedImg = self.model.removeFilteredPoints()
        self.view.canvas.create_image(300, 300, image = pointsRemovedImg)
        
    def onEraseButtonClick(self):
        self.model.eraseActivated = not bool(self.model.eraseActivated)
        if (self.model.eraseActivated):
            self.view.eraseButton.config(relief = SUNKEN)
        if not (self.model.eraseActivated):
            self.view.eraseButton.config(relief = RAISED)
        pass
    
    def onCanvasClick(self, event):
        if(self.model.eraseActivated):
            erasedImg = self.model.erase(event, self.eraserSize)
            self.view.canvas.create_image(300, 300, image = erasedImg)
            
    def onDatabaseButtonClick(self):
        self.model.sendToDB()
              
    def onRadioButtonClick(self):
        self.eraserSize = self.view.radio.get()
    
    def onSimulateButtonClick(self):
        # self.view.setSimulatorFrame(self.simulator.animation_root)
        self.simulator.simulate()
        
    def onStopSimulationClick(self):
        self.simulator.stopSimulation()
        self.simulator = Simulator(self.view, self.view.getCanvasSize())
    
if __name__ == '__main__':
    app = Controller()
    app.main()