from PIL import Image,ImageTk
import math
import cv2
import numpy as np
from path_calculator import pathCalculator
import os


# NOTE self._image must be handled as PIL.Image object. PIL.ImageTk is returned to controller

class Model():
    def __init__(self, showPointsCallback, filterCallback):
        self.imageOriginal = None
        self._image = None
        self._canvasImage = None
    
        self._width = 1
        self._height = 1
        
        self.calculator = pathCalculator(showPointsCallback)
        self.filterCallback = filterCallback
        self._path = None
        
    def setWidth(self, width):
        self._width = width
        self._image = self._image.resize((self._width, self._height), Image.ANTIALIAS)
        print(self._image.size)
              
    def setHeight(self, height):
        self._height = height
        self._image = self._image.resize((self._width, self._height), Image.ANTIALIAS)
        
    def getWidth(self):
        return self._width
        
    def getHeight(self):
        return self._height
        
    def get_Tk_Image(self):
        return ImageTk.PhotoImage(self._image)
    
    def get_canvas(self):
        if (self._canvasImage):
           return self._canvasImage 
        raise Exception("Canvas is empty")
        
    
    def setImage(self, img):
        self._image = img
        self._width, self._height = self._image.size
        
    # function optimazes picture size when first downloaded
    def scale_image(self):
        width, height = self._image.size
        # print('scaling; width: height: ' + str(width) + " " + str(height))
        if (width > 600):
            ratio = 600 / width
            width = 600
            height = math.floor(height * ratio)
            self._width, self._height = width, height
            self._image = self._image.resize((width, height), Image.ANTIALIAS)
            return self._image
        elif(height > 600):
            ratio = 600 / height
            height = 600
            width = math.floor(height * ratio)
            self._image = self._image.resize((width, height), Image.ANTIALIAS)
            self._width, self._height = width, height
            return self._image
        return self._image
    
    def convert_to_grayscale(self, maxValue, blockSize, constant):
        image = np.asarray(self._image)
        # image = cv2.imread('canvasImage.jpg')
        # cv2.resize(image, (self._width, self._height))
        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        imageTH = cv2.adaptiveThreshold(
                                        grayImage,
                                        maxValue,
                                        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        \
                                        cv2.THRESH_BINARY,
                                        blockSize,
                                        constant)
    
        self.pil_image = Image.fromarray(imageTH) 
        self.imageTk = ImageTk.PhotoImage(self.pil_image)
        self._canvasImage = self.imageTk
        # self.convertedImg = ImageTk.getimage(self.imageTk)
        self.save_image_jpg(self._canvasImage)
        return self.imageTk
    
    def save_image_jpg(self, image):
        img = ImageTk.getimage(image)
        img = img.convert('RGB') # discard alpha channel
        fileName = 'canvas.jpg'
        img.save(os.path.join(os.getcwd(), fileName), 'JPEG')
        img.close()
        
    def calculatePath(self):
        self._path = self.calculator.calculatePath()
        
    def filter(self):
        self._points = self.calculator.getPointsToDraw()
        factor = 3
        
        def iterateDict():
            for point in self._points.copy():
                x, y = point[0], point[1]
                for i in range(-factor, factor + 1):
                    for j in range(-factor, factor + 1):
                        if (x + i, y + j) in self._points:
                            print(f'found point {x+i} {y+j} near point {x} {y} ...continue')
                            self._points.pop((x + i, y + j))
                            iterateDict()
                        
        iterateDict()
        print('filter done, points left')
        print(self._points)
        for point in self._points:
            self.filterCallback(point)
                        
  
                
        

        
    