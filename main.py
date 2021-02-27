import os
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from tkinter import messagebox
import cv2
from PIL import ImageGrab
import PIL.Image
import PIL.ImageTk
from PIL import Image
import numpy as np
import math
import serial
import serial.tools.list_ports
import time
import pytesseract
import threading
from tkinter import filedialog
from interactiveScreenshot import IS


def newFile():
    global previewScreenshot
    img = Image.open('images/Not_found.png')
    imgData = imageForMainWindow(img)
    previewScreenshot = PIL.ImageTk.PhotoImage(imgData[0])
    imageCanvas.itemconfigure(canvImgId, image=previewScreenshot)


def saveFile():
    app.saveProcessedImg()
    print("Save Complete")


def loadFile():
    global position
    global previewloadImg
    global loadedFile

    file_name = filedialog.askopenfilename(
        initialdir="./data", title="Select file", filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
    with open(file_name, 'r') as file:
        list_1 = file.read().split(',')
        position = list(map(int, list_1))
    loadedFile = os.path.basename(file_name)[:-4] + ".png"
    loadImg = Image.open('./images/original/'+loadedFile)
    imgData = imageForMainWindow(loadImg)
    previewloadImg = PIL.ImageTk.PhotoImage(imgData[0])

    imageCanvas.itemconfigure(canvImgId, image=previewloadImg)
    # imageCanvas.create_image(
    #     ((220-imgData[1])/2), ((220-imgData[2])/2), image=previewloadImg, anchor='nw')


def doOcr(img):
    print(pytesseract.image_to_string(img))


def healthBar(thresh):
    calculate(thresh)
    print("healthBar")


def Image_processing(img):
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # blur the gray image to remove noise and to averaging the color
    blurred = cv2.bilateralFilter(
        gray_image, 15, position[-1], position[-1])
    # converting the blurred image to pure black(0) and white(255) binary image
    thresh = cv2.threshold(
        blurred, position[4], position[5], cv2.THRESH_BINARY)[1]
    if position[6] == 1:
        doOcr()
    elif position[6] == 2:
        thresh = cv2.Canny(thresh, 100, 150)
        healthBar(thresh)
    return PIL.Image.fromarray(thresh)


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
    global app
    # pyautogui.getWindowsWithTitle("Gamer Assist")[0].minimize()
    root.wm_state('iconic')
    screenshotWindow = tk.Toplevel(root)
    app = IS(screenshotWindow, root)


def runScreenRecording():
    global stopRecording
    global position
    global liveRecording

    if not position:
        tk.messagebox.showinfo(title="No file selected",
                               message="No CSV file selected")

    while (True):
        if stopRecording:
            break
        capture = (ImageGrab.grab(
            bbox=(position[0], position[1], position[2], position[3])))
        process = np.array(capture)
        cvt_image = cv2.cvtColor(process, cv2.COLOR_BGR2RGB)

        vidData = imageForMainWindow(Image_processing(cvt_image))
        liveRecording = PIL.ImageTk.PhotoImage(vidData[0])
        imageCanvas.itemconfig(canvImgId, image=liveRecording)


def startThread():
    global stopRecording
    stopRecording = False
    newThread = threading.Thread(target=runScreenRecording, daemon=True)
    newThread.start()


def stopThread():
    global stopRecording
    global stopImg
    stopRecording = True

    loadImg = Image.open('./images/original/'+loadedFile)
    imgData = imageForMainWindow(loadImg)
    stopImg = PIL.ImageTk.PhotoImage(imgData[0])
    imageCanvas.itemconfigure(canvImgId, image=stopImg)


def imageForMainWindow(img):
    originalImg = img

    imgWidth, imgHeight = originalImg.size
    imageCanvas.update()
    newHeight = imageCanvas.winfo_height()

    if imgWidth <= imgHeight:
        newWidth = int(imageCanvas.winfo_height() / imgHeight * imgWidth)
    else:
        newWidth = imageCanvas.winfo_width()
        newHeight = int((newWidth/imgWidth)*imgHeight)

    return (originalImg.resize((newWidth, newHeight)), newWidth, newHeight)


if __name__ == "__main__":

    pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract'
    cvt_image = None
    position = []
    baduRate = [110, 300, 600, 1200, 2400, 4800, 9600,
                14400, 19200, 38400, 57600, 115200, 128000, 256000]

    root = tk.Tk()
    root.title("Gamer Assist")
    root.geometry("385x305")
    root.resizable(False, False)
    processedVar = tk.IntVar()
    processedVar.set("1")
    # Adding Menu system
    menu_system = tk.Menu(root)
    root.config(menu=menu_system)

    # creating file menu item
    file_menu = tk.Menu(menu_system, tearoff=False)
    menu_system.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="New", command=newFile)
    file_menu.add_command(label="Open", command=loadFile)
    file_menu.add_command(label="Save As", command=saveFile)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)

    # creating help menu item
    help_menu = tk.Menu(menu_system, tearoff=False)
    menu_system.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="Manual", command=None)
    help_menu.add_command(label="About", command=None)

    imageCanvas = tk.Canvas(root, height=220, width=220, bg="black")
    imageCanvas.grid(padx=5, row=0, rowspan=3,
                     columnspan=2, column=0, sticky="W")

    img = Image.open('images/Not_found.png')
    imgData = imageForMainWindow(img)
    previewScreenshot = PIL.ImageTk.PhotoImage(imgData[0])

    canvImgId = imageCanvas.create_image(
        ((220-imgData[1])/2), ((220-imgData[2])/2), image=previewScreenshot, anchor='nw')

    startButton = tk.Button(root, text="Start", width=10, command=startThread)
    startButton.grid(padx=5, pady=5, row=0, column=2, sticky="NS")
    tk.Button(root, text="Stop", width=10, command=stopThread).grid(
        padx=5, pady=5, row=1, column=2, sticky="NS")
    tk.Button(root, text="Edit Config", width=10, command=newScreenArea).grid(
        padx=5, pady=5, row=2, column=2, sticky="NS")

    tk.Label(root, text="Badu Rate:").grid(
        padx=5, pady=5, row=3, column=0, sticky='NW')

    badu = ttk.Combobox(root, value=baduRate)
    badu.grid(padx=0, pady=5, row=3, column=1)
    badu.current(6)
    badu.bind("<<ComboboxSelected>>", None)

    tk.Label(root, text="Port:").grid(
        padx=5, pady=5, row=4, column=0, sticky='NW')

    comList = serial_ports()
    if not comList:
        comList.append("No device")
    com = ttk.Combobox(root, value=comList)
    com.grid(padx=5, pady=5, row=4, column=1)
    com.current(0)
    com.bind("<<ComboboxSelected>>", None)

    tk.Button(root, text="Refresh Port", width=10, command=refreshPorts).grid(
        padx=5, pady=5, row=4, column=2)

    root.mainloop()
