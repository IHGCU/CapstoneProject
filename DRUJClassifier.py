# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 09:40:03 2021

@author: AnLWells
"""

# Load required packages

import PySimpleGUI as sg
import matplotlib.pyplot as plt
from keras.models import model_from_json
import numpy as np

# Define a function for reading DICOM Images

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

# Get path prefix for reading and saving files

layout = [  [sg.Text("What is the path where you will store files? For example: C:/Classifier/")],     
            [sg.Input()],
            [sg.Button('Ok')] ]

window = sg.Window('Path Prefix', layout)      
                                                

event, values = window.read()                   

filenamePrefix = values[0]
filenameCombView = filenamePrefix+"myFigure.png"

window.close()                                 



# Filenames for DICOM images

filename01 = sg.popup_get_file('Enter the file for the PA View')
filename02 = sg.popup_get_file('Enter the file for the Oblique View')
filename03 = sg.popup_get_file('Enter the file for the Lateral View')

# Load and look at the images

img1 = read_xray(filename01)
plt.figure(figsize = (12,12))
plt.imshow(img1, 'gray')
plt.title("PA View")
plt.show


img2 = read_xray(filename02)
plt.figure(figsize = (12,12))
plt.imshow(img2, 'gray')
plt.title("Oblique Veiw")
plt.show


img3 = read_xray(filename03)
plt.figure(figsize = (12,12))
plt.imshow(img3, 'gray')
plt.title("Lateral View")
plt.show


plt.figure(figsize = (12,12))
plt.show

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

# Reduce resolution of combined view

ComboReduce = np.zeros((500, 1050))
ComboViewN = ComboView/255

for k in range(500):
    for i in range(1050):
        ComboReduce[k,i] = round((ComboViewN[2*k,2*i]+ComboViewN[2*k+1,2*i]+
                                    ComboViewN[2*k, 2*i+1]+ComboViewN[2*k+1,2*i+1])/4)           
# View Combined view 

plt.figure(figsize=(6, 3))
plt.imshow(ComboView, cmap='gray') 
plt.title("Classified fracture, Combined View") 
plt.savefig(filenameCombView)

# Reshape the input to match the input to the model

ComboReduce = np.reshape(ComboReduce,(1,500,1050,1))

# Load and run the model

# load json and create model
json_file = open(filenamePrefix+'model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights(filenamePrefix+"model.h5")
print(" ")
print("Loaded model from disk")
# evaluate loaded model on test data
loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
# score = loaded_model.evaluate(X, Y, verbose=0)
# print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))

# Use the model to predict classification of fracture and produce the output for the model

predict_x=loaded_model.predict(ComboReduce)
classes_x=np.argmax(predict_x,axis=1)

if classes_x==0:
    str01=" Type of fracture is I"
    str05=" A typical type I fracture is shown with the classified fracture below"
    filename04 = filenamePrefix+'TypeI.png'
else:
    if classes_x==1:
        str01=" Type of fracture is II"
        str05=" A typical type II fracture is shown with the classified fracture below"
        filename04 = filenamePrefix+'TypeII.png'
    else:
        str01=" Type of fracture is III"
        str05=" A typical type III fracture is shown with the classified fracture below"
        filename04 = filenamePrefix+'TypeIII.png'

str02=' Type I:   ' + str(round(predict_x[0,0]*100,2))
str03=' Type II:  ' + str(round(predict_x[0,1]*100,2))
str04=' Type III: ' + str(round(predict_x[0,2]*100,2))

layout10 = [[sg.Listbox(values=[' Report for Classification of DRUJ Fracture', 
                                ' ', str01, ' ', 
                                ' The softmax numbers for each type of fracture are: ',
                                ' ', str02, str03, str04,
                                ' ', ' ', str05], size=(60,15), font=('Times', 14))],             
            [sg.Image(filename04)],                        
            [sg.Image('C:/Users/AnLWells/Documents/CapstoneProject/Classifier/myFigure.png')],
            [sg.Button('Ok')]]

window = sg.Window('Model Output',layout10)

event, values = window.read()

window.close()

