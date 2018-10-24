from tkinter import *

root = Tk()

registerheaderlabel = Label(master=root,text='Login Medewerkers', font='Helvetica 16 bold', height=2)
registerheaderlabel.pack()



def login():
        print("hey")



loginnaam = Label(master=root,text='Voer uw hele naam in',height=2)
loginnaam.pack()

loginnaamentry = Entry(master=root)
loginnaamentry.pack(padx=10, pady=10)


loginwachtwoord = Label(master=root,text='Voer een wachtwoord in',height=2)
loginwachtwoord.pack()

wachtwoordentry = Entry(master=root)
wachtwoordentry.pack(padx=10, pady=10)

button = Button(master=root, text='Login', command=login)
button.pack(pady=10)


root.mainloop()