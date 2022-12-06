from PIL import Image,ImageTk
import math
import cv2
import numpy as np
from utils.path_calculator import pathCalculator
import os
import firebase_admin
from firebase_admin import db
from scipy.spatial import distance
import json
import dotenv

# NOTE self._image must be handled as PIL.Image object. PIL.ImageTk is returned to controller

class Model():
    def __init__(self, showPointsCallback, filterCallback, getName):
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
        
        self.getName = getName
        
        try:
            dotenv.load_dotenv()
            database_url = os.getenv('DATABASE_URL')
            print(database_url)
            cred_obj = firebase_admin.credentials.Certificate("./service_account.json")
            self.firebase = firebase_admin.initialize_app(cred_obj, {'databaseURL' : f'{database_url}'})
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
    
    def convert_to_grayscale(self, maxValue, blockSize, constant) -> ImageTk.PhotoImage:
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
        '''Saves path object to self._path variable
        and also in pathGenerated.json in working directory'''
        self._path = self.calculator.calculatePath()
      
    # def erase(self, event) -> ImageTk.PhotoImage:
    #         '''Returns edited canvas image'''
    #         x, y = event.x, event.y
    #         cv_image = cv2.imread("canvas.jpg")
    #         r = 5
    #         for i, j in self._circleAreaPoints:
    #             cv_image[y + j][x + i] = (255, 255 ,255) #FIXME: coordinates wrong way
    #         cv2.imwrite('canvas.jpg', cv_image)
    #         color_coverted = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
    #         pil_image = Image.fromarray(color_coverted)
    #         self.imageTk = ImageTk.PhotoImage(pil_image)
    #         return self.imageTk
    
    def erase(self, event) -> ImageTk.PhotoImage:
        cv_image = cv2.imread('canvas.jpg')
        r = 10
        x, y = event.x, event.y
        cv2.circle(cv_image, (x,y), r, (255, 255, 255), -1)
        cv2.imwrite('canvas.jpg', cv_image)
        color_coverted = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(color_coverted)
        self.imageTk = ImageTk.PhotoImage(pil_image)
        return self.imageTk
        
                        
    def filter(self, threshold_radius: int = 10, k: int = 6):
        '''
        itares through every point and checks how many points are near it   
        Args: 
            threshold_radius: Radius of circle where points are searched'
            k: Number of points required to be in the circle'
        '''
        self._points = list(self.calculator.getPointsToDraw().keys())
        self._pointsToRemove = []
        for i in range (len(self._points)):
            point = self._points[i]
            # point can't be in list when the closest point is search
            copy = self._points[:]
            copy.remove(point)
            x, y = point[0], point[1]
            ## get distances to another points
            distances = distance.cdist([(x,y)], copy).reshape(-1).tolist()
            idxs = np.argpartition(distances, k)[:k] #idxs contains indexes of k nearest points
            # check distance of farthest point
            # if above theshold remove all points from idxs 0 to k-1
            if (distances[idxs[k-1]] > threshold_radius):
                for i in range (k-1):
                    p = copy[idxs[i]]
                    self._pointsToRemove.append(p)
                    self.filterCallback(p)
                self._pointsToRemove.append(point)
                self.filterCallback(point)
        if len(self._pointsToRemove) != 0:
            pass
        
    def removeFilteredPoints(self) -> ImageTk.PhotoImage:
        '''Removes points from canvas.jpg, returns edited photo'''
        cv_image = cv2.imread("canvas.jpg")
        for point in self._pointsToRemove:
            x, y = point[0], point[1]    
            print('removing point',x,y)
            cv_image[x][y] = (255, 255 ,255) #FIXME: coordinates wrong way
        cv2.imwrite('canvas.jpg', cv_image)
        color_coverted = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(color_coverted)
        self.imageTk = ImageTk.PhotoImage(pil_image)
        return self.imageTk
                                     
    def __getCircleArea(self, r):
        x0 = 0
        y0 = 0
        coordinates = []
        for i in range(-r , r + 1):
                for j in range(-r, r + 1):
                    if (i - x0)**2 + (j - y0)**2 <= r**2:
                        coordinates.append((i, j))
        return coordinates
    
    def sendToDB(self):
        name = self.getName()
        if(name):
            try:
                self.__compileJson()
                db_ref = db.reference(f"/Paths/{name}")
                with open('compiled.json', "r") as f:
                    content = json.load(f)
                db_ref.set(content)
                print('Work succesfully send to database')
                
            except Exception as e:
                print(e)
                print('Failed to send data')   
        else:
            print('Give picture name')
    
    def __compileJson(self):
        '''Creates json in working directory to be sent in to database'''
        word = self.getName()
        letters = list(word)
            
        with open('pathGenerated.json', "r") as f:
            path = json.load(f)
            dict = {
                'word' : word,
                'letters' : letters,
                'path' : path
            }
            object = json.dumps(dict, indent=4)
            with open('compiled.json', 'w') as file:
                file.write(object)