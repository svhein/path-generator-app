from PIL import Image,ImageTk
import math
import cv2
import numpy as np
from path_calculator import pathCalculator
import os
import firebase_admin
from scipy.spatial import distance


# NOTE self._image must be handled as PIL.Image object. PIL.ImageTk is returned to controller

class Model():
    def __init__(self, showPointsCallback, filterCallback):
        self.imageOriginal = None
        self._image = None
        self._canvasImage = None
    
        self._width = 1
        self._height = 1
        
        self.eraseActivated = False
        
        self.calculator = pathCalculator(showPointsCallback)
        self.filterCallback = filterCallback
        self._path = None
        
        self._brush_radius = 4
        self._circleAreaPoints = self.__getCircleArea(self._brush_radius)
        
        try:
            cred_obj = firebase_admin.credentials.Certificate("./service_account.json")
            self.firebase = firebase_admin.initialize_app(cred_obj)
            print('Succesfully connected to the database')
        except Exception as e:
            # print(e)
            print('Unable to connect to the database')   
        
        
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
        
    # def filter(self):
    #     image = cv2.imread('canvas.jpg')
    #     dst = cv2.fastNlMeansDenoising(image,None, h=100, templateWindowSize=1, searchWindowSize=5)
    #     cv2.imshow('', dst)
    
    def erase(self, event) -> ImageTk.PhotoImage:
            '''Returns edited canvas image'''
            x, y = event.x, event.y
            cv_image = cv2.imread("canvas.jpg")
            r = 5
            # for i in range (-r , r + 1):
            #     for j in range (-(r-i), r-i):
            #         image[x+i][y+j] = (255, 255, 255)
            for i, j in self._circleAreaPoints:
                cv_image[y + j][x + i] = (255, 255 ,255) #FIXME: coordinates wrong way
            cv2.imwrite('canvas.jpg', cv_image)
            color_coverted = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(color_coverted)
            self.imageTk = ImageTk.PhotoImage(pil_image)
            return self.imageTk
    
    def filter2(self, threshold = 10):
        self._points = list(self.calculator.getPointsToDraw().keys())
        self._points = np.asarray(self._points)
        print(self._points)
        pointsToRemove = []
        for point in self._points:
            print(f'checking point {point}')
            # check distance to closest point:
            x, y = point[0], point[1]
            smallest_distance = distance.cdist([(x, y)], self._points).min()
            print(f'distance {smallest_distance}')
            # if distance above thresshold remove point
            if (smallest_distance > threshold):
                pointsToRemove.append(point)
                self.filterCallback(point)
                #closest_index = distance.cdist([point], self._points).argmin()
                
    def filter(self, threshold_distance: int = 10, k: int = 6):
        print(threshold_distance, k)
        self._points = list(self.calculator.getPointsToDraw().keys())
        # self._points = np.asarray(self._points)
        pointsToRemove = []
        for i in range (len(self._points)):
            point = self._points[i]
            # point can't be in list when the closest point is search
            copy = self._points[:]
            copy.remove(point)
            print(f'checking point {point}')
            x, y = point[0], point[1]
            ## get distances to another points
            distances = distance.cdist([(x,y)], copy).reshape(-1).tolist()
            idxs = np.argpartition(distances, k)[:k] #idxs contains indexes of k nearest points
            # check distance of k nearest point
            # if above theshold remove all points from idxs 0 to k-1
            if (distances[idxs[k-1]] > threshold_distance):
                for i in range (k-1):
                    p = copy[idxs[i]]
                    pointsToRemove.append(p)
                    self.filterCallback(p)
                pointsToRemove.append(point)
                self.filterCallback(point)
                                     
    def __getCircleArea(self, r):
        x0 = 0
        y0 = 0
        coordinates = []
        for i in range(-r , r + 1):
                for j in range(-r, r + 1):
                    if (i - x0)**2 + (j - y0)**2 <= r**2:
                        coordinates.append((i, j))
        return coordinates
    
    def sendToDB(self, path = ""):
        try:
            cred_obj = firebase_admin.credentials.Certificate("./service_account.json")
            self.firebase = firebase_admin.initialize_app(cred_obj)
            print('Succesfully connected to the database')
        except Exception as e:
            # print(e)
            print('Unable to connect to the database')   
             

        
        
                        
        
        
   