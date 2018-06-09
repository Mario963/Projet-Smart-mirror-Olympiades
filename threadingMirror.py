#Executer en Python 3 !

#http://blog.goo.ne.jp/roboz80/e/16ea5be9a9eaf370046035be841b4bfd
#https://www.tutorialspoint.com/python/tk_anchors.htm
# smartmirror.py
# requirements
# requests, feedparser, traceback, Pillow



"""- début de la partie servant à l'importation des mocules/librairies de Python necessaires -"""
from tkinter import *
import threading
import speech_recognition as sr
import locale
import threading
import time
import requests
import json
import traceback
import feedparser

from PIL import Image, ImageTk
from contextlib import contextmanager
"""- fin de la partie servant à l'importation des mocules/librairies de Python necessaires -"""



"""- début de la partie servant au parametrage pour les differentes partie du Projet (heure, date police du texte, etc) -"""
LOCALE_LOCK = threading.Lock()

ui_locale = '' # e.g. 'fr_FR' fro French, '' as default
time_format = 24 # 12 or 24
date_format = "%d %B %Y" # check python doc for strftime() for options
news_country_code = 'fr'
weather_api_token = 'cfc41891406d753dc6e532e8d6baabe3' # create account at https://darksky.net/dev/
weather_lang = 'fr' # see https://darksky.net/dev/docs/forecast for full list of language parameters values
weather_unit = 'auto' # see https://darksky.net/dev/docs/forecast for full list of unit parameters values
latitude = None # Set this if IP location lookup does not work for you (must be a string)
longitude = None # Set this if IP location lookup does not work for you (must be a string)
xlarge_text_size = 50
large_text_size = 30
medium_text_size = 20
small_text_size = 12

@contextmanager
def setlocale(name): #thread proof function to work with locale
    with LOCALE_LOCK:
        saved = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, name)
        finally:
            locale.setlocale(locale.LC_ALL, saved)


#ici on liste les images qui seront utiliser par la partie "méteo" pour l'association des images en fonction de la météo #

# maps open weather icons to
# icon reading is not impacted by the 'lang' parameter
icon_lookup = {
    'clear-day': "assets/Sun.png",  # clear sky day
    'wind': "assets/Wind.png",   #wind
    'cloudy': "assets/Cloud.png",  # cloudy day
    'partly-cloudy-day': "assets/PartlySunny.png",  # partly cloudy day
    'rain': "assets/Rain.png",  # rain day
    'snow': "assets/Snow.png",  # snow day
    'snow-thin': "assets/Snow.png",  # sleet day
    'fog': "assets/Haze.png",  # fog day
    'clear-night': "assets/Moon.png",  # clear sky night
    'partly-cloudy-night': "assets/PartlyMoon.png",  # scattered clouds night
    'thunderstorm': "assets/Storm.png",  # thunderstorm
    'tornado': "assests/Tornado.png",    # tornado
    'hail': "assests/Hail.png"  # hail
}
"""- fin de la partie servant au parametrage pour les differentes partie du Projet (heure, date police du texte, etc) -"""



"""- Commentaires -"""
"""La quasi totalité des langage de programmation moderne comprennent ou sont des Langage Orienté Objet ( appelé aussi POO, Programmation Obrienté Objet)
Python en fait parti !
La programmation orienté objet, c’est un style de programmation qui permet de regrouper au même endroit le comportement (les fonctions) 
et les données (les structures) qui sont faites pour aller ensemble.

Dans la suite du programme nous allons utiliser des "classes"
Les classes sont, en Python, un moyen de definir un objet (paramètres , etc)
Un objet peut être n'importe quoi, l'objet est un moyen de dire à l'ordinateur que tel "chose" possède tel paramètres

Pour l'affichage j'utilise le module Tkinter, qui me permet de créer des interface graphiques
Tkinter dispose de nombreuse Widget(des elements graphiques) comme par exemple : le widget bouton, Canvas(espace dans laquelle il peut possible de dessiner ou d'écrire), 
widget input(demande à l'utilisateur de saisir un texte ou autres information)
Le widget Frame en fait parti, une Frame est un conteneur qui permet de separer les elements pour mieux organiser l'interface"""
"""- fin Commentaires -"""



"""- début de la partie servant à l'aafichage de l'heure et de la date -"""
class Clock(Frame):
    def __init__(self, parent, *args, **kwargs): 
        Frame.__init__(self, parent, bg='black')
        # initialize time label
        self.time1 = ''
        self.timeLbl = Label(self, font=('Helvetica', large_text_size), fg="cyan", bg="black")
        self.timeLbl.pack(side=TOP, anchor=E)
        # initialize day of week
        self.day_of_week1 = ''
        self.dayOWLbl = Label(self, text=self.day_of_week1, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.dayOWLbl.pack(side=TOP, anchor=E) # la méthode .pack() sert au placement du widget sans celà il ne sera pas affiché il en existe d'autre mais pack() est plus simple et facile à maîtriser
        # initialize date label
        self.date1 = ''
        self.dateLbl = Label(self, text=self.date1, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.dateLbl.pack(side=TOP, anchor=E)
        self.tick()

    def tick(self): # def... est utiliser pour definir une fonction 
        with setlocale(ui_locale):
            if time_format == 12:
                time2 = time.strftime('%I:%M %p') #hour in 12h format
            else:
                time2 = time.strftime('%H:%M') #hour in 24h format

            day_of_week2 = time.strftime('%A')
            date2 = time.strftime(date_format)
            # if time string has changed, update it
            if time2 != self.time1:
                self.time1 = time2
                self.timeLbl.config(text=time2)
            if day_of_week2 != self.day_of_week1:
                self.day_of_week1 = day_of_week2
                self.dayOWLbl.config(text=day_of_week2)
            if date2 != self.date1:
                self.date1 = date2
                self.dateLbl.config(text=date2)
            # calls itself every 200 milliseconds
            # to update the time display as needed
            # could use >200 ms, but display gets jerky
            self.timeLbl.after(200, self.tick)
"""-fin  de la partie servant à l'affichage de l'heure et de la date -"""



"""- début de la partie servant à l'affichage de la météo -"""
class Weather(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        self.temperature = ''
        self.forecast = ''
        self.location = ''
        self.currently = ''
        self.icon = ''
        self.degreeFrm = Frame(self, bg="black")
        self.degreeFrm.pack(side=TOP, anchor=W)
        self.temperatureLbl = Label(self.degreeFrm, font=('Helvetica', xlarge_text_size), fg="yellow", bg="black")
        self.temperatureLbl.pack(side=LEFT, anchor=N)
        self.iconLbl = Label(self.degreeFrm, bg="black")
        self.iconLbl.pack(side=LEFT, anchor=N, padx=20)
        self.currentlyLbl = Label(self, font=('Helvetica', medium_text_size), fg="white", bg="black")
        self.currentlyLbl.pack(side=TOP, anchor=W)
        self.forecastLbl = Label(self, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.forecastLbl.pack(side=TOP, anchor=W)
        self.locationLbl = Label(self, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.locationLbl.pack(side=TOP, anchor=W)
        self.get_weather()

    def get_ip(self):
        try:
            ip_url = "http://jsonip.com/"
            req = requests.get(ip_url)
            ip_json = json.loads(req.text)
            return ip_json['ip']
        except Exception as e:
            traceback.print_exc()
            return "Error: %s. Cannot get ip." % e

    def get_weather(self):
        try:

            if latitude is None and longitude is None:
                # get location
                location_req_url = "http://freegeoip.net/json/%s" % self.get_ip()
                r = requests.get(location_req_url)
                location_obj = json.loads(r.text)

                lat = location_obj['latitude']
                lon = location_obj['longitude']

                location2 = "%s, %s" % (location_obj['city'], location_obj['region_code'])

                # get weather
                weather_req_url = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" % (weather_api_token, lat,lon,weather_lang,weather_unit)
            else:
                location2 = ""
                # get weather
                weather_req_url = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" % (weather_api_token, latitude, longitude, weather_lang, weather_unit)

            r = requests.get(weather_req_url)
            weather_obj = json.loads(r.text)

            degree_sign= '\N{DEGREE SIGN}'
            temperature2 = "%s%s" % (str(int(weather_obj['currently']['temperature'])), degree_sign)
            currently2 = weather_obj['currently']['summary']
            forecast2 = weather_obj["hourly"]["summary"]

            icon_id = weather_obj['currently']['icon']
            icon2 = None

            if icon_id in icon_lookup:
                icon2 = icon_lookup[icon_id]

            if icon2 is not None:
                if self.icon != icon2:
                    self.icon = icon2
                    image = Image.open(icon2)
                    image = image.resize((100, 100), Image.ANTIALIAS)
                    image = image.convert('RGB')
                    photo = ImageTk.PhotoImage(image)

                    self.iconLbl.config(image=photo)
                    self.iconLbl.image = photo
            else:
                # remove image
                self.iconLbl.config(image='')

            if self.currently != currently2:
                self.currently = currently2
                self.currentlyLbl.config(text=currently2)
            if self.forecast != forecast2:
                self.forecast = forecast2
                self.forecastLbl.config(text=forecast2)
            if self.temperature != temperature2:
                self.temperature = temperature2
                self.temperatureLbl.config(text=temperature2)
            if self.location != location2:
                if location2 == ", ":
                    self.location = "Cannot Pinpoint Location"
                    self.locationLbl.config(text="Cannot Pinpoint Location")
                else:
                    self.location = location2
                    self.locationLbl.config(text=location2)
        except Exception as e:
            traceback.print_exc()
            print(("Error: %s. Cannot get weather." % e))

        self.after(600000, self.get_weather)

    @staticmethod
    def convert_kelvin_to_fahrenheit(kelvin_temp):
        return 1.8 * (kelvin_temp - 273) + 32
"""- fin de la partie servant à l'affichage de la météo -"""



"""- début de la partie servant à l'affichage des News -"""
class News(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.config(bg='black')
        #self.font.config(underline = 1)
        self.title = 'News' # 'News' is more internationally generic
        self.newsLbl = Label(self, text=self.title, font=('Helvetica', 18,'underline'), fg="lawn green", bg="black")
        self.newsLbl.pack(side=TOP, anchor=W)
        self.headlinesContainer = Frame(self, bg="black")
        self.headlinesContainer.pack(side=TOP)
        self.get_headlines()

    def get_headlines(self):
        try:
            # remove all children
            for widget in self.headlinesContainer.winfo_children():
                widget.destroy()
            if news_country_code == None:
                headlines_url = "https://news.google.com/news?ned=us&output=rss"
            else:
                headlines_url = "https://news.google.com/news?ned=%s&output=rss" % news_country_code

            feed = feedparser.parse(headlines_url)

            for post in feed.entries[0:5]:
                headline = NewsHeadline(self.headlinesContainer, post.title)
                headline.pack(side=TOP, anchor=W)
        except Exception as e:
            traceback.print_exc()
            print(("Error: %s. Cannot get news." % e))

        self.after(600000, self.get_headlines)


class NewsHeadline(Frame):
    def __init__(self, parent, event_name=""):
        Frame.__init__(self, parent, bg='black')

        image = Image.open("assets/Newspaper.png")
        image = image.resize((25, 25), Image.ANTIALIAS)
        image = image.convert('RGB')
        photo = ImageTk.PhotoImage(image)

        self.iconLbl = Label(self, bg='black', image=photo)
        self.iconLbl.image = photo
        self.iconLbl.pack(side=LEFT, anchor=N)

        self.eventName = event_name
        self.eventNameLbl = Label(self, text=self.eventName, font=('Helvetica', 10), fg="white", bg="black")
        self.eventNameLbl.pack(side=LEFT, anchor=N)
"""- fin de la partie servant à l'affichage des News -"""



"""- début de la partie servant à l'affichage du Calendrier -"""
class Calendar(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        self.title = 'Calendar Events'
        self.calendarLbl = Label(self, text=self.title, font=('Helvetica', 16,'underline'), fg="lawn green", bg="black")
        self.calendarLbl.pack(side=TOP, anchor=E)
        self.calendarEventContainer = Frame(self, bg='black')
        self.calendarEventContainer.pack(side=TOP, anchor=E)
        self.get_events()

    def get_events(self):
        #TODO: implement this method
        # reference https://developers.google.com/google-apps/calendar/quickstart/python

        # remove all children
        for widget in self.calendarEventContainer.winfo_children():
            widget.destroy()

        calendar_event = CalendarEvent(self.calendarEventContainer)
        calendar_event.pack(side=TOP, anchor=E)
        pass


class CalendarEvent(Frame):
    def __init__(self, parent, event_name="Event 1"):
        Frame.__init__(self, parent, bg='black')
        self.eventName = event_name
        self.eventNameLbl = Label(self, text=self.eventName, font=('Helvetica', 12), fg="white", bg="black")
        self.eventNameLbl.pack(side=TOP, anchor=E)
"""- fin de la partie servant à l'affichage du Calendrier -"""

"""- début de la partie servant pour la reconnaissance vocale -"""
class CommandeVocale(Frame):

        def __init__(self):          


                self.r = sr.Recognizer()
                
                self.recordAudio()


        def recordAudio(self):
                

                with sr.Microphone() as source:
                        

                        self.r.adjust_for_ambient_noise(source, duration = 1)

                        print("Parlez!")

                        self.audio = self.r.listen(source)

                        try:
                                
                                
                                self.commande = self.r.recognize_google(self.audio, language = "fr-FR")

                                print("Vous avez dit: " + self.commande)

                                self.commande = self.commande.lower()


                        except sr.UnknownValueError:
                                

                                print("Je n'ai pas compris! ")


                        except sr.RequestError as e:


                                print("Erreur! Vérifiez votre connexion Internet! ")

                        #return self.commande

"""- fin de la partie servant pour la reconnaissance vocale -"""




"""- début de la partie servant à l'affichage de l'interface dynamique que nous utiliserons -"""

class InterfaceDynamique(Frame):
    def __init__(self,parent,*args,**kwargs):
        Frame.__init__(self, parent, bg="black")
        self.title = "Home"
        self.InterfaceName = Label(self, text=self.title, font=('Helvetica', 30,'underline'), fg="lawn green", bg="black")
        self.InterfaceName.pack(side=TOP,anchor=W)
        self.InterfaceContainer = Frame(self, bg="black")
        self.InterfaceContainer.pack(anchor=CENTER)
        self.bouton = Button(self, text="Espace Santé", font=('Helvetica', 16), fg="lawn green", bg="black", command=self.modifier )
        self.bouton.pack(anchor=E)

    def modifier(self):
        self.InterfaceName.destroy()
        self.bouton.destroy()
        self.message = Label(self, text="Bienvenue dans votre espace santé", font=('Helvetica', 16,'underline'), fg="red", bg="black")
        self.message.pack(anchor=E, padx=100)
        self.messageSituation = Label(self, text="Voici votre situation actuelle",  font=('Helvetica', 16,'underline'), fg="red", bg="black")
        self.messageSituation.pack(anchor=E,padx=140)
        self.espace = Label(self, text="", bg="black")
        self.espace.pack()
        #Affichage du poids, âge....
        self.titre_IMC = Label(self, text="IMC: ", font=('Helvetica', 12), fg="white", bg="black")
        self.titre_IMC.pack(side=RIGHT, padx=10)
        self.titre_IMG = Label(self, text="IMG: ", font=('Helvetica', 12), fg="white", bg="black")
        self.titre_IMG.pack(side=RIGHT, padx=10)
        self.titre_poids = Label(self, text="Poids: ...kg", font=('Helvetica', 12), fg="white", bg="black")
        self.titre_poids.pack(side=RIGHT, padx=15)
        self.titre_sexe = Label(self, text="Sexe: ", font=('Helvetica', 12), fg="white", bg="black")
        self.titre_sexe.pack(side=RIGHT, padx=15)
        self.titre_taille = Label(self, text="Taille: ...cm", font=('Helvetica', 12), fg="white", bg="black")
        self.titre_taille.pack(side=RIGHT, padx=15)
        self.titre_age = Label(self, text="Age: ...ans", font=('Helvetica', 12), fg="white", bg="black")
        self.titre_age.pack(side=RIGHT, padx=15)

"""- fin de la partie servant à l'affichage de l'interface dynamique que nous utiliserons -"""



"""- début de la partie servant à l'affichage de toutes les informations precedentes dans l'interface Graphique de Tkinter -"""
class FullscreenWindow:
    def __init__(self):
        #cration et paramétrage de l'interface graphique
        self.tk = Tk()
        self.tk.configure(background='black')
        self.topFrame = Frame(self.tk, background = 'black')
        self.bottomFrame = Frame(self.tk, background = 'black')
        self.centerFrame = Frame(self.tk, background = "black")
        self.topFrame.pack(side = TOP, fill=BOTH, expand = YES)
        self.bottomFrame.pack(side = BOTTOM, fill=BOTH, expand = YES)
        self.centerFrame.pack(anchor=CENTER, fill=BOTH, expand = YES)
        self.state = False
        self.tk.bind("<Return>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)
        #interface
        self.interface = InterfaceDynamique(self.centerFrame)
        self.interface.pack(side=TOP, padx=100, pady=0)
        # clock
        self.clock = Clock(self.topFrame)
        self.clock.pack(side=RIGHT, anchor=N, padx=100, pady=60)
        # weather
        self.weather = Weather(self.topFrame)
        self.weather.pack(side=LEFT, anchor=N, padx=100, pady=60)
        # news
        self.news = News(self.bottomFrame)
        self.news.pack(side=LEFT, anchor=S, padx=100, pady=60)
        # calender - removing for now
        self.calender = Calendar(self.bottomFrame)
        self.calender.pack(side = RIGHT, anchor=S, padx=100, pady=60)

        

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"
"""- fin de la partie servant à l'affichage de toutes les informations precedentes dans l'interface Graphique de Tkinter -"""



w = FullscreenWindow()

#execution des threads
ThreadingFenetre = threading.Thread(target=FullscreenWindow).start()
ThreadingCommandeVocale = threading.Thread(target=CommandeVocale).start()

#boucle de la fenetre Tkinter
w.tk.mainloop()