How to use:
Step 1: To get the code to work you will have to install the libraries at the top of the file using pip. Type this in the command prompt (assuming you have python):
pip install opencv-python
(then after that downloads)
pip install pillow
These libraries are used for image processing.

Step 2: Connect a webcam to your computer.  
On line 30: “cap = cv2.VideoCapture(1)” the code gets the second camera connected to your laptop (including the built in camera).
if you want to use your built in camera or you don’t have a built in camera change line 30 to “cap = cv2.VideoCapture(0)” any webcam should work for this.
If you want to use your phone, look up how to use your phone as a webcam.  I used a program called droidcam for this because I don't have a webcam at home.

Step 3: point the camera at some black lego connector pieces and press the spacebar.

Hopefully this is enough information if you want to actually run this Krill, if not just ask me lol.  



