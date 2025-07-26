# Digit Recognizer
Is a project user draw digit in canvas, and the model predict the number.
I used Pygame for the drawing, Scikit-learn to build the model, and [MNIST dataset](https://www.openml.org/search?type=data&status=active&id=554).

## Files
 - `prediciton.py`: Load the model, and contain the functions for predicting and preparing the canvas.
 - `model.ipynb`: Process of build the models.
 - `canvases.csv`: Contain few digits I made in Pygame, for building *scale_setting_reg* model.
 - `models/rf_clf.joblib`: Model for predict the digit, will be created after run *main.py* in first time.
 - `models/scale_setting_reg.joblib`:  Model for predict the blur & bold settings, to make the digit that user made look like the MNIST dataset.

## Installation
Clone the project:
`git clone https://github.com/Abdullah-Saeed-BB/digit_recognizer.git`

Run the `main.py` (Warning: At first time it will create model and train it, so it will take some time depend on your device)
<br/>
<br/>
<p align="center">
  <img src="https://github.com/user-attachments/assets/a131c4dd-10ff-4af7-9314-5fa00be57f8d" alt="Demo" width="400"/>
</p>
