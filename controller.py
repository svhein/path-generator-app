from view import View
from model import Model
from tkinter.filedialog import askopenfilename
from PIL import Image,ImageTk, ImageGrab

class Controller():
    def __init__(self):
        self.view = View(self)
        self.model = Model()
        
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
        self._newImg = self.model.get_PIL_Image()
        self.view.canvas.create_image(300,300, image = self._newImg)
        print('canvas slider fired')
        # self.image = self.image.resize((self.x, self.y), Image.ANTIALIAS)
        # self.imgTk = ImageTk.PhotoImage(self.image)
        # self.canvas.create_image(300, 300, image = self.imgTk)
        
    def onConfigSliderChange(self, value):
    
        print('slider change fired')
        maxValue = self.view.maxValueSlider.get()
        blockSize = self.view.blockSizeSlider.get()
        constant = self.view.constantSlider.get()
        self.model.convert_to_grayscale(maxValue, blockSize, constant) 
        self.configImg = self.model.get_PIL_Image()
        self.view.canvas.create_image(300, 300, image = self.configImg)
        
    def resetCanvasImage(self):
        self.view.canvas.delete('all')
        self.model.setImage(self.model.imageOriginal)
        self.view.canvasSlider_X.set(self.model.getWidth())
        self.view.canvasSlider_Y.set(self.model.getHeight())
        self.view.canvas.create_image(300, 300, image = self.model.get_PIL_Image())
              
if __name__ == '__main__':
    app = Controller()
    app.main()