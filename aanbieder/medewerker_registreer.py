from tkinter import *
import pymongo
from pymongo import MongoClient

root = Tk()

registerheaderlabel = Label(master=root,text='Registreer Medewerkers', font='Helvetica 16 bold', height=2)
registerheaderlabel.pack()



def register(naam, adres, wachtwoord):
        print ('Connecting to database...')
        connection = pymongo.MongoClient ('ds159489.mlab.com', 59489)
        db = connection['thuisbioscoop']
        db.authenticate ("test123", "yourmom123")
        if db.is_mongos:
                print ('Connection successful.')
                mycol = db["aanbieders"]

                nosqlcharacter = {
                "Naam": naam,
                "Adres": adres,
                "Wachtwoord": wachtwoord}

                mycol.insert_one (nosqlcharacter)



naam = Label(master=root,text='Voer uw hele naam in',height=2)
naam.pack()

naamEntry = Entry(master=root)
naamEntry.pack(padx=10, pady=10)


adres = Label(master=root,text='Voer uw adres in',height=2)
adres .pack()

adresEntry = Entry(master=root)
adresEntry.pack(padx=10, pady=10)


wachtwoord = Label(master=root,text='Voer een wachtwoord in',height=2)
wachtwoord.pack()

wachtwoordEntry = Entry(master=root,show="*")
wachtwoordEntry.pack(padx=10, pady=10)

button = Button(master=root, text='Registreer', command= lambda: register(naamEntry.get(), adresEntry.get(), wachtwoordEntry.get()))
button.pack(pady=10)


root.mainloop()