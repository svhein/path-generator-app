from PIL import Image,ImageTk
import math
import cv2
import numpy as np

class Model():
    def __init__(self):
        self.imageOriginal = None
        self._image = None
        self._grayScaleImage = None
        
        self._width = 1
        self._height = 1
        
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
        
    def get_PIL_Image(self):
        return ImageTk.PhotoImage(self._image)
    
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
        
        # cv2.imwrite('grayTest.jpg', grayImage)
        # cv2.imwrite('treshholdTest.jpg', imageTH)
    
        pil_image = Image.fromarray(imageTH) 
        self.imageTk = ImageTk.PhotoImage(pil_image)
        self.convertedImg = ImageTk.getimage(self.imageTk)
        self._grayScaleImage = self.convertedImg
        self._image = self.convertedImg
        return self.convertedImg
        

    

        
        

        
        
    
        
    
    