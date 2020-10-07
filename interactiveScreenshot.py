import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import PhotoImage
import cv2
from PIL import ImageGrab
import PIL.Image
import PIL.ImageTk
from PIL import Image
import numpy as np
import pyautogui
import pytesseract
import healthBarCalculator


class IS(tk.Frame):
    def __init__(self, parent, superparent):
        self.superparent = superparent
        parent.title("Interactive Screenshot")
        parent.geometry(
            "{0}x{1}+0+0".format(self.superparent.winfo_screenwidth(), self.superparent.winfo_screenheight()))
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
        self.edgeAdjust1 = tk.IntVar()
        self.edgeAdjust2 = tk.IntVar()

        self.threshControl.set("100")
        self.maxValueControl.set("250")
        self.blurControl.set("100")

        # Toplevel widget
        self.ScreenshotEditorWm.title("Editor")

        #self.ScreenshotEditorWm.resizable(False, False)
        self.screenshotPreviewCanv = tk.Canvas(
            self.ScreenshotEditorWm, height=220, width=220, bg="black")
        self.screenshotPreviewCanv.grid(
            padx=5, row=0, rowspan=4, columnspan=2, column=0, sticky="EW")
        previewScreenshotImg = PIL.ImageTk.PhotoImage(self.EditorImg())
        self.image_label = tk.Label(
            self.screenshotPreviewCanv, image=previewScreenshotImg)
        self.image_label.pack(anchor=tk.CENTER, fill=tk.BOTH)

        self.ScreenshotEditorWm.deiconify()

        tresh_horizontal_slider_w = tk.Scale(self.ScreenshotEditorWm, from_=0, to=300,
                                             orient=tk.HORIZONTAL, variable=self.threshControl, command=self.imageAdjustment)
        tresh_horizontal_slider_b = tk.Scale(self.ScreenshotEditorWm, from_=0, to=300,
                                             orient=tk.HORIZONTAL, variable=self.maxValueControl, command=self.imageAdjustment)
        blur_horizontal_slider = tk.Scale(self.ScreenshotEditorWm, from_=0, to=300,
                                          orient=tk.HORIZONTAL, variable=self.blurControl, command=self.imageAdjustment)

        tresh_horizontal_slider_w.grid(padx=5, row=0, column=3, sticky="EW",)
        tresh_horizontal_slider_b.grid(padx=5, row=1, column=3, sticky="EW")
        blur_horizontal_slider.grid(padx=5, row=2, column=3, sticky="EW")
        tk.Radiobutton(self.ScreenshotEditorWm, text="Health Value", variable=self.ocr, value=1,
                       command=self.radioBUttonSelection).grid(padx=5, row=5, column=0, sticky="EW")
        tk.Radiobutton(self.ScreenshotEditorWm, text="Health Bar", variable=self.ocr, value=2,
                       command=self.radioBUttonSelection).grid(padx=5, row=5, column=1, sticky="EW")

        tk.Button(self.ScreenshotEditorWm, text="Save", command=self.saveProcessedImg).grid(
            padx=5, pady=5, row=5, column=3, sticky="EW")

    def saveProcessedImg(self):
        global gray_image
        self.imageAdjustment(None)
        processedImg = PIL.Image.fromarray(gray_image)
        current_dir_path = os.path.dirname(
            os.path.realpath(__file__))

        dialog = filedialog.asksaveasfile(
            initialdir=current_dir_path + "/data", mode='w', defaultextension=".csv", filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
        if dialog is None:  # asksaveasfile return `None` if dialog closed with "cancel".
            return

        dialog.write("{0},{1},{2},{3},{4},{5},{6},{7}".format(int(
            self.rectx0-0.5), int(self.recty0+26), int(self.rectx1), int(self.recty1+26.5), self.threshControl.get(),
            self.maxValueControl.get(), self.blurControl.get(), self.ocr.get()),)
        dialog.close()

        filename = os.path.basename(dialog.name)[:-4]
        processSaveImgDir = "./images/processed/" + filename+".png"
        processedImg.save(processSaveImgDir)

        originalSaveImgDir = "./images/original/temp.png"
        renamePath = "./images/original/" + filename + ".png"
        os.rename(originalSaveImgDir, renamePath)
        # with open('./data/pos.csv', 'w') as file:
        #     file.write("{0},{1},{2},{3},{4},{5},{6}".format(int(
        #         self.rectx0-0.5), int(self.recty0+26), int(self.rectx1), int(self.recty1+26.5), self.threshControl.get(),
        #         self.maxValueControl.get(), self.blurControl.get()))
        #     file.close()

    def EditorImg(self):
        screenshotOriginal = PIL.Image.fromarray(gray_image)
        screenshotOriginal.thumbnail((220, 220))
        resized = screenshotOriginal
        return resized

    def imageProcessingPreview(self):
        global previewScreenshotImg
        previewScreenshotImg = PIL.ImageTk.PhotoImage(self.EditorImg())
        self.image_label.config(image=previewScreenshotImg)

    def imageAdjustment(self, var):
        global gray_image
        gray_image = cv2.cvtColor(np.array(PIL.Image.open(
            "./images/original/temp.png")), cv2.COLOR_BGR2GRAY)
        # blur the gray image to remove noise and to averaging the color
        blurred = cv2.bilateralFilter(
            gray_image, 15, self.blurControl.get(), self.blurControl.get())
        # converting the blurred image to pure black(0) and white(255) binary image
        thresh = cv2.threshold(blurred, self.threshControl.get(
        ), self.maxValueControl.get(), cv2.THRESH_BINARY)[1]
        # cv2.imshow('Original',thresh)
        if self.ocr.get() == 2:
            thresh = cv2.Canny(thresh, 100, 150)
        gray_image = thresh
        self.imageProcessingPreview()

    def radioBUttonSelection(self):
        if self.ocr.get() == 1:
            # print(pytesseract.image_to_string(thresh))
            print("OCR")
            self.imageAdjustment(None)

        else:
            print("Health Bar")
            self.imageAdjustment(None)

    def selectionDone(self):
        global gray_image
        capture = ImageGrab.grab(
            bbox=(self.rectx0-0.5, self.recty0+26, self.rectx1, self.recty1+26.5))
        screen = np.array(capture)
        capture.save('./images/original/temp.png')
        cvt_image = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
        gray_image = cv2.cvtColor(cvt_image, cv2.COLOR_BGR2GRAY)

    def exitScreenshot(self):
        self.parent.destroy()

    def _createCanvas(self):
        self.canvas = tk.Canvas(self.parent, width=self.superparent.winfo_screenwidth(), height=self.superparent.winfo_screenheight(),
                                bg=None, cursor="crosshair")
        # self.canvas.grid(row=0, column=0)
        self.mainScreenButton = tk.Button(
            self.parent, text="Exit", width=10, command=self.exitScreenshot, bg='#ff0000', fg='black')
        self.screenshotButton = tk.Button(
            self.parent, text="Grab", width=10, command=self.screenshotEditor, bg='#00ff00', fg='black')
        # self.button.grid(padx = 50,pady=50,row=2, column=1)
        self.screenshotButton.grid(padx=5, row=0, column=1, sticky='E')
        self.mainScreenButton.grid(padx=5, row=0, column=0, sticky='W')
        self.canvas.grid(row=1,  columnspan=2, column=0)

    def _createCanvasBinding(self):
        self.canvas.bind("<Button-1>", self.startRect)
        self.canvas.bind("<ButtonRelease-1>", self.stopRect)
        self.canvas.bind("<B1-Motion>", self.movingRect)

    def startRect(self, event):
        # Translate mouse screen x0,y0 coordinates to canvas coordinates
        self.rectx0 = self.canvas.canvasx(event.x)
        self.recty0 = self.canvas.canvasy(event.y)
        self.canvas.delete("all")
        # Create rectangle

        self.rectid = self.canvas.create_rectangle(
            self.rectx0, self.recty0, self.rectx0, self.recty0, fill="#4eccde")

    def movingRect(self, event):
        # Translate mouse screen x1,y1 coordinates to canvas coordinates
        self.rectx1 = self.canvas.canvasx(event.x)
        self.recty1 = self.canvas.canvasy(event.y)
        # Modify rectangle x1, y1 coordinates
        self.canvas.coords(self.rectid, self.rectx0, self.recty0,
                           self.rectx1, self.recty1)
        # print('Rectangle x1, y1 = ', self.rectx1, self.recty1)

    def stopRect(self, event):
        # Translate mouse screen x1,y1 coordinates to canvas coordinates
        self.rectx1 = self.canvas.canvasx(event.x)
        self.recty1 = self.canvas.canvasy(event.y)
        # Modify rectangle x1, y1 coordinates
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
