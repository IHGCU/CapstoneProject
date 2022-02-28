# CapstoneProject
Capstone Project for Master of Data Science at GCU

This project will build a CNN to classify xray images of distal radius fractures. The image data is not publicly available, so the bulk of the data will not be posted. A few test cases will be uploaded so that the classifier can be tested. For each case, there are three DICOM images: PA view, Oblique view, and Lateral view. 

The files contained in this repository are:
1. CropImages.ipynb - a Jupyter notebook showing how the images were converted from DICOM format to numpy arrays, cropped, and saved as CSV files.
2. DataPrepforDRUJTrainVal.ipynb - a Jupyter notebook showing how the Training/Validation CSV files were saved as a single array for processing with the Convolutional Neural Network (CNN).
3. DataPrepforDRUJTest.ipynb - a Jypyter notebook showing how the Test set CSV files were saved as a single array for processing
4. CNNforDRUJCombinedViewReducedResolution.ipynb - a Jupyter notebook that defines, trains, and saves the parameters for a CNN
5. DRUJClassification.ipynb - a Jupyter notebook that takes the saved CNN parameters and three x-ray views of a fracture and classifies the fracture as a Type I, Type II, or Type III fracture. 
6. TestCases - a folder that contains DICOM images for 5 test cases. Subject005 was updated on 12/12/2021 so that a type I fracture would part of the test cases. 
7. model.h5 - a file with the saved model weights NOTE: THIS FILE WAS TOO LARGE TO UPLOAD! The DRUJClassification.ipynb notebook will not run without it. I have uploaded it to my Google drive. If anyone is interested in running the classifier, please email me at laurieinmukono@gmail.com. I will share the file with you. 
8. model.json - a file with the saved model characteristics
9. DRUJClassifier.py - A Python script for running the classifier. This file requires the test cases and the model characteristics and model weights to run. There are also images of typical type I, II, and III fractures that are needed. They are in the Classifier folder. This file implements some elements of the GUI. 
10. Classifier - a folder that contains images of typical type I, II, and III fractures
11. DSC590_0500 Wells User Guide for Distal Radius Fracture Classifier.pdf - The user guide for the classifier
12. System Administration Guide for Distal Radius Fracture Classifier.docx - The system administration guid for the classifier
13. DSC590_0500WellsFinalPresentation.mp4 - Video recording of presentation of the final project
14. DSC590_0500WellsDemonstration.mp4 - Video demonstration of the classifier
15. CapstoneProjectFinalReport.pdf - Final Report. Includes all milestones and conclusion
