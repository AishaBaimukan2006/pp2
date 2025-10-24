f = open("C:/Users/Aisha/Desktop/pp2/lab6/file/ALhABHET","r")
txt = f.read()
f.close()

p = open("C:/Users/Aisha/Desktop/pp2/lab6/file/e.txt","w")
p.write(txt)
p.close()