from tkinter import *
from PIL import Image, ImageTk

root = Tk()

root.configure(bg="purple")

root.title("Thuis Bioscoop")
frame = Frame(root, bg="purple")

h1 = Label(frame, fg="white", bg="purple", font=("Arial", 50), text="HOMEPAGE")
h2 = Label(frame, fg="white", bg="purple", font=("Arial", 30), text="WELKOM GEBRUIKER")
img = Image.open("homepage.jpg")
photo = ImageTk.PhotoImage(img)

picture = Label(frame, image=photo)
picture.image = photo

frame.pack(fill=None, expand=True)
h1.pack(fill=None, expand=True)
h2.pack(fill=None, expand=True)
picture.pack(fill=None, expand=True)


root.mainloop()
