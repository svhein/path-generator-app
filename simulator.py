import tkinter as tk
from tkinter import *
import json

class Simulator():
    
    def __init__(self, parent, canvasSize):
    
        self.animation_root = tk.Frame(parent)
        # self.animation_root.title('Sim')
        self.height, self.width = canvasSize[0], canvasSize[1]
        # self.animation_root.geometry('{}x{}'.format(self.height,self.width))
        
        self.animation_canvas = Canvas(self.animation_root, width=self.width, height=self.height,bd=0,highlightthickness=0)
        self.animation_canvas.pack()
        PhotoImage(master = self.animation_root, width = 600, height = 600)
        
        self.background_image = PhotoImage(file="utils/valkoinen.png")
        self.image = self.animation_canvas.create_image(0, 0, anchor=NW, image=self.background_image)
        
        self.animation_root.bind('<s>', self.simulate)
        self.animation_root.bind('<q>', self.stopSimulation)
        # self.animation_root.mainloop()
    
    def simulate(self):
        
        # self.animation_root.pack()
        self.animation_root.place(x = 350, rely = 0.5, anchor = CENTER)
        move = 0
        eka = True
        ekaRivi = False #TODO tämä kai turha nykyään
        # df = pd.read_csv(tiedostoNimi, converters={"rivi":int,"x":int,'y':int,'z':int})
        file = open('pathGenerated.json')
        data = json.load(file)
        
        for object in data:
            
            if (ekaRivi):
                ekaRivi = False
                continue

            # animation_x = row[2]
            # animation_y = row[1]
            # animation_z = row[3]
            animation_x = object['y']
            animation_y = object['x']
            animation_z = object['z']
            
            if (eka == False):
                
                self.animation_canvas.delete(oval,animation_x_text,animation_y_text,animation_z_text,animation_move_text)
                self.animation_canvas.move(animation_xLine,0,animation_y-lastY)
                self.animation_canvas.move(animation_yLine,animation_x-lastX,0)
                oval = self.animation_canvas.create_oval(animation_x + 5 +animation_z, animation_y + 5 +animation_z, animation_x-5-animation_z, animation_y-5-animation_z, fill="purple")
                
                animation_x_text = self.animation_canvas.create_text(self.width-20,10,text="X: {}".format(animation_x), fill="red")
                animation_y_text = self.animation_canvas.create_text(self.width-20,20,text="Y: {}".format(animation_y), fill="blue")
                animation_z_text = self.animation_canvas.create_text(self.width-20,30,text="Z: {}".format(animation_z), fill="medium violet red")
                animation_move_text = self.animation_canvas.create_text(self.width-20,40,text="p {}".format(move), fill="black")
                
                self.animation_canvas.update()   
                
            if (eka):
                animation_yLine = self.animation_canvas.create_line(animation_x, 0, animation_x, self.width, fill="red", width=2)
                animation_xLine = self.animation_canvas.create_line(0, animation_y, self.height, animation_y, fill="blue", width=2)
                animation_x_text = self.animation_canvas.create_text(self.width-20,10,text="X: {}".format(animation_x), fill="red")
                animation_y_text = self.animation_canvas.create_text(self.width-20,20,text="Y: {}".format(animation_y), fill="blue")
                animation_z_text = self.animation_canvas.create_text(self.width-20,30,text="Z: {}".format(animation_z), fill="medium violet red")
                animation_move_text = self.animation_canvas.create_text(self.width-20,40,text="p {}".format(move), fill="black")
                oval = self.animation_canvas.create_oval(animation_x + 5 +animation_z, animation_y + 5 +animation_z,animation_x-5-animation_z, animation_y-5-animation_z, fill="purple")
            if (animation_z == 0):
                self.background_image.put("#%02x%02x%02x" % (0, 0, 0), (animation_x, animation_y))
                move += 1
                 
            print("{},{},{}".format(animation_x,animation_y,animation_z))
            
            lastX = animation_x
            lastY = animation_y
            lastZ = animation_z
        
            eka = False
                 
    def stopSimulation(self):
        self.animation_root.pack_forget()
        self.animation_root.destroy()
            

