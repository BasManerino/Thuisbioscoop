#administrator scherm

import tkinter as tk



window = tk.Tk()

#window.configure(bg="navyblue")



window.title("Thuis Bioscoop")

window.geometry("800x600")



#Label

title = tk.Label(text= "Totaal aantal bezoekers: ")

title.grid(column=0, row=4)

title.place(x=300, y=100)



title1 = tk.Label(text= "Naam: ")

title1.grid(column=4, row=4)

title1.place(x=250, y=200)



title2 = tk.Label(text= "Aantal Bezoekers: ")

title2.grid(column=4, row=5)

title2.place(x=250, y=250)



title3 = tk.Label(text= "Naam: ")

title3.grid(column=4, row=6)

title3.place(x=250, y=300)



title4 = tk.Label(text= "Aantal Bezoekers: ")

title4.grid(column=4, row=7)

title4.place(x=250, y=350)



title5= tk.Label(text= "Naam: ")

title5.grid(column=4, row=8)

title5.place(x=250, y=400)



title6 = tk.Label(text= "Aantal Bezoekers: ")

title6.grid(column=4, row=9)

title6.place(x=250, y=450)



#buttons

button1 = tk.Button(text="Header Menu")

button1.grid(column=0, row=0)

button1.place(x=0, y=0)



button2 = tk.Button(text="Film 1")

button2.grid(column=2, row=4)

button2.place(x=200, y=200)



button3 = tk.Button(text="Film 2")

button3.grid(column=2, row=6)

button3.place(x=200, y=300)



button4 = tk.Button(text="Film 3")

button4.grid(column=2, row=8)

button4.place(x=200, y=400)



window.mainloop()