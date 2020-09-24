import tkinter as tk
from tkinter import ttk 
from tkinter import PhotoImage
import cv2
from PIL import ImageGrab
import PIL.Image, PIL.ImageTk
from PIL import Image
import numpy as np
import math
import serial
import serial.tools.list_ports
import time
import pyautogui
import pytesseract

class InteractiveScreenshot(tk.Frame):
    def __init__( self, parent):
        parent.title("Interactive Screenshot");
        parent.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
        parent.attributes('-alpha', 0.3)
        parent.attributes("-fullscreen", True)
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

    def screenshotEditor(self): 
        global previewScreenshotImg

        self.parent.withdraw() 
        self.parent.destroy()
        self.selectionDone()
        self.ScreenshotEditorWm = tk.Toplevel() 
        self.ocr = tk.IntVar()
        self.ocr.set("1")

        self.threshControl = tk.IntVar()
        self.maxValueControl = tk.IntVar()
        self.blurControl = tk.IntVar()

        self.threshControl.set("100")
        self.maxValueControl.set("250")
        self.blurControl.set("100")

        # Toplevel widget 
        self.ScreenshotEditorWm.title("Editor") 
  
        self.ScreenshotEditorWm.resizable(False, False)
        self.screenshotPreviewCanv= tk.Canvas(self.ScreenshotEditorWm,height=220,width = 220,bg = "black")
        self.screenshotPreviewCanv.grid(padx = 5,row=0,rowspan=4,columnspan=2, column=0,sticky="EW")
        previewScreenshotImg = PIL.ImageTk.PhotoImage(self.EditorImg())
        self.image_label = tk.Label(self.screenshotPreviewCanv, image=previewScreenshotImg)
        self.image_label.pack(anchor=tk.CENTER,fill = tk.BOTH)
        
        self.ScreenshotEditorWm.deiconify() 

        tresh_horizontal_slider_w = tk.Scale(self.ScreenshotEditorWm,from_=0,to=300,orient = tk.HORIZONTAL,variable=self.threshControl,command=self.imageAdjustment)
        tresh_horizontal_slider_b = tk.Scale(self.ScreenshotEditorWm,from_=0,to=300,orient = tk.HORIZONTAL, variable=self.maxValueControl,command=self.imageAdjustment)
        blur_horizontal_slider = tk.Scale(self.ScreenshotEditorWm,from_=0,to=300,orient = tk.HORIZONTAL, variable=self.blurControl,command=self.imageAdjustment)
        
        tresh_horizontal_slider_w.grid(padx = 5,row=0,column=3,sticky="EW",)
        tresh_horizontal_slider_b.grid(padx = 5,row=1,column=3,sticky="EW")
        blur_horizontal_slider.grid(padx = 5,row=2,column=3,sticky="EW")

        tk.Radiobutton(self.ScreenshotEditorWm,text="Health Value",variable=self.ocr,value=1,command=self.radioBUttonSelection).grid(padx = 5,row=4,column=0,sticky="EW")
        tk.Radiobutton(self.ScreenshotEditorWm,text="Health Bar",variable=self.ocr,value=2,command=self.radioBUttonSelection).grid(padx = 5,row=4,column=1,sticky="EW")

        tk.Button(self.ScreenshotEditorWm,text="Save",command=self.saveProcessedImg).grid(padx = 5,pady=5,row=4,column=3,sticky="EW")
        
    def saveProcessedImg(self):
        global gray_image
        processedImg =  PIL.Image.fromarray(gray_image)
        processedImg.save("./images/processed/screenshot.png")

    def EditorImg(self):
        screenshotOriginal =  PIL.Image.fromarray(gray_image)
        screenshotOriginal.thumbnail((220,220))
        resized =  screenshotOriginal
        return resized

    def imageProcessingPreview(self):
        global previewScreenshotImg
        previewScreenshotImg = PIL.ImageTk.PhotoImage(self.EditorImg())
        self.image_label.config(image=previewScreenshotImg)        

    def imageAdjustment(self,var):
        global gray_image
        gray_image = cv2.cvtColor(np.array(PIL.Image.open("./images/original/screenshot.png")), cv2.COLOR_BGR2GRAY) 
        #blur the gray image to remove noise and to averaging the color
        blurred = cv2.bilateralFilter(gray_image,15,self.blurControl.get(),self.blurControl.get())
        #converting the blurred image to pure black(0) and white(255) binary image
        thresh = cv2.threshold(blurred,self.threshControl.get(),self.maxValueControl.get(), cv2.THRESH_BINARY)[1]
        #cv2.imshow('Original',thresh)
        gray_image = thresh
        self.imageProcessingPreview()
        

    def radioBUttonSelection(self):
        if self.ocr.get() == 1:
            # print(pytesseract.image_to_string(thresh))
            print("OCR")
        else:
            print("Health Bar")
       

    def selectionDone(self):
        global gray_image
        # print('started at x = {1} y = {2} ended at x1 = {3} y1 = {4} '. format(self.rectid, self.rectx0, self.recty0, self.rectx1,
        #              self.recty1))
        # '''Getting the Image from the screen and find the edge of the health bar'''
        # print(pyautogui.position())
	    #Grabbing the image from screen using pillow library
	    #converting the image to numpy array to use the image with cv2 library
        capture = ImageGrab.grab(bbox = (self.rectx0-0.5,self.recty0+26,self.rectx1,self.recty1+26.5))
        screen = np.array(capture)
        capture.save('./images/original/screenshot.png')
        cvt_image = cv2.cvtColor(screen,cv2.COLOR_BGR2RGB)
        gray_image = cv2.cvtColor(cvt_image, cv2.COLOR_BGR2GRAY)
       

    def exitScreenshot(self):
        self.parent.destroy()

    def _createCanvas(self):
        self.canvas = tk.Canvas(self.parent, width = root.winfo_screenwidth(), height = root.winfo_screenheight(),
                                bg = None,cursor="crosshair")
        #self.canvas.grid(row=0, column=0)
        self.mainScreenButton = tk.Button(self.parent, text="Exit", width=10, command=self.exitScreenshot,bg='#ff0000',fg='black')
        self.screenshotButton = tk.Button(self.parent, text="Grab", width=10, command=self.screenshotEditor,bg='#00ff00',fg='black')
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
       
    def movingRect(self, event):
        #Translate mouse screen x1,y1 coordinates to canvas coordinates
        self.rectx1 = self.canvas.canvasx(event.x)
        self.recty1 = self.canvas.canvasy(event.y)
        #Modify rectangle x1, y1 coordinates
        self.canvas.coords(self.rectid, self.rectx0, self.recty0,
                      self.rectx1, self.recty1)
        # print('Rectangle x1, y1 = ', self.rectx1, self.recty1)

    def stopRect(self, event):
        #Translate mouse screen x1,y1 coordinates to canvas coordinates
        self.rectx1 = self.canvas.canvasx(event.x)
        self.recty1 = self.canvas.canvasy(event.y)
        #Modify rectangle x1, y1 coordinates
        self.canvas.coords(self.rectid, self.rectx0, self.recty0,
                      self.rectx1, self.recty1)
        # print('Rectangle ended')
        # print(pyautogui.position())

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
    # print('Serial searching')
    result = []
    for port, desc, hwid in sorted(ports):
        # print("{}: {} [{}]".format(port, desc, hwid))
        result.append(desc)
    return result

def refreshPorts():
    comList = serial_ports()
    if not comList:
        comList.append("No device")
    com['values'] = comList
    com.current(0)

def newScreenArea():
    #pyautogui.getWindowsWithTitle("Gamer Assist")[0].minimize()
    root.wm_state('iconic')
    screenshotWindow = tk.Toplevel(root)
    app = InteractiveScreenshot(screenshotWindow)



if __name__ == "__main__":
    
    pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract'
    cvt_image = None

    baduRate = ["9600","115200","19200"]

    root = tk.Tk()
    root.title("Gamer Assist")
    root.geometry("322x290")
    root.resizable(False, False)

    # Adding Menu system
    menu_system = tk.Menu(root)
    root.config(menu=menu_system)

    #creating file menu item
    file_menu = tk.Menu(menu_system,tearoff=False)
    menu_system.add_cascade(label="File",menu=file_menu)
    file_menu.add_command(label="New Config",command=None)
    file_menu.add_command(label="Open Config",command=None)
    file_menu.add_command(label="Save Config",command=None)
    file_menu.add_separator()
    file_menu.add_command(label="Exit",command=root.quit)

    #creating help menu item
    help_menu = tk.Menu(menu_system,tearoff=False)
    menu_system.add_cascade(label="Help",menu=help_menu)
    help_menu.add_command(label="Manual",command=None)
    help_menu.add_command(label="About",command=None)


    imageCanvas = tk.Canvas(root,height=220,width = 220,bg = "black")
    imageCanvas.grid(padx = 5,row=0,rowspan=3,columnspan=2, column=0,sticky="W")

    originalImg = Image.open('images/Health.png')

    imgWidth,imgHeight = originalImg.size
    imageCanvas.update()
    newHeight = imageCanvas.winfo_height()
    
    if imgWidth <= imgHeight:
        newWidth = int(imageCanvas.winfo_height() / imgHeight * imgWidth) 
    else:
        newWidth = imageCanvas.winfo_width()
        newHeight = int((newWidth/imgWidth)*imgHeight)

    resized = originalImg.resize((newWidth,newHeight))
    previewScreenshot = PIL.ImageTk.PhotoImage(resized)
   
    imageCanvas.create_image(((220-newWidth)/2),((220-newHeight)/2),image=previewScreenshot,anchor='nw')

    tk.Button(root, text="Start", width=10, command=None).grid(padx = 5,pady = 5,row=0, column=2,sticky="NS")
    tk.Button(root, text="Stop", width=10, command=None).grid(padx = 5,pady = 5, row=1, column=2,sticky="NS")
    tk.Button(root, text="Edit Config", width=10, command=newScreenArea).grid(padx = 5,pady = 5, row=2, column=2,sticky="NS")

    tk.Label(root, text="Badu Rate:").grid(padx = 5,pady = 5, row=3, column=0, sticky='NW')
    
    badu = ttk.Combobox(root,value = baduRate)
    badu.grid(padx = 0,pady = 5, row=3, column=1)
    badu.current(0)
    badu.bind("<<ComboboxSelected>>",None)
    
    tk.Label(root, text="Port:").grid(padx = 5,pady = 5, row=4, column=0, sticky='NW')

    comList = serial_ports()
    if not comList:
        comList.append("No device")
    com = ttk.Combobox(root,value = comList)
    com.grid(padx = 5,pady = 5, row=4, column=1)
    com.current(0)
    com.bind("<<ComboboxSelected>>",None)

    tk.Button(root, text="Refresh Port", width=10, command=refreshPorts).grid(padx = 5,pady = 5, row=4, column=2)

    root.mainloop()
    