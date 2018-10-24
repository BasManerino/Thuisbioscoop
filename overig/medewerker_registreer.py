from tkinter import *

root = Tk()

registerheaderlabel = Label(master=root,text='Registreer Medewerkers', font='Helvetica 16 bold', height=2)
registerheaderlabel.pack()



def register():
        print("hey")



naam = Label(master=root,text='Voer uw hele naam in',height=2)
naam.pack()

naamentry = Entry(master=root)
naamentry.pack(padx=10, pady=10)


adres = Label(master=root,text='Voer uw adres in',height=2)
adres .pack()

adresentry = Entry(master=root)
adresentry.pack(padx=10, pady=10)


wachtwoord = Label(master=root,text='Voer een wachtwoord in',height=2)
wachtwoord.pack()

wachtwoordentry = Entry(master=root)
wachtwoordentry.pack(padx=10, pady=10)

button = Button(master=root, text='Registreer', command=register)
button.pack(pady=10)


root.mainloop()