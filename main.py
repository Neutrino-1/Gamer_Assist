import tkinter as tk

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

    def selectionDone(self):
        print('started at x = {1} y = {2} ended at x1 = {3} y1 = {4} '. format(self.rectid, self.rectx0, self.recty0, self.rectx1,
                     self.recty1))

    def _createCanvas(self):
        self.canvas = tk.Canvas(self.parent, width = root.winfo_screenwidth(), height = root.winfo_screenheight(),
                                bg = None)
        #self.canvas.grid(row=0, column=0)
        self.mainScreenButton = tk.Button(root, text="Main Menu", width=10, command=self.quit(),bg='#00ffea',fg='black')
        self.screenshotButton = tk.Button(root, text="Grab", width=10, command=self.selectionDone,bg='#00ff08',fg='black')
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

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"

def helloCallBack():
    pass

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    root.attributes('-alpha', 0.3)
    root.attributes("-fullscreen", True)
    app = InteractiveScreenshot(root)
    root.mainloop()
    