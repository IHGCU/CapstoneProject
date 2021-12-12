# CapstoneProject
Capstone Project for Master of Data Science at GCU

This project will build a CNN to classify xray images of distal radius fractures. The image data is not publicly available, so the bulk of the data will not be posted. A few test cases will be uploaded so that the classifier can be tested. For each case, there are three DICOM images: PA view, Oblique view, and Lateral view. 

The files contained in this repository are:
1. Subjects 001 to 005.ipynb - a Jupyter notebook showing how the images were converted from DICOM format to numpy arrays, cropped, and saved as CSV files.
2. DataPrepforDRUJ.ipynb - a Jupyter notebook showing how the CSV files were saved as a single array for processing with the Convolutional Neural Network (CNN).
3. CNNforDRUJCombinedViewReducedResolution.ipynb - a Jupyter notebook that defines, trains, and saves the parameters for a CNN
4. DRUJClassification.ipynb - a Jupyter notebook that takes the saved CNN parameters and three x-ray views of a fracture and classifies the fracture as a Type I, Type II, or Type III fracture. 
5. TestCases - a folder that contains DICOM images for 5 test cases. Subject005 was updated on 12/12/2021 so that a type I fracture would part of the test cases. 
6. model.h5 - a file with the saved model parameters NOTE: THIS FILE WAS TOO LARGE TO UPLOAD! The DRUJClassification.ipynb notebook will not run without it. I have uploaded it to my Google drive. If anyone is interested in running the classifier, please email me at laurieinmukono@gmail.com. I will share the file with you. 
7. model.json - a file with the saved model characteristics
8. DRUJClassifier.py - A Python script for running the classifier. This file requires the test cases and the model characteristics and model weights to run. There are also images of typical type I, II, and III fractures that are needed. They are in the Classifier folder. This file implements some elements of the GUI. 
9. Classifier - a folder that contains images of typical type I, II, and III fractures
