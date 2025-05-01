
###
# Copyright (c) 2025 Roland Labana. All rights reserved.
# Permission is hereby granted, free of charge, to use, copy, modify, merge, publish, 
# distribute, sublicense, and/or sell copies of this software for educational purposes, 
# provided that the above copyright notice and this permission notice are included in all copies or substantial portions of the software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NONINFRIGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, 
# ARISING FROM, OUT OF, OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
###


'''

* v4l2-ctl --list-ctrls  :  shell cmd to list avail camera settings, or v4l2-ctl --device=/dev/video0 --list-ctrls 
Lists controls, ranges, and current value
User Controls

                     brightness 0x00980900 (int)    : min=0 max=255 step=1 default=128 value=128
                       contrast 0x00980901 (int)    : min=0 max=255 step=1 default=34 value=34
                     saturation 0x00980902 (int)    : min=0 max=255 step=1 default=48 value=48
                            hue 0x00980903 (int)    : min=0 max=255 step=1 default=128 value=128
        white_balance_automatic 0x0098090c (bool)   : default=1 value=0
                          gamma 0x00980910 (int)    : min=100 max=300 step=1 default=110 value=110
                           gain 0x00980913 (int)    : min=0 max=255 step=1 default=0 value=0
           power_line_frequency 0x00980918 (menu)   : min=0 max=2 default=1 value=1 (50 Hz)
      white_balance_temperature 0x0098091a (int)    : min=2800 max=6500 step=1 default=4600 value=4600
                      sharpness 0x0098091b (int)    : min=0 max=255 step=1 default=38 value=38
         backlight_compensation 0x0098091c (int)    : min=0 max=10 step=1 default=4 value=4

Camera Controls

                  auto_exposure 0x009a0901 (menu)   : min=0 max=3 default=3 value=3 (Aperture Priority Mode)
         exposure_time_absolute 0x009a0902 (int)    : min=3 max=2047 step=1 default=166 value=2047 flags=inactive
     exposure_dynamic_framerate 0x009a0903 (bool)   : default=0 value=1
                   pan_absolute 0x009a0908 (int)    : min=-648000 max=648000 step=3600 default=0 value=0
                  tilt_absolute 0x009a0909 (int)    : min=-648000 max=648000 step=3600 default=0 value=0
                 focus_absolute 0x009a090a (int)    : min=0 max=255 step=1 default=0 value=50
     focus_automatic_continuous 0x009a090c (bool)   : default=0 value=0
                  zoom_absolute 0x009a090d (int)    : min=0 max=60 step=1 default=0 value=0
'''






import cv2
import os
import datetime


DEBUG = True


# Open log file
log_file = open("v4l2_settings.log", "w")

# Function to run v4l2-ctl commands and log them
def set_v4l2_ctrl(ctrl, value):
    cmd = f"v4l2-ctl --device=/dev/video0 --set-ctrl={ctrl}={value}"
    os.system(cmd)
    log_file.write(f"{datetime.datetime.now()}: Set {ctrl} to {value}\n")

# Initialize camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera.")
    log_file.write(f"{datetime.datetime.now()}: Error: Could not open camera.\n")
    log_file.close()
    exit()

# Set resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Disable auto modes for full manual control
set_v4l2_ctrl("auto_exposure", 3)  # 1 = Manual Mode, 3 = aperture pri, 0 = ?, 2= ?
set_v4l2_ctrl("focus_automatic_continuous", 0)  # Disable auto-focus
set_v4l2_ctrl("white_balance_automatic", 0)  # Disable auto white balance

# Initial settings
brightness = 128
contrast = 34 
gain = 0
exposure = 166
focus = 50
sharpness = 38
saturation = 48

# Apply initial settings
set_v4l2_ctrl("brightness", brightness)
set_v4l2_ctrl("contrast", contrast)
set_v4l2_ctrl("gain", gain)
set_v4l2_ctrl("exposure_time_absolute", exposure)
set_v4l2_ctrl("focus_absolute", focus)
set_v4l2_ctrl("sharpness", sharpness)
set_v4l2_ctrl("saturation", saturation)


print("settings:")
current_settings = f"Current - B: {brightness}, C: {contrast}, G: {gain}, E: {exposure}, F: {focus}, S: {sharpness}"
print(current_settings)
log_file.write(f"{datetime.datetime.now()}: {current_settings}\n")


#read a few frames so auto exposure has time
for _ in range(5):  
    ret, frame = cap.read()  # Read and discard a few frames


if not ret:
   print("Error: Could not read frame.")
   log_file.write(f"{datetime.datetime.now()}: Error: Could not read frame.\n")
else:
   fname = input("enter file name (include .jpg):  ")
   cv2.imwrite(fname, frame)
   print("Final image saved as ", fname)
   log_file.write(f"{datetime.datetime.now()}: Final image saved as {fname}")


cap.release()
cv2.destroyAllWindows()
log_file.close()


