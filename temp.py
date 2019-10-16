
from Tkinter import *

root = Tk()

def doNothing():
	print("Doing Nothing")

root.title("GUI-Chess")



menu = Menu(root)
root.config(menu= menu)

subMenu = Menu(menu)
menu.add_cascade(label="File", menu = subMenu)
subMenu.add_command(label="New", command=doNothing)
subMenu.add_command(label="Save", command=doNothing)
subMenu.add_separator()
subMenu.add_command(label="Exit", command=doNothing)

editMenu = Menu(menu)
menu.add_cascade(label="Edit", menu = editMenu)
editMenu.add_command(label="Redo", command=doNothing)




toolbar = Frame(root, bg="blue")

insertB = Button(toolbar, text = "Insert Image", command= doNothing)
insertB.pack(side = LEFT,padx =2, pady = 2)
printB = Button(toolbar, text = "Print", command= doNothing)
printB.pack(side = LEFT,padx =2, pady = 2)

toolbar.pack(side=TOP, fill = X)




status = Label(root, text = "Nothing for now...", bd=1, relief=SUNKEN,anchor =W)
status.pack(side=BOTTOM, fill = X)



canvas_width = 800
canvas_height =800

canvas = Canvas(root, 
           width=canvas_width, 
           height=canvas_height, bg='black', bd = 2)

canvas.pack()

img = PhotoImage(file="yellow.png")
canvas.create_image(0,0, anchor=NW, image=img)

def checkered(canvas, line_distance):
   # vertical lines at an interval of "line_distance" pixel
   for x in range(line_distance,canvas_width,line_distance):
      canvas.create_line(x, 0, x, canvas_height, fill="#476042", width =3)
   # horizontal lines at an interval of "line_distance" pixel
   for y in range(line_distance,canvas_height,line_distance):
      canvas.create_line(0, y, canvas_width, y, fill="#476042", width =3)
checkered(canvas,100)




ent = Entry(root)
ent.pack()
ent.focus_set() 
root.mainloop()
