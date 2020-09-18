import tkinter as tk
from tkinter import ttk 
import cv2
from PIL import ImageGrab
import numpy as np
import math
import serial
import serial.tools.list_ports
import time
import pyautogui

class InteractiveScreenshot(tk.Frame):
    def __init__( self, parent):
        tk.Frame.__init__(self, parent)
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.end_fullscreen)
        # self.screenshotButton = tk.Button(root, text="Add folder", width=10, command=None)
        self._createVariables(parent)
        self._createCanvas()
        self._createCanvasBinding()      

    def _createVariables(self, parent):
        self.parent = parent
        self.rectx0 = 0
        self.recty0 = 0
        self.rectx1 = 0
        self.recty1 = 0
        self.rectid = None

    def openNewWindow(self): 
        # Toplevel object which will  
        # be treated as a new window 
        self.newWindow = tk.Toplevel() 
  
        # sets the title of the 
        # Toplevel widget 
        self.newWindow.title("New Window") 
  
        # sets the geometry of toplevel 
        self.newWindow.geometry("200x200") 
  
        # A Label widget to show in toplevel 
        self.Label(self.newWindow,text ="This is a new window").pack() 
        self.parent.destroy()


    def selectionDone(self):
        print('started at x = {1} y = {2} ended at x1 = {3} y1 = {4} '. format(self.rectid, self.rectx0, self.recty0, self.rectx1,
                     self.recty1))
        '''Getting the Image from the screen and find the edge of the health bar'''
        print(pyautogui.position())
	    #Grabbing the image from screen using pillow library
	    #converting the image to numpy array to use the image with cv2 library
        screen = np.array(ImageGrab.grab(bbox = (self.rectx0-0.5,self.recty0+26,self.rectx1,self.recty1+26.5)))
        cvt_image = cv2.cvtColor(screen,cv2.COLOR_BGR2RGB)
	    #using open cv2 to gray out the image grab
        gray_image = cv2.cvtColor(cvt_image, cv2.COLOR_BGR2GRAY)

        #blur the gray image to remove noise and to averaging the color
        blurred = cv2.bilateralFilter(gray_image,15,65,65)
    	#displaying the edge and thresh image
        cv2.imshow('Original',cvt_image)

    def _createCanvas(self):
        self.canvas = tk.Canvas(self.parent, width = root.winfo_screenwidth(), height = root.winfo_screenheight(),
                                bg = None)
        #self.canvas.grid(row=0, column=0)
        self.mainScreenButton = tk.Button(root, text="Main Menu", width=10, command=self.quit(),bg='#00ffea',fg='black')
        self.screenshotButton = tk.Button(root, text="Grab", width=10, command=self.openNewWindow,bg='#00ff08',fg='black')
        #self.button.grid(padx = 50,pady=50,row=2, column=1)
        self.screenshotButton.grid(padx = 5,row=0, column=1, sticky='E')
        self.mainScreenButton.grid(padx = 5,row=0, column=0, sticky= 'W')
        self.canvas.grid(row=1,  columnspan = 2,column=0)
        
    def _createCanvasBinding(self):
        self.canvas.bind( "<Button-1>", self.startRect )
        self.canvas.bind( "<ButtonRelease-1>", self.stopRect )
        self.canvas.bind( "<B1-Motion>", self.movingRect )

    def startRect(self, event):
        #Translate mouse screen x0,y0 coordinates to canvas coordinates
        self.rectx0 = self.canvas.canvasx(event.x)
        self.recty0 = self.canvas.canvasy(event.y) 
        self.canvas.delete("all")
        #Create rectangle

        self.rectid = self.canvas.create_rectangle(
            self.rectx0, self.recty0, self.rectx0, self.recty0, fill="#4eccde")
        # print('Rectangle {0} started at {1} {2} {3} {4} '.
        #       format(self.rectid, self.rectx0, self.recty0, self.rectx0,
        #              self.recty0))

    def movingRect(self, event):
        #Translate mouse screen x1,y1 coordinates to canvas coordinates
        self.rectx1 = self.canvas.canvasx(event.x)
        self.recty1 = self.canvas.canvasy(event.y)
        #Modify rectangle x1, y1 coordinates
        self.canvas.coords(self.rectid, self.rectx0, self.recty0,
                      self.rectx1, self.recty1)
        print('Rectangle x1, y1 = ', self.rectx1, self.recty1)

    def stopRect(self, event):
        #Translate mouse screen x1,y1 coordinates to canvas coordinates
        self.rectx1 = self.canvas.canvasx(event.x)
        self.recty1 = self.canvas.canvasy(event.y)
        #Modify rectangle x1, y1 coordinates
        self.canvas.coords(self.rectid, self.rectx0, self.recty0,
                      self.rectx1, self.recty1)
        print('Rectangle ended')
        print(pyautogui.position())

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"

def  Image_processing():
    	pass

def serial_ports():
    ports = serial.tools.list_ports.comports()
    print('Serial searching')
    result = []
    for port, desc, hwid in sorted(ports):
        print("{}: {} [{}]".format(port, desc, hwid))
        result.append(desc)
    return result

def refreshPorts():
    comList = serial_ports()
    if not comList:
        comList.append("No device")
    com['values'] = comList
    com.current(0)


if __name__ == "__main__":

    baduRate = ["9600","115200","19200"]

    root = tk.Tk()
    #root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    #root.attributes('-alpha', 0.3)
    #root.attributes("-fullscreen", True)
    #app = InteractiveScreenshot(root)
    root.title("Gamer Assist");
    root.geometry("315x175");

    # Adding Menu system
    menu_system = tk.Menu(root)
    root.config(menu=menu_system)

    #creating file menu item
    file_menu = tk.Menu(menu_system)
    menu_system.add_cascade(label="File",menu=file_menu)
    file_menu.add_command(label="New Config",command=None)
    file_menu.add_command(label="Open Config",command=None)
    file_menu.add_command(label="Save Config",command=None)
    file_menu.add_separator()
    file_menu.add_command(label="Exit",command=root.quit)

    #creating help menu item
    help_menu = tk.Menu(menu_system)
    menu_system.add_cascade(label="Help",menu=help_menu)
    help_menu.add_command(label="Manual",command=None)
    help_menu.add_command(label="About",command=None)


    tk.Canvas(root,height=100,width = 50,bg = "White").grid(padx = 5,row=0,rowspan=3,columnspan=2, column=0,sticky="EW")

    tk.Button(root, text="Start", width=10, command=None).grid(padx = 5,pady = 5,row=0, column=2)
    tk.Button(root, text="Stop", width=10, command=None).grid(padx = 5,pady = 5, row=1, column=2)
    tk.Button(root, text="Config file", width=10, command=None).grid(padx = 5,pady = 5, row=2, column=2)

    label = tk.Label(root, text="Badu Rate:").grid(padx = 5,pady = 5, row=3, column=0, sticky='NW')
    
    badu = ttk.Combobox(root,value = baduRate)
    badu.grid(padx = 0,pady = 5, row=3, column=1)
    badu.current(0)
    badu.bind("<<ComboboxSelected>>",None)
    
    label = tk.Label(root, text="Port:").grid(padx = 5,pady = 5, row=4, column=0, sticky='NW')

    comList = serial_ports()
    if not comList:
        comList.append("No device")
    com = ttk.Combobox(root,value = comList)
    com.grid(padx = 5,pady = 5, row=4, column=1)
    com.current(0)
    com.bind("<<ComboboxSelected>>",None)

    tk.Button(root, text="Refresh Port", width=10, command=refreshPorts).grid(padx = 5,pady = 5, row=4, column=2)
    root.mainloop()
    