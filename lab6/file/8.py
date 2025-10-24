import os

path = "C:/Users/Aisha/Desktop/pp2/lab6/h"

if os.path.exists(path):
    os.rmdir(path)
else:
    print("The file does not exist")