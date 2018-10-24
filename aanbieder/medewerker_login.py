from tkinter import *
import pymongo
from pymongo import MongoClient

root = Tk()

loginheaderlabel = Label(master=root,text='Login Medewerkers', font='Helvetica 16 bold', height=2)
loginheaderlabel.pack()

def login(naam, wachtwoord):
        print ('Connecting to database...')
        connection = pymongo.MongoClient ('ds159489.mlab.com', 59489)
        db = connection['thuisbioscoop']
        db.authenticate ("test123", "yourmom123")
        if db.is_mongos:
                print ('Connection successful.')
                mycol = db["aanbieders"]

                callstats = {"Naam": naam, "Wachtwoord": wachtwoord}

                findStats = mycol.find_one (callstats)
                print(findStats["Naam"])
                print(findStats["Wachtwoord"])
                print(findStats["Adres"])



naam = Label(master=root,text='Voer uw hele naam in',height=2)
naam.pack()

naamEntry = Entry(master=root)
naamEntry.pack(padx=10, pady=10)

wachtwoord = Label(master=root,text='Voer uw wachtwoord in',height=2)
wachtwoord.pack()

wachtwoordEntry = Entry(master=root,show="*")
wachtwoordEntry.pack(padx=10, pady=10)

button = Button(master=root, text='Login', command= lambda: login(naamEntry.get(), wachtwoordEntry.get()))
button.pack(pady=10)


root.mainloop()