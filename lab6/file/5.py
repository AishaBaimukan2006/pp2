f = open("C:/Users/Aisha/Desktop/pp2/lab6/file/e.txt","w")
txt = [123457, "hello", "byebye", False ]
text = ""
for i in txt:
    text += str(i)+"\n"
f.write(text)
f.close()