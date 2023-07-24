import subprocess
import os
import random

def detect(img_path):
    ris = subprocess.run(["python", os.getcwd()+"/yolov5/detect.py", "--weights", "model/best.pt", "--img", "640", "--conf", "0.05", "--source", str(img_path), "--half"], capture_output=True, text=True) 
    ris_class, ris_img_path = ris.stdout.split(",")
    print(f"The predicted class is <{ris_class}>")
    print(f"Its result image can be found at {ris_img_path}")

if __name__ == "__main__":
    # now we simulate the interaction of the users with the robot when they show him the item (garbage) to throw...
    img_path = "data/user_imgs/"+str(random.randint(1, 20))+".jpg"
    detect(img_path)