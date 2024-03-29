from tkinter import *
import PIL
from PIL import ImageDraw
import matplotlib.pyplot as plt

import numpy as np
import tensorflow as tf

import os

class App:
    def __init__(self):

        self.model = tf.keras.models.load_model('model.h5')

        self.old_x = None
        self.old_y = None

        self.brush_size = 15

        self.root = Tk()
        self.root.title("Digit Recognition Application")

        self.canvas = Canvas(self.root, width=300, height=300, bg="white")
        self.canvas.pack()

        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

        self.frame = Frame(self.root)
        self.frame.pack(fill=X)

        self.predict_button = Button(self.frame, text='Predict', command=self.predict)
        self.predict_button.grid(row=0, column=1)

        self.clear_button = Button(self.frame, text='Clear', command=self.clear)
        self.clear_button.grid(row=0, column=2)


        self.prediction_label = Label(self.root, text="Prediction: ")
        self.prediction_label.pack(fill=X)


        self.root.mainloop()


    def clear(self):
        self.canvas.delete("all")
        self.prediction_label.config(text="Prediction: ")


    def draw(self, event):
        if self.old_x and self.old_y:
            self.canvas.create_line(self.old_x, 
                                    self.old_y, 
                                    event.x, 
                                    event.y,
                                    fill='black', 
                                    width=self.brush_size,
                                    capstyle=ROUND,
                                    smooth=True)
        self.old_x = event.x
        self.old_y = event.y


    def reset(self, event):
        self.old_x = None
        self.old_y = None


    def predict(self):
        filename = "file_name"
        self.canvas.update()
        self.canvas.postscript(file=filename+".ps", colormode='color')
        img = PIL.Image.open(filename+".ps")

        inverted_image = PIL.ImageOps.invert(img)
        img_gray = inverted_image.convert("L")

        img_gray_resized = img_gray.resize((28, 28), PIL.Image.LANCZOS)

        x = np.array(img_gray_resized)
        x = x.reshape(1, 28, 28, -1)

        y_pred = np.argmax(self.model.predict(x))
        self.prediction_label.config(text="Prediction: " + str(y_pred))




app = App()