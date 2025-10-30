import os
b=65
for x in range(26):
    f=open(f"C:\Users\Aisha\Desktop\pp2\lab6\file\ALhABHET/{chr(b)}","w")
    b+=1
f.close()

import os

folder = "C:/Users/Aisha/Desktop/pp2/lab6/file/ALPHABET"
os.makedirs(folder, exist_ok=True)  

for b in range(65, 91):  
    with open(f"{folder}/{chr(b)}.txt", "w") as f:
        f.write(f"This is file {chr(b)}.txt")

print("26 files created!")

for i in range(1, 11):         
    a = f"File{i}.txt"  
    with open(a, "w") as file:  
        file.write(f" {i}")

import os

b = 1
for x in range(10):
    f = open(f"lab6/file/ALhABHET/File{b}.txt", "w")
    b += 1
    f.close()