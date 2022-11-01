from colorsys import yiq_to_rgb
import cv2
import numpy as np
from scipy import spatial
from math import sqrt
import json

class pathCalculator:
    def __init__(self, showPointsCallback):
        # self.filename = filename
        # self.img = cv2.imread(filename)
        # self.width, self.height = self.img.shape[:2]
        # print(f'width: {self.width} height: {self.height}') 
        self.pointsToDraw = []
        self.dict = {}
        self.pathJson = []
        self.showPointsCallback = showPointsCallback
        
    def __findPointsToDraw(self):
        
        if not (self.width):
            self.img = cv2.imread('canvas.jpg')
            self.width, self.height = self.img.shape[:2]
        
        for x in range(0, self.width - 1 , 1):
            for y in range (0, self.height - 1, 1):
                pixel = self.img[x, y]           ## arvo joko 0 0 0 tai 255 255 255 joten eka arvo riittää
                if (pixel[0] < 150):
                    self.pointsToDraw.append((x, y))
                    self.dict[(x,y)] = 1
        
    def __findClosestPoint(self, x, y):
        closestDistance = 10000 
        closestPoint = (600,600)
        # print(f'finding closest point ({x},{y})')
        for point in self.pointsToDraw:
            distance = sqrt(((x - point[0])**2) + ((y - point[1])**2))
            if (distance < closestDistance):
                closestPoint = point
                closestDistance = distance
        # print('find closest point done')
        self.pointsToDraw.remove(closestPoint)
        return closestPoint 
    
    #apufunktio
    def __AddPathBetweenPoints(self, x_old, y_old, z_old, x, y, z):
        # print('calculating path between points...')
        cordsList = []
    
        memory_x = x_old
        memory_y = y_old
        memory_z = z_old
        
        while (memory_x != x or memory_y != y or memory_z != z):
            
            if (memory_x < x): dx = 1 
            if (memory_x == x): dx = 0
            if (memory_x > x): dx = -1
            
            if (memory_y < y): dy = 1 
            if (memory_y == y): dy = 0
            if (memory_y > y): dy = -1
            
            if (memory_z < z): dz = 1 
            if (memory_z == z): dz = 0
            if (memory_z > z): dz = -1
            
            memory_x = memory_x + dx
            memory_y = memory_y + dy
            memory_z = memory_z + dz
            
            # cordsList.append([memory_x,memory_y,memory_z])
            obj = {"x": memory_x,
                   "y": memory_y,
                   "z": memory_z}
            self.pathJson.append(obj)
            # print(f'({memory_x},{memory_y},{memory_z})')
            # print(f'coordinates added: ({memory_x},{memory_y},{memory_z})')
        pass
     
    def calculatePath(self) -> list:
        '''returns path in list of objects (each object is coordinate)'''
        self.__filename = 'canvas.jpg'
        self.img = cv2.imread(self.__filename)
        self.width, self.height = self.img.shape[:2]
       
        self.__findPointsToDraw()
        lastX, lastY, lastZ = 0, 0, 0
        i = 0
 
        while(len(self.pointsToDraw) > 0):
            # print(len(self.pointsToDraw))
            p = self.__findClosestPoint(lastX, lastY)
            x, y = p[0], p[1]
            
            if (x+1 == lastX or x-1 == lastX or y+1 == lastY or y-1 == lastY):
                z = 0
                self.__AddPathBetweenPoints(lastX,lastY,lastZ,x,y,z)
                lastZ = z
                i += 1
            else:
                self.__AddPathBetweenPoints(lastX,lastY,lastZ,x,y,10)
                self.__AddPathBetweenPoints(x,y,10,x,y,0)
                i += 1
            self.showPointsCallback((x, y))
            print(i)
            lastX = x
            lastY = y
            
        # with open('dict_test.json', 'w') as f:
        #     json.dump(self.dict, f, indent = 1)
          
        # askFileName = input('nimi tiedostolle: ')
        with open('testiii.json', 'w') as file:
            json.dump(self.pathJson, file, indent=1)    
            
        return self.pathJson
    
    
    def getPointsToDraw(self) -> dict:
        '''return dictionary of which keys are coordinates of drawable points on the canvas'''
        self.__findPointsToDraw()
        return self.dict
            
# import time
# start = time.time()

# calculator = pathCalculator(showPointsCallback=None)
# calculator.calculatePath()

# end = time.time()

# print(end-start)
