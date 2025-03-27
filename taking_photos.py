import subprocess
import time
import os
from datetime import datetime
# Create the folder to store images (if it doesn't already exist)
# Make sure to change the pathway depending on host computer
folder_path = "/home/mori1/Desktop/Moriphotos"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Initialize the camera

# Take x amount of pictures, for x amount of rounds every x seconds
rounds = 5 # set the amount of rounds
amount = 3 # set the amount of pics per round
seconds = 60 # seconds between each round

ctime = datetime.now().time()
ctime = datetime.now().strftime("%H:%M:%S")
for rds in range (0, rounds):
    for pic in range(0, amount):
        # Make the filename for each image (H:M:S_Y-M-D.jpg)
        filename = os.path.join(folder_path, f"{ctime}_{datetime.today().date()}.jpg")
        
        # Capture the image and save it to a file
        image = subprocess.run(["libcamera-still"," --width"," 800"," --height ","800","-o", filename])

    
        print(f"Picture {rds +1 }.{pic + 1} taken. Waiting for 2 minutes")
        time.sleep(1)
    time.sleep(seconds) # sleep after a round is done.
