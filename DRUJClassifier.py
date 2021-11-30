# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 09:40:03 2021

@author: AnLWells
"""

# Load required packages and functions

import numpy as np
import matplotlib.pyplot as plt
from keras.models import model_from_json

# Define function for reading DICOM Images

import pydicom
from pydicom.pixel_data_handlers.util import apply_voi_lut


def read_xray(path, voi_lut = True, fix_monochrome = True):
    dicom = pydicom.read_file(path)
    
    # VOI LUT (if available by DICOM device) is used to transform raw DICOM data to "human-friendly" view
    if voi_lut:
        data = apply_voi_lut(dicom.pixel_array, dicom)
    else:
        data = dicom.pixel_array
               
    # depending on this value, X-ray may look inverted - fix that:
    if fix_monochrome and dicom.PhotometricInterpretation == "MONOCHROME1":
        data = np.amax(data) - data
        
    data = data - np.min(data)
    data = data / np.max(data)
    data = (data * 255).astype(np.uint8)
        
    return data

# Filenames for DICOM images

# filename01 = 'TestCases\Subject002\PAView'
# filename02 = 'TestCases\Subject002\ObliqueView'
# filename03 = 'TestCases\Subject002\LateralView'

from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename01 = askopenfilename() # show an "Open" dialog box and return the path to the selected file
filename02 = askopenfilename() # show an "Open" dialog box and return the path to the selected file
filename03 = askopenfilename() # show an "Open" dialog box and return the path to the selected file

# Load and look at the images

img1 = read_xray(filename01)
plt.figure(figsize = (12,12))
plt.imshow(img1, 'gray')

img2 = read_xray(filename02)
plt.figure(figsize = (12,12))
plt.imshow(img2, 'gray')

img3 = read_xray(filename03)
plt.figure(figsize = (12,12))
plt.imshow(img3, 'gray')

# Crop images

x1 = img1.shape
img1cr = img1[np.round(x1[0]/2).astype(int)-500:np.round(x1[0]/2).astype(int)+500, 
              np.round(x1[1]/2).astype(int)-350:np.round(x1[1]/2).astype(int)+350]

x2 = img2.shape
img2cr = img2[np.round(x2[0]/2).astype(int)-500:np.round(x2[0]/2).astype(int)+500, 
              np.round(x2[1]/2).astype(int)-350:np.round(x2[1]/2).astype(int)+350]

x3 = img3.shape
img3cr = img3[np.round(x3[0]/2).astype(int)-500:np.round(x3[0]/2).astype(int)+500, 
              np.round(x3[1]/2).astype(int)-350:np.round(x3[1]/2).astype(int)+350]

# Make combined view of images

ComboView = np.append(img1cr, img2cr, axis=1)
ComboView = np.append(ComboView, img3cr, axis=1)

# View Combined view

plt.imshow(ComboView, cmap='gray')  
plt.show

# Reduce resolution of combined view

ComboReduce = np.zeros((500, 1050))
ComboViewN = ComboView/255

for k in range(500):
    for i in range(1050):
        ComboReduce[k,i] = round((ComboViewN[2*k,2*i]+ComboViewN[2*k+1,2*i]+
                                    ComboViewN[2*k, 2*i+1]+ComboViewN[2*k+1,2*i+1])/4)           
        
# Reshape the input to match the input to the model

ComboReduce = np.reshape(ComboReduce,(1,500,1050,1))

# Load and run the model

# load json and create model
json_file = open('model20211129a.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model20211129a.h5")
print(" ")
print("Loaded model from disk")
# evaluate loaded model on test data
loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
# score = loaded_model.evaluate(X, Y, verbose=0)
# print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))

# Use the model to predict classification of fracture

predict_x=loaded_model.predict(ComboReduce)
classes_x=np.argmax(predict_x,axis=1)

print(" ")
if classes_x==0:
    print("Type of fracture is I")
else:
    if classes_x==1:
        print("Type of fracture is II")
    else:
        print("Type of fracture is III")
print("Type I:   ", round(predict_x[0,0]*100,2))
print("Type II:  ", round(predict_x[0,1]*100,2))
print("Type III: ", round(predict_x[0,2]*100,2))
