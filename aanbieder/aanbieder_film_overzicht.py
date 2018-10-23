import tkinter as tk
import requests
import xmltodict
import time
from datetime import datetime
from tkinter import *
from tkinter.tix import *
import urllib.request
from PIL import Image, ImageTk

date = time.strftime("%d-%m-%Y")

api_url = 'http://api.filmtotaal.nl/filmsoptv.xml?apikey=djg2nqcl4jpkwivqgjdox3klob4zyx3d&dag='+str(date)+'&sorteer=0'
response = requests.get(api_url)

filmXML = xmltodict.parse(response.text)
print('Dit zijn de films die vandaag en morgen te zien zijn: \n')

def download_cover(url, naam):
    name=(str(naam) + '.jpg')
    urllib.request.urlretrieve(url, name)

    return name

date = time.strftime("%d-%m-%Y")
print(date)

def data():
    api_url = 'http://api.filmtotaal.nl/filmsoptv.xml?apikey=djg2nqcl4jpkwivqgjdox3klob4zyx3d&dag=' + str (
        date) + '&sorteer=0'
    response = requests.get (api_url)

    filmXML = xmltodict.parse (response.text)
    print ('Dit zijn de films die vandaag en morgen te zien zijn: \n')

    row = 0

    for film in filmXML['filmsoptv']['film']:
        titel = Label (frame, text=film['titel'].encode("utf-8"), fg="white", bg="purple")
        canvas = Canvas (frame)
        img = ImageTk.PhotoImage (Image.open (download_cover (film['cover'], titel)))
        cover = Label (frame, image=img)
        cover.image = img
        genre = Label (frame, text=film['genre'].encode("utf-8"), fg="white", bg="purple")
        zender = Label (frame, text=film['zender'].encode("utf-8"), fg="white", bg="purple")

        cover.grid (row=row, column=1, sticky=NW)
        titel.grid (row=row, column=2, sticky=NW)
        genre.grid (row=row, column=3, sticky=NW)
        zender.grid (row=row, column=4, sticky=NW)

        st = int (film['starttijd'])
        starttijd = (datetime.utcfromtimestamp (st).strftime ('%m-%d %H:%M'))

        et = int (film['eindtijd'])
        eindtijd = (datetime.utcfromtimestamp (et).strftime ('%m-%d %H:%M'))

        row += 1


def myfunction(event):
    canvas.configure(scrollregion=canvas.bbox("all"),width=1000,height=800)

root=Tk()
sizex = 800
sizey = 600
posx  = 100
posy  = 100
root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))

myframe=Frame(root,relief=GROOVE,width=50,height=100,bd=1)
myframe.place(x=10,y=10)

canvas=Canvas(myframe, bg="Purple")
frame=Frame(canvas, bg="Purple")
myscrollbar=Scrollbar(myframe,orient="vertical",command=canvas.yview)
canvas.configure(yscrollcommand=myscrollbar.set)

myscrollbar.pack(side="right",fill="y")
canvas.pack(side="left")
canvas.create_window((0,0),window=frame,anchor='nw')
frame.bind("<Configure>",myfunction)
data()
root.mainloop()