                # -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 09:40:03 2021

@author: AnLWells

DRUJ Classifier
"""

# Load required packages

import pandas as pd
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

# Ask whether the images are for a left hand or a right hand

layout = [  [sg.Text("Are the images for a left hand or a right hand? (L/R)")],     
            [sg.Input()],
            [sg.Button('Ok')] ]

window = sg.Window('Left or Right', layout)      
                                                

event, values = window.read()                   

Hand01 = values[0]

window.close()                                 

# Filenames for DICOM images

filename01 = sg.popup_get_file('Enter the file for the PA View')
filename02 = sg.popup_get_file('Enter the file for the Oblique View')
filename03 = sg.popup_get_file('Enter the file for the Lateral View')

# Load and look at the images
# Determine where to crop the images

img1 = read_xray(filename01)
plt.figure(figsize = (12,12))
plt.imshow(img1, 'gray')
plt.title("PA View")
plt.savefig(filenamePrefix + 'PAView.png')

# Determine crop height

layoutPAH =  [   [sg.Text("What is the crop height? 0 start from top, 0.5 centered, 1 start at bottom")],     
                [sg.Input()],                     
                [sg.Button('Ok')],
                [sg.Image(filenamePrefix+'PAView.png')] ]

window = sg.Window("Crop Height", layoutPAH)

event, values = window.read()

CHPA = values[0]
CHPA = float(CHPA)

window.close()

# Determine crop width

layoutPAW =  [   [sg.Text("What is the crop width? 0 start from left, 0.5 centered, 1 start at right")],     
                [sg.Input()],                     
                [sg.Button('Ok')],
                [sg.Image(filenamePrefix+'PAView.png')] ]

window = sg.Window("Crop Width", layoutPAW)

event, values = window.read()

CWPA = values[0]
CWPA = float(CWPA)

window.close()


img2 = read_xray(filename02)
plt.figure(figsize = (12,12))
plt.imshow(img2, 'gray')
plt.title("Oblique Veiw")
plt.savefig(filenamePrefix + 'ObView.png')

# Determine crop height

layoutObH =  [   [sg.Text("What is the crop height? 0 start from top, 0.5 centered, 1 start at bottom")],     
                [sg.Input()],                     
                [sg.Button('Ok')],
                [sg.Image(filenamePrefix+'ObView.png')] ]

window = sg.Window("Crop Height", layoutObH)

event, values = window.read()

CHOb = values[0]
CHOb = float(CHOb)

window.close()

# Determine crop width

layoutObW =  [   [sg.Text("What is the crop width? 0 start from left, 0.5 centered, 1 start at right")],     
                [sg.Input()],                     
                [sg.Button('Ok')],
                [sg.Image(filenamePrefix+'ObView.png')] ]

window = sg.Window("Crop Width", layoutObW)

event, values = window.read()

CWOb = values[0]
CWOb = float(CWOb)

window.close()


img3 = read_xray(filename03)
plt.figure(figsize = (12,12))
plt.imshow(img3, 'gray')
plt.title("Lateral View")
plt.savefig(filenamePrefix + 'LView.png')

# Determine crop height

layoutLH =  [   [sg.Text("What is the crop height? 0 start from top, 0.5 centered, 1 start at bottom")],     
                [sg.Input()],                     
                [sg.Button('Ok')],
                [sg.Image(filenamePrefix+'LView.png')] ]

window = sg.Window("Crop Height", layoutLH)

event, values = window.read()

CHL = values[0]
CHL = float(CHL)

window.close()

# Determine crop width

layoutLW =  [   [sg.Text("What is the crop width? 0 start from left, 0.5 centered, 1 start at right")],     
                [sg.Input()],                     
                [sg.Button('Ok')],
                [sg.Image(filenamePrefix+'LView.png')] ]

window = sg.Window("Crop Width", layoutLW)

event, values = window.read()

CWL = values[0]
CWL = float(CWL)

window.close()


plt.figure(figsize = (12,12))
plt.show

# Crop images and reverse right hands so that the radius is always on the right of the image

x1 = img1.shape
PAH0 = np.round(CHPA*(x1[0]-1000)).astype(int)
PAW0 = np.round(CWPA*(x1[1]-700)).astype(int)

img1cr = img1[PAH0:PAH0+1000, 
              PAW0:PAW0+700]

if Hand01=="R" or Hand01=="r":
    img1crpd = pd.DataFrame(img1cr)
    img1cr = pd.DataFrame(img1crpd.iloc[:,699])
    for i in range(699):
        img1cr = img1cr.join(pd.DataFrame(img1crpd.iloc[:,698-i]))

x2 = img2.shape
ObH0 = np.round(CHOb*(x2[0]-1000)).astype(int)
ObW0 = np.round(CWOb*(x2[1]-700)).astype(int)

img2cr = img2[ObH0:ObH0+1000, 
              ObW0:ObW0+700]

if Hand01=="R" or Hand01=="r":
    img2crpd = pd.DataFrame(img2cr)
    img2cr = pd.DataFrame(img2crpd.iloc[:,699])
    for i in range(699):
        img2cr = img2cr.join(pd.DataFrame(img2crpd.iloc[:,698-i]))


x3 = img3.shape
LH0 = np.round(CHL*(x3[0]-1000)).astype(int)
LW0 = np.round(CWL*(x3[1]-700)).astype(int)

img3cr = img3[LH0:LH0+1000, 
              LW0:LW0+700]

if Hand01=="R" or Hand01=="r":
    img3crpd = pd.DataFrame(img3cr)
    img3cr = pd.DataFrame(img3crpd.iloc[:,699])
    for i in range(699):
        img3cr = img3cr.join(pd.DataFrame(img3crpd.iloc[:,698-i]))


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
            [sg.Image(filenamePrefix+'myFigure.png')],
            [sg.Button('Ok')]]

window = sg.Window('Model Output',layout10)

event, values = window.read()

window.close()

