import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
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
import pyautogui
import pytesseract
import threading
from interactiveScreenshot import IS


def Image_processing():
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
    app = IS(screenshotWindow, root)


def runScreenRecording():
    global stopRecording
    with open('./data/pos.csv', 'r') as file:
        list_1 = file.read().split(',')
        position = list(map(int, list_1))
    while (True):

        capture = np.array(ImageGrab.grab(
            bbox=(position[0], position[1], position[2], position[3])))
        cvt_image = cv2.cvtColor(capture, cv2.COLOR_BGR2RGB)
        cv2.imshow('Original', cvt_image)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


def startThread():
    newThread = threading.Thread(target=runScreenRecording, daemon=True)
    newThread.start()


def stopThread():
    pass


if __name__ == "__main__":

    pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract'
    cvt_image = None

    baduRate = ["9600", "115200", "19200"]

    root = tk.Tk()
    root.title("Gamer Assist")
    root.geometry("322x290")
    root.resizable(False, False)

    # Adding Menu system
    menu_system = tk.Menu(root)
    root.config(menu=menu_system)

    # creating file menu item
    file_menu = tk.Menu(menu_system, tearoff=False)
    menu_system.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="New Config", command=None)
    file_menu.add_command(label="Open Config", command=None)
    file_menu.add_command(label="Save Config", command=None)
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

    originalImg = Image.open('images/Health.png')

    imgWidth, imgHeight = originalImg.size
    imageCanvas.update()
    newHeight = imageCanvas.winfo_height()

    if imgWidth <= imgHeight:
        newWidth = int(imageCanvas.winfo_height() / imgHeight * imgWidth)
    else:
        newWidth = imageCanvas.winfo_width()
        newHeight = int((newWidth/imgWidth)*imgHeight)

    resized = originalImg.resize((newWidth, newHeight))
    previewScreenshot = PIL.ImageTk.PhotoImage(resized)

    imageCanvas.create_image(
        ((220-newWidth)/2), ((220-newHeight)/2), image=previewScreenshot, anchor='nw')

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
    badu.current(0)
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
