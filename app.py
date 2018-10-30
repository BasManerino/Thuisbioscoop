import tkinter as tk
import requests
import xmltodict
import time
from datetime import datetime
import urllib.request
from PIL import Image, ImageTk
from pathlib import Path
import pymongo
from pymongo import MongoClient
from functools import partial
import qrcode
import random, string
import hashlib
import uuid

root = tk.Tk ()

global menu
menu = 0

global aanbieder

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()
        self.configure(bg="purple")

class Homepage(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       frame = tk.Frame (self, bg="purple")

       h1 = tk.Label (frame, fg="white", bg="purple", font=("Arial", 50), text="HOMEPAGE")
       h2 = tk.Label (frame, fg="white", bg="purple", font=("Arial", 30), text="WELKOM GEBRUIKER")
       img = Image.open ("homepage.jpg")
       photo = ImageTk.PhotoImage (img)

       picture = tk.Label (frame, image=photo)
       picture.image = photo

       frame.pack (fill=None, expand=True)
       h1.pack (fill=None, expand=True)
       h2.pack (fill=None, expand=True)
       picture.pack (fill=None, expand=True)

class FilmOverzichtBezoeker(Page):
   def __init__(self, film):
       Page.__init__(self, film)

       container = tk.Frame (self)
       container.pack (side="top", fill="both", expand=True)

       def download_cover(url, naam):
           name = (str (naam) + '.jpg')
           urllib.request.urlretrieve (url, name)

           return name

       date = time.strftime ("%d-%m-%Y")
       print (date)

       def data():
           print ('Connecting to database...')
           connection = pymongo.MongoClient ('ds159489.mlab.com', 59489)
           db = connection['thuisbioscoop']
           db.authenticate ("test123", "wachtwoord123")
           if db.is_mongos:
               print ('Connection successful.')
               mycol = db["films"]

               callstats = {"Datum": date}

               findStats = mycol.find (callstats)

               labelcover = tk.Label (frame, text="Cover")
               labelcover.grid (row=0, column=1, sticky=tk.NW)

               labeltitel = tk.Label (frame, text="Titel")
               labeltitel.grid (row=0, column=2, sticky=tk.NW)

               labelgenre = tk.Label (frame, text="Genre")
               labelgenre.grid (row=0, column=3, sticky=tk.NW)

               labelstarttijd = tk.Label (frame, text="Starttijd")
               labelstarttijd.grid (row=0, column=4, sticky=tk.NW)

               labeleindtijd = tk.Label (frame, text="Eindtijd")
               labeleindtijd.grid (row=0, column=5, sticky=tk.NW)

               labeladres = tk.Label (frame, text="Adres")
               labeladres.grid (row=0, column=6, sticky=tk.NW)

               row = 1

               def get_film(film, starttijd, eindtijd):
                   global filmtitel
                   filmtitel = film
                   global start
                   start = starttijd
                   global eind
                   eind = eindtijd
                   p1.lift()

               for film in findStats:
                   titel = tk.Label (frame, text=film['Titel'].encode ("utf-8"), font="Helvetica 18 bold", fg="white",
                                  bg="purple")
                   canvas = tk.Canvas (frame)
                   img = ImageTk.PhotoImage (Image.open (download_cover (film['Cover'], titel)))
                   cover = tk.Label (frame, image=img)
                   cover.image = img
                   genre = tk.Label (frame, text=film['Genre'].encode ("utf-8"), font="Helvetica 18 bold", fg="white",
                                  bg="purple")
                   starttijd = tk.Label (frame, text=film['Starttijd'].encode ("utf-8"), font="Helvetica 18 bold",
                                      fg="white", bg="purple")
                   eindtijd = tk.Label (frame, text=film['Eindtijd'].encode ("utf-8"), font="Helvetica 18 bold",
                                     fg="white", bg="purple")
                   adres = tk.Label (frame, text=film['Adres'].encode ("utf-8"), font="Helvetica 18 bold", fg="white",
                                  bg="purple")

                   action = partial(get_film,film['Titel'],film["Starttijd"],film["Eindtijd"])
                   button = tk.Button (frame, text='Reserveer', command=action)

                   cover.grid (row=row, column=1, sticky=tk.NW)
                   titel.grid (row=row, column=2, sticky=tk.NW)
                   genre.grid (row=row, column=3, sticky=tk.NW)
                   starttijd.grid (row=row, column=4, sticky=tk.NW)
                   eindtijd.grid (row=row, column=5, sticky=tk.NW)
                   adres.grid (row=row, column=6, sticky=tk.NW)
                   button.grid (row=row, column=7, sticky=tk.NW)

                   """
                   st = int (film['starttijd'])
                   starttijd = (datetime.utcfromtimestamp (st).strftime ('%m-%d %H:%M'))


                   et = int (film['eindtijd'])
                   eindtijd = (datetime.utcfromtimestamp (et).strftime ('%m-%d %H:%M'))
                   """
                   row += 1

       p1 = LoginBezoeker(self)
       p1.place (in_=container, x=0, y=0, relwidth=1, relheight=1)

       def myfunction(event):
           canvas.configure (scrollregion=canvas.bbox ("all"), width=1500, height=800)

       sizex = 800
       sizey = 600
       posx = 100
       posy = 100
       root.wm_geometry ("%dx%d+%d+%d" % (sizex, sizey, posx, posy))

       myframe = tk.Frame (self, relief=tk.GROOVE, width=50, height=100, bd=1)
       myframe.place (x=10, y=10)

       canvas = tk.Canvas (myframe, bg="Purple")
       frame = tk.Frame (canvas, bg="Purple")
       myscrollbar = tk.Scrollbar (myframe, orient="vertical", command=canvas.yview)
       canvas.configure (yscrollcommand=myscrollbar.set)

       myscrollbar.pack (side="right", fill="y")
       canvas.pack (side="left")
       canvas.create_window ((0, 0), window=frame, anchor='nw')
       frame.bind ("<Configure>", myfunction)

       data ()
       # root.mainloop ()

       # for p in Path (".").glob ("*.jpg"):
       #     p.unlink ()

class LoginBezoeker (Page):
    def __init__(self, *args):
        Page.__init__ (self, *args)

        self.configure(bg="purple")
        loginheaderlabel = tk.Label (master=self,
                                  text='Voer hier uw gegevens in en klik dan op OK om deze film te reserveren.',
                                  font='Helvetica 16 bold', height=2, bg="purple", fg="white")
        loginheaderlabel.pack ()

        def randomword(length):
            letters = string.ascii_lowercase
            return str(''.join (random.choice (letters) for i in range (length)))

        woordje = randomword(14)

        def bezoeken(naam, email, film, starttijd, eindtijd, word):

            # Create an image from the QR Code instance
            print ('Connecting to database...')
            connection = pymongo.MongoClient ('ds159489.mlab.com', 59489)
            db = connection['thuisbioscoop']
            db.authenticate ("test123", "wachtwoord123")
            if db.is_mongos:
                print ('Connection successful.')
                mycol2 = db["films"]

                callstats2 = {"Titel": film}

                findStats2 = mycol2.find_one (callstats2)

                mycol = db["bezoekers"]

                nosqlcharacter = {"Naam": naam, "Email": email, "Film": film, "code": word, "Aanbieder": findStats2["Aanbieder"]}

                mycol.insert_one (nosqlcharacter)

                qr = qrcode.QRCode (version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10,
                    border=4, )

                data = str (word)
                print (data)

                adres = tk.Label (master=self, text="Adres: " + findStats2["Adres"], background="purple", foreground="white")
                adres.pack (pady=10, padx=10, )

                # Add data
                qr.add_data (data)
                qr.make (fit=True)

                # Create an image from the QR Code instance
                img = qr.make_image ()

                # Save it somewhere, change the extension as needed:
                # img.save("image.png")
                # img.save("image.bmp")
                # img.save("image.jpeg")
                img.save ("QR.jpg")
                qrframe = tk.Frame (master=self)
                codelabel = tk.Label (master=self, text="Code: " + data, background="purple", foreground="white")
                codelabel.pack (pady=10, padx=10, )
                tijdlabel = tk.Label (master=self, text="Speeltijd: " + starttijd + ' - ' + eindtijd, background="purple", foreground="white")
                tijdlabel.pack (pady=10, padx=10, )
                qrframe.pack (fill=None, expand=True, pady=10, padx=10)
                img = ImageTk.PhotoImage (Image.open ("QR.jpg"))
                cover = tk.Label (qrframe, image=img)
                cover.image = img
                cover.pack ()
                titelnaam = tk.Label (master=self, text="Film: " + film, background="purple", foreground="white")
                titelnaam.pack (pady=10, padx=10, )

        naam = tk.Label (master=self, text='Voer uw hele naam in', height=2, bg="purple", fg="white")
        naam.pack ()

        naamEntry = tk.Entry (master=self)
        naamEntry.pack (padx=10, pady=10)

        email = tk.Label (master=self, text='Voer uw email adres in', height=2, bg="purple", fg="white")
        email.pack ()

        emailEntry = tk.Entry (master=self)
        emailEntry.pack (padx=10, pady=10)

        button = tk.Button (master=self, text='OK',
                         command=lambda:[bezoeken(naamEntry.get(), emailEntry.get(), filmtitel, start, eind, woordje), button.destroy()])
        button.pack (pady=10)

        scancodetxt = tk.Label (master=self,
                                text="Zodra u uw gegevens heeft ingevuld en verzonden zal er hier een QR code verschijnen. Scan deze om uw toegangscode te verkrijgen.",
                                background="purple", foreground="white")
        scancodetxt.pack (pady=10, padx=10, fill=None, expand=True)

class RegistrerenAanbieder(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__ (self, *args, **kwargs)
        self.configure(bg="purple")

        def hash_password(password):
            # uuid is used to generate a random number
            salt = uuid.uuid4 ().hex
            return hashlib.sha256 (salt.encode () + password.encode ()).hexdigest () + ':' + salt

        registerheaderlabel = tk.Label (master=self, text='Registreer aanbieders', font='Helvetica 16 bold', height=2, fg="white", bg="purple")
        registerheaderlabel.pack ()

        def register(naam, adres, wachtwoord):
            hashed_password = hash_password(wachtwoord)
            print ('Connecting to database...')
            connection = pymongo.MongoClient ('ds159489.mlab.com', 59489)
            db = connection['thuisbioscoop']
            db.authenticate ("test123", "wachtwoord123")
            if db.is_mongos:
                print ('Connection successful.')
                mycol = db["aanbieders"]

                nosqlcharacter = {"Naam": naam, "Adres": adres, "Wachtwoord": hashed_password}

                mycol.insert_one (nosqlcharacter)

                button = tk.Button (master=self, state=tk.DISABLED, text='Registreer',
                                    command=lambda: register (naamEntry.get (), adresEntry.get (),
                                                              wachtwoordEntry.get ()))
                button.pack (pady=10)

                melding = tk.Label (master=self, text='U bent registreerd, u kunt nu inloggen.', height=2, fg="white", bg="purple")
                melding.pack ()

        naam = tk.Label (master=self, text='Voer uw hele naam in', height=2, fg="white", bg="purple")
        naam.pack ()

        naamEntry = tk.Entry (master=self)
        naamEntry.pack (padx=10, pady=10)

        adres = tk.Label (master=self, text='Voer uw adres in', height=2, fg="white", bg="purple")
        adres.pack ()

        adresEntry = tk.Entry (master=self)
        adresEntry.pack (padx=10, pady=10)

        wachtwoord = tk.Label (master=self, text='Voer een wachtwoord in', height=2, fg="white", bg="purple")
        wachtwoord.pack ()

        wachtwoordEntry = tk.Entry (master=self, show="*")
        wachtwoordEntry.pack (padx=10, pady=10)

        button = tk.Button (master=self, text='Registreer',
                         command=lambda:[register (naamEntry.get (), adresEntry.get (), wachtwoordEntry.get ()),button.destroy()])
        button.pack (pady=10)

class LoginAanbieder(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__ (self, *args, **kwargs)
        self.configure (bg="purple")

        loginheaderlabel = tk.Label (master=self, text='Login aanbieders', font='Helvetica 16 bold', height=2, bg="purple", fg="white")
        loginheaderlabel.pack ()

        naam = tk.Label (master=self, text='Voer uw hele naam in', height=2, bg="purple", fg="white")
        naam.pack ()

        naamEntry = tk.Entry (master=self)
        naamEntry.pack (padx=10, pady=10)

        wachtwoord = tk.Label (master=self, text='Voer uw wachtwoord in', height=2, bg="purple", fg="white")
        wachtwoord.pack ()

        wachtwoordEntry = tk.Entry (master=self, show="*")
        wachtwoordEntry.pack (padx=10, pady=10)

        button = tk.Button (master=self, text='Login', command=lambda: login(naamEntry.get (), wachtwoordEntry.get ()))
        button.pack (pady=10)

class FilmOverzichtAanbieder(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       date = time.strftime ("%d-%m-%Y")

       api_url = 'http://api.filmtotaal.nl/filmsoptv.xml?apikey=djg2nqcl4jpkwivqgjdox3klob4zyx3d&dag=' + str (
           date) + '&sorteer=0'
       response = requests.get (api_url)

       filmXML = xmltodict.parse (response.text)

       def download_cover(url, naam):
           name = (str (naam) + '.jpg')
           urllib.request.urlretrieve (url, name)

           return name

       date = time.strftime ("%d-%m-%Y")

       def bied_aan(titel, cover, genre, starttijd, eindtijd, naam_aanbieder, datum, row):
           def check(aanbieder):
               connection = pymongo.MongoClient ('ds159489.mlab.com', 59489)
               db = connection['thuisbioscoop']
               db.authenticate ("test123", "wachtwoord123")
               if db.is_mongos:
                   print ('Connection successful.')
                   mycol = db["aanbieders"]

                   callstats = {"Naam": aanbieder}

                   findStats = mycol.find_one (callstats)
                   print(aanbieder)
                   return findStats["Naam"], findStats["Adres"]

           naam, adres = check(naam_aanbieder)
           connection = pymongo.MongoClient ('ds159489.mlab.com', 59489)
           db = connection['thuisbioscoop']
           db.authenticate ("test123", "wachtwoord123")
           if db.is_mongos:
               print ('Connection successful.')
               mycol = db["films"]

               nosqlcharacter = {"Titel": titel, "Cover": cover, "Genre": genre, "Starttijd": starttijd,
                   "Eindtijd": eindtijd, "Aanbieder": naam, "Adres": adres, "Datum": datum}

               mycol.insert_one (nosqlcharacter)


               button = tk.Button (frame, text='Bied film aan', state=tk.DISABLED, bg="blue", fg="white")
               button.grid(row=row, column=6, sticky=tk.NW)

               melding = tk.Label (frame, text='De film is succesvol aangeboden.', height=2, fg="white", bg="purple")
               melding.grid(row=row, column=7, sticky=tk.NW)

       def data(aanbieder):
           api_url = 'http://api.filmtotaal.nl/filmsoptv.xml?apikey=djg2nqcl4jpkwivqgjdox3klob4zyx3d&dag=' + str (
               date) + '&sorteer=0'
           response = requests.get (api_url)

           filmXML = xmltodict.parse (response.text)

           row = 4

           rood = tk.Label (frame, text="RODE KNOP:", fg="white", bg="red")
           rood.grid (row=0, column=1, sticky=tk.NW)

           roodtekst = tk.Label (frame, text="Film is al aangeboden door een andere aanbieder", fg="white", bg="purple")
           roodtekst.grid (row=0, column=2, sticky=tk.NW)

           blauw = tk.Label (frame, text="BLAUWE KNOP:", fg="white", bg="blue")
           blauw.grid (row=1, column=1, sticky=tk.NW)

           blauwtekst = tk.Label (frame, text="Film is al aangeboden door u", fg="white", bg="purple")
           blauwtekst.grid (row=1, column=2, sticky=tk.NW)

           groen = tk.Label (frame, text="GROENE KNOP:", fg="white", bg="green")
           groen.grid (row=2, column=1, sticky=tk.NW)

           groentekst = tk.Label (frame, text="Film is nog niet aangeboden", fg="white", bg="purple")
           groentekst.grid (row=2, column=2, sticky=tk.NW)

           labelcover = tk.Label (frame, text="Cover")
           labelcover.grid (row=3, column=1, sticky=tk.NW)

           labeltitel = tk.Label (frame, text="Titel")
           labeltitel.grid (row=3, column=2, sticky=tk.NW)

           labelstarttijd = tk.Label (frame, text="Starttijd")
           labelstarttijd.grid (row=3, column=3, sticky=tk.NW)

           labeleindtijd = tk.Label (frame, text="Eindtijd")
           labeleindtijd.grid (row=3, column=4, sticky=tk.NW)

           labelkanaal = tk.Label (frame, text="Kanaal")
           labelkanaal.grid (row=3, column=5, sticky=tk.NW)

           connection = pymongo.MongoClient ('ds159489.mlab.com', 59489)
           db = connection['thuisbioscoop']
           db.authenticate ("test123", "wachtwoord123")

           mycol = db["films"]

           def check_aanbieding(mycol, titel, row, action):
               callstats = {"Titel": titel}
               findStats = mycol.find_one (callstats)
               if(findStats == None):
                   button = tk.Button (frame, text='Bied film aan', command=lambda:[action(), button.destroy()], bg="green", fg="white")
                   button.grid (row=row, column=6, sticky=tk.NW)
               elif(findStats['Aanbieder'] == aanbieder):
                   button = tk.Button (frame, text='Bied film aan', state=tk.DISABLED, bg="blue", fg="white")
                   button.grid (row=row, column=6, sticky=tk.NW)
               else:
                   button = tk.Button (frame, text='Bied film aan', state=tk.DISABLED, bg="red", fg="white")
                   button.grid (row=row, column=6, sticky=tk.NW)



           for film in filmXML['filmsoptv']['film']:
               st = int (film['starttijd'])
               starttijd = (datetime.utcfromtimestamp (st).strftime ('%H:%M'))

               et = int (film['eindtijd'])
               eindtijd = (datetime.utcfromtimestamp (et).strftime ('%H:%M'))

               titel = tk.Label (frame, text=film['titel'].encode ("utf-8"), font="Helvetica 18 bold", fg="white",
                              bg="purple")
               # canvas = Canvas (frame)
               img = ImageTk.PhotoImage (Image.open (download_cover (film['cover'], titel)))
               cover = tk.Label (frame, image=img)
               cover.image = img
               starttijdLabel = tk.Label (frame, text=starttijd.encode ("utf-8"), font="Helvetica 18 bold", fg="white",
                              bg="purple")
               eindtijdLabel = tk.Label (frame, text=eindtijd.encode ("utf-8"), font="Helvetica 18 bold", fg="white",
                                 bg="purple")
               zender = tk.Label (frame, text=film['zender'].encode ("utf-8"), font="Helvetica 18 bold", fg="white",
                               bg="purple")

               action_with_arg = partial (bied_aan, film['titel'], film['cover'], film['genre'], str (starttijd),
                                          str (eindtijd), aanbieder, date, row)

               action = partial(check_aanbieding,mycol, film['titel'], row, action_with_arg)

               action()

               cover.grid (row=row, column=1, sticky=tk.NW)
               titel.grid (row=row, column=2, sticky=tk.NW)
               starttijdLabel.grid (row=row, column=3, sticky=tk.NW)
               eindtijdLabel.grid (row=row, column=4, sticky=tk.NW)
               zender.grid (row=row, column=5, sticky=tk.NW)

               row += 1

       def myfunction(event):
           canvas.configure (scrollregion=canvas.bbox ("all"), width=1500, height=800)
       sizex = 800
       sizey = 600
       posx = 100
       posy = 100
       root.wm_geometry ("%dx%d+%d+%d" % (sizex, sizey, posx, posy))

       myframe = tk.Frame (self, relief=tk.GROOVE, width=50, height=100, bd=1)
       myframe.place (x=10, y=10)

       canvas = tk.Canvas (myframe, bg="Purple")
       frame = tk.Frame (canvas, bg="Purple")
       myscrollbar = tk.Scrollbar (myframe, orient="vertical", command=canvas.yview)
       canvas.configure (yscrollcommand=myscrollbar.set)

       myscrollbar.pack (side="right", fill="y")
       canvas.pack (side="left")
       canvas.create_window ((0, 0), window=frame, anchor='nw')
       frame.bind ("<Configure>", myfunction)
       data (aanbieder)

class OverzichtVanBezoekers(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)

       def download_cover(url, naam):
           name = (str (naam) + '.jpg')
           urllib.request.urlretrieve (url, name)

           return name

       date = time.strftime ("%d-%m-%Y")
       print (date)

       def data():
           print ('Connecting to database...')
           connection = pymongo.MongoClient ('ds159489.mlab.com', 59489)
           db = connection['thuisbioscoop']
           db.authenticate ("test123", "wachtwoord123")
           if db.is_mongos:
               print ('Connection successful.')
               mycol = db["bezoekers"]

               callstats = {"Aanbieder": aanbieder}

               findStats = mycol.find (callstats)

               titel = tk.Label (frame, text="Filmtitel")
               titel.grid (row=0, column=1, sticky=tk.NW)

               bezoeker = tk.Label (frame, text="Naam bezoeker")
               bezoeker.grid (row=0, column=2, sticky=tk.NW)

               code = tk.Label (frame, text="Code bezoeker")
               code.grid (row=0, column=3, sticky=tk.NW)

               row = 1

               for film in findStats:
                   titel = tk.Label (frame, text=film['Film'].encode ("utf-8"), font="Helvetica 18 bold", fg="blue", bg="purple")
                   bezoekernaam = tk.Label (frame, text=film['Naam'].encode ("utf-8"), font="Helvetica 18 bold", fg="red", bg="purple")
                   code = tk.Label (frame, text=film['code'].encode ("utf-8"), font="Helvetica 18 bold", fg="green", bg="purple")

                   titel.grid (row=row, column=1, sticky=tk.NW)
                   bezoekernaam.grid (row=row, column=2, sticky=tk.NW)
                   code.grid (row=row, column=3, sticky=tk.NW)

                   row += 1

       container = tk.Frame (self)
       container.pack (side="top", fill="both", expand=True)

       def myfunction(event):
           canvas.configure (scrollregion=canvas.bbox ("all"), width=1500, height=800)

       sizex = 800
       sizey = 600
       posx = 100
       posy = 100
       root.wm_geometry ("%dx%d+%d+%d" % (sizex, sizey, posx, posy))

       myframe = tk.Frame (self, relief=tk.GROOVE, width=50, height=100, bd=1)
       myframe.place (x=10, y=10)

       canvas = tk.Canvas (myframe, bg="Purple")
       frame = tk.Frame (canvas, bg="Purple")
       myscrollbar = tk.Scrollbar (myframe, orient="vertical", command=canvas.yview)
       canvas.configure (yscrollcommand=myscrollbar.set)

       myscrollbar.pack (side="right", fill="y")
       canvas.pack (side="left")
       canvas.create_window ((0, 0), window=frame, anchor='nw')
       frame.bind ("<Configure>", myfunction)

       data ()

class MainView(tk.Frame):
    global aanbieder
    aanbieder = None
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack (side="top", fill="both", expand=True)

        def set_menu(self):
            p1 = Homepage (self)
            p2 = FilmOverzichtBezoeker (self)
            p3 = FilmOverzichtAanbieder (self)
            p4 = RegistrerenAanbieder (self)
            p5 = LoginAanbieder (self)
            p6 = OverzichtVanBezoekers(self)

            p1.place (in_=container, x=0, y=0, relwidth=1, relheight=1)
            p2.place (in_=container, x=0, y=0, relwidth=1, relheight=1)
            p3.place (in_=container, x=0, y=0, relwidth=1, relheight=1)
            p4.place (in_=container, x=0, y=0, relwidth=1, relheight=1)
            p5.place (in_=container, x=0, y=0, relwidth=1, relheight=1)
            p6.place (in_=container, x=0, y=0, relwidth=1, relheight=1)

            if (menu == 0):
                menuBezoeker = tk.Menu (root)
                home = tk.Menu (menuBezoeker, tearoff=0)
                home.add_command (label="Home", command=p1.lift)
                menuBezoeker.add_cascade (label="Home", menu=home)

                films = tk.Menu (menuBezoeker, tearoff=0)
                films.add_command (label="Overzicht", command=p2.lift)
                menuBezoeker.add_cascade (label="Films", menu=films)

                aanbieders = tk.Menu (menuBezoeker, tearoff=0)
                aanbieders.add_command (label="Inloggen", command=p5.lift)
                aanbieders.add_command (label="Registreren", command=p4.lift)
                menuBezoeker.add_cascade (label="Inloggen/registreren aanbieders", menu=aanbieders)

                root.config (menu=menuBezoeker)

            elif (menu == 1):
                menuaanbieder = tk.Menu (root)
                home = tk.Menu (menuaanbieder, tearoff=0)
                home.add_command (label="Home", command=p1.lift)
                menuaanbieder.add_cascade (label="Home", menu=home)

                films = tk.Menu (menuaanbieder, tearoff=0)
                films.add_command (label="Bied een nieuwe film aan", command=p3.lift)
                menuaanbieder.add_cascade (label="Films", menu=films)

                bezoekers = tk.Menu (menuaanbieder, tearoff=0)
                bezoekers.add_command (label="Overzicht van bezoekers", command=p6.lift)
                menuaanbieder.add_cascade (label="Bezoekers", menu=bezoekers)

                root.config (menu=menuaanbieder)

            p1.show ()

        def check_password(hashed_password, user_password):
            password, salt = hashed_password.split (':')
            return password == hashlib.sha256 (salt.encode () + user_password.encode ()).hexdigest ()
        self.configure(bg="purple")

        global login
        def login(naam, wachtwoord):
            global aanbieder
            aanbieder = naam
            print ('Connecting to database...')
            connection = pymongo.MongoClient ('ds159489.mlab.com', 59489)
            db = connection['thuisbioscoop']
            db.authenticate ("test123", "wachtwoord123")
            if db.is_mongos:
                print ('Connection successful.')
                mycol = db["aanbieders"]

                callstats = {"Naam": naam}

                findStats = mycol.find_one(callstats)
                if(findStats and check_password (findStats["Wachtwoord"], wachtwoord)):
                    global menu
                    menu = 1
                    set_menu(self)
                    print(menu)

        set_menu(self)

if __name__ == "__main__":
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("1000x800")
    print(menu)
    root.mainloop()

    for p in Path (".").glob (".!mainview*.jpg"):
        p.unlink ()

    for s in Path (".").glob (".!frame*.jpg"):
        s.unlink ()
