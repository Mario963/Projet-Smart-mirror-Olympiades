#coding:utf-8

# mirroir.py
# requirements
# requests, feedparser, traceback, Pillow
# Pybluez

from Tkinter import *
import locale
import threading
import time
import requests
import json
import traceback
import feedparser
import subprocess
import os
from balance1 import *
#from jean1 import *

import time
import RPi.GPIO as GPIO
import random
subprocess.call('sudo pigpiod', shell= True)

from PIL import Image, ImageTk
from contextlib import contextmanager


LOCALE_LOCK = threading.Lock()

ui_locale = '' # e.g. 'fr_FR' fro French, '' as default
time_format = 24 # 12 or 24
date_format = "%d %B %Y" # check python doc for strftime() for options
news_country_code = 'fr'
weather_api_token = 'cfc41891406d753dc6e532e8d6baabe3' # create account at https://darksky.net/dev/
weather_lang = 'fr' # see https://darksky.net/dev/docs/forecast for full list of language parameters values
weather_unit = 'auto' # see https://darksky.net/dev/docs/forecast for full list of unit parameters values
latitude = 48.866667 # Set this if IP location lookup does not work for you (must be a string)
longitude = 2.333333 # Set this if IP location lookup does not work for you (must be a string)
xlarge_text_size = 94
large_text_size = 48
medium_text_size = 28
small_text_size = 18
chemin="./Desktop/smartmirrorFINAL-8/"
IMC = 0

@contextmanager
def setlocale(name): #thread proof function to work with locale
    with LOCALE_LOCK:
        saved = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, name)
        finally:
            locale.setlocale(locale.LC_ALL, saved)

# maps open weather icons to
# icon reading is not impacted by the 'lang' parameter
icon_lookup = {
    'clear-day': chemin + "assets/Sun.png",  # clear sky day
    'wind': chemin + "assets/Wind.png",   #wind
    'cloudy': chemin + "assets/Cloud.png",  # cloudy day
    'partly-cloudy-day': chemin + "assets/PartlySunny.png",  # partly cloudy day
    'rain': chemin + "assets/Rain.png",  # rain day
    'snow': chemin + "assets/Snow.png",  # snow day
    'snow-thin': chemin + "assets/Snow.png",  # sleet day
    'fog': chemin + "assets/Haze.png",  # fog day
    'clear-night': chemin + "assets/Moon.png",  # clear sky night
    'partly-cloudy-night': chemin + "assets/PartlyMoon.png",  # scattered clouds night
    'thunderstorm': chemin + "assets/Storm.png",  # thunderstorm
    'tornado': chemin + "assests/Tornado.png",    # tornado
    'hail': chemin + "assests/Hail.png"  # hail
    
}


    
    

class Sensor(Frame):
    import time
    import RPi.GPIO as GPIO
    def __init__(self,parent,*args,**kwargs):
        Frame.__init__(self, parent, bg='black')
        self.titre_Sante = Label(self, text= "", font=('Helvetica', 18), fg="lawn green", bg="black")
        self.titre_Sante.pack(anchor = CENTER)
        
        self.titre_IMC = Label(self, text= "" , font=('Helvetica', 12), fg="white", bg="black")
        self.titre_IMC.pack(anchor = CENTER)
        
        self.titre_IMG = Label(self, text="", font=('Helvetica', 12), fg="white", bg="black")
        self.titre_IMG.pack(anchor = CENTER)
        
        self.titre_poids = Label(self, text="", font=('Helvetica', 12), fg="white", bg="black")
        self.titre_poids.pack(anchor = CENTER)

        self.titre_aide = Label(self, text="", font=('Helvetica', 12), fg ="yellow", bg="black")
        self.titre_aide.pack(anchor = CENTER, side = LEFT)

        self.GPIO.setmode(self.GPIO.BOARD)

        self.Pin = 16
        self.long_press = 4
        self.press = 1
        self.GPIO.setup(self.Pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        print ("1 mesure de distance par le capteur ultrasonore HC-SR04")
        self.trigPin = 8
        self.echoPin = 10
        self.GPIO.setup(self.trigPin,self.GPIO.OUT)
        self.GPIO.setup(self.echoPin,self.GPIO.IN)
        GPIO.setwarnings(False)
        self.GPIO.output(self.trigPin, False)
        self.nombre_mesure = 1
        self.detection()

    def detection(self):

        #passage=0
        #self.passage=passage
        self.GPIO.setmode(self.GPIO.BOARD)
        self.trigPin = 8
        self.echoPin = 10
        self.GPIO.setup(self.trigPin,self.GPIO.OUT)
        self.GPIO.setup(self.echoPin,self.GPIO.IN)
        self.GPIO.output(self.trigPin, False)
        self.nombre_mesure = 1
        button_press_timer = 0
        self.Pin = 16
        self.long_press = 2
        self.press = 1
        self.GPIO.setup(self.Pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        for x in range(1):    #on mesure 3 fois
                          
          #time.sleep(1)  ## 1 seconde de délai entre chaque mesure

          self.GPIO.output(self.trigPin, True)     ## on envoie une brève impulsion sur la pin Trig
          time.sleep(0.15)
          self.GPIO.output(self.trigPin, False)

          while self.GPIO.input(self.echoPin)==0:  ## émission de l'ultrason
            self.debutImpulsion = time.time()

          while self.GPIO.input(self.echoPin)==1:   ## retour de l'écho
            self.finImpulsion = time.time()

          self.distance = round((self.finImpulsion - self.debutImpulsion) * 340 * 100 / 2, 1)  ## car vitesse du son = 340 m/s

          
          print ("Mesure ",self.nombre_mesure,": ",self.distance,"cm")    ## affichage à l'écran

          self.nombre_mesure += 1
          

        
        if self.distance >= 160:#executer si à la dixième mesure 50<= distance <=80
            


            print("aucune personne détectée !")
            #print("J'éteinds le miroir !")
            time.sleep(0.5)

            subprocess.call('xset dpms force off', shell=True)#mode off
            plein_ecran = FullscreenWindow
            plein_ecran.end_fullscreen

            

        else:

            
            subprocess.call('xset dpms force on', shell=True)#mode on
            plein_ecran = FullscreenWindow
            plein_ecran.toggle_fullscreen
            print("présence détectée !")

            #time.sleep(2)
            GPIO.setmode(GPIO.BOARD)
            self.Pin = 16

            if GPIO.input(self.Pin) == False:
                button_press_timer += 0.2 # ... on enregistre le temps que cela dure
            #else:
            if (button_press_timer > self.long_press) :
                print "very long press : ", button_press_timer
                subprocess.call(['sudo reboot "Reboot du systeme par bouton GPIO" &'], shell=True)
                
            elif (button_press_timer >= 0.1):
                print "short press : ", button_press_timer
                        
##                image = Image.open("picture/microphone.png")
##                image = image.resize((150, 150), Image.ANTIALIAS)
##                image = image.convert('RGB')
##                photo = ImageTk.PhotoImage(image)
##
##                self.pic = Label(self, image=photo)
##                self.pic.image = photo
##                self.pic.pack(anchor=CENTER)
                
                main()
                consigne = """Commandes:

Lancer un suivi santé : dites " santé "
Lancer la musique ou la radio : dites "lancer" ed Sheeran(track1) ou radio
Allumer les lumières facade : dites allumer les "lumières"
Allumer les led : dites allumer led (rouge ou bleu ou vert) 
Pour arreter un processus : dites eteint ou coupe  + lumière/led/musique/radio
En cas d'urgence : dites "arret d'urgence" """
                try:
                    machin = Aide[0]
                    if machin == 1:
                        self.titre_aide.config(text = consigne)
                except IndexError:
                    self.titre_aide.config(text="")
                    pass

                
                x = 1
                y= 0
            
                try:
                    if Commande[1] != None :

                        
                        lol1 = str(IMG_value)[1:-1]+"%"
                        lol2 =str(poids_value)[1:-1]+"kg"
                        if (len(lol1)> 1) :
                            
##                            pic = None
##                            pic2 = None

##                            if passage==0 :
##                                image = Image.open("picture/santer.png")
##                                image = image.resize((35, 35), Image.ANTIALIAS)
##                                image = image.convert('RGB')
##                                photo = ImageTk.PhotoImage(image)
##
##                                pic = Label(self, image=photo)
##                                pic.image = photo
##                                pic.pack(side=RIGHT, anchor = CENTER)
##
##                                pic2 = Label(self, image=photo)
##                                pic2.image = photo
##                                pic2.pack(side=LEFT, anchor = CENTER)
##                                passage+=1
##                            else:
##                                passage=0
                                
                            
                            self.titre_Sante.config(text = "Suivi Santé")
                            
                            self.titre_IMC.config(text=str(message_IMC)[2:-2] + str(IMC_value)[1:-1])
                            self.titre_IMG["text"] = str(message_IMG)[2:-2] + lol1#+"%"
                            self.titre_poids["text"] = "Poidds: "+lol2#+"kg"

                            

                            del message_IMC[:]
                            del message_IMG[:]
                            del IMC_value[:]
                            del IMG_value[:]
                            del poids_value[:]
                            
                        else:
                            self.titre_IMC.config(text=str(message_IMC)[2:-2] + str(IMC_value)[1:-1])
                            self.titre_IMG["text"] = ""
                            self.titre_poids["text"] = ""
                            self.titre_Sante.config(text="")

                    else:
                        self.titre_IMC.config(text=str(message_IMC)[2:-2] + str(IMC_value)[1:-1])
                        self.titre_IMG["text"] = ""
                        self.titre_poids["text"] = ""
                        self.titre_Sante.config(text="")

                        
                   


                        
                    
                    #effacer les listes pour ne pas afficher le message plusieurs fois:

                 
                        #GPIO.add_event_detect(self.Pin, GPIO.FALLING, callback=system_button, bouncetime=200)

                except IndexError:
                    self.titre_IMC.config(text=str(message_IMC)[2:-2] + str(IMC_value)[1:-1])
                    self.titre_IMG["text"] = str(message_IMG)[2:-2] + str(IMG_value)[1:-1]+""
                    self.titre_poids["text"] = " "+str(poids_value)[1:-1]+""


                button_press_timer = 0
                time.sleep(1)
                    
           
            #tout les 3 sec
        self.after(100, self.detection)

class Slogan(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        # initialize time label
        self.ms = ''
        self.msLbl = Label(self, text="ENJOY YOUR DAY", font=('Helvetica', medium_text_size), fg="cyan", bg="black")
        self.msLbl.pack(side=TOP, anchor=CENTER)  

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
        self.dayOWLbl.pack(side=TOP, anchor=E)
        # initialize date label
        self.date1 = ''
        self.dateLbl = Label(self, text=self.date1, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.dateLbl.pack(side=TOP, anchor=E)
        self.tick()

    def tick(self):
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
            return ("Error: %s. Cannot get ip." % e)

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

            degree_sign= u'\N{DEGREE SIGN}'
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
            print ("Error: %s. Cannot get weather." % e)

        self.after(600000, self.get_weather)

    @staticmethod
    def convert_kelvin_to_fahrenheit(kelvin_temp):
        return 1.8 * (kelvin_temp - 273) + 32


class News(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.config(bg='black')
        #self.font.config(underline = 1)
        self.title = 'Actualités' # 'News' is more internationally generic
        self.newsLbl = Label(self, text=self.title, font=('Helvetica', 18), fg="lawn green", bg="black")
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
                headlines_url = "https://news.google.com/news?ned=fr&output=rss"
            else:
                headlines_url = "https://news.google.com/news?ned=%s&output=rss" % news_country_code

            feed = feedparser.parse(headlines_url)

            for post in feed.entries[0:5]:
                headline = NewsHeadline(self.headlinesContainer, post.title)
                headline.pack(side=TOP, anchor=W)
        except Exception as e:
            traceback.print_exc()
            print ("Error: %s. Cannot get news." % e)

        self.after(600000, self.get_headlines)


class NewsHeadline(Frame):
    def __init__(self, parent, event_name=""):
        Frame.__init__(self, parent, bg='black')

        image = Image.open("./Desktop/smartmirrorFINAL-8/assets/Newspaper.png")
        image = image.resize((15, 20), Image.ANTIALIAS)
        image = image.convert('RGB')
        photo = ImageTk.PhotoImage(image)

        self.iconLbl = Label(self, bg='black', image=photo)
        self.iconLbl.image = photo
        self.iconLbl.pack(side=LEFT, anchor=N)

        self.eventName = event_name
        self.eventNameLbl = Label(self, text=self.eventName, font=('Helvetica', 8), fg="white", bg="black")
        self.eventNameLbl.pack(side=LEFT, anchor=S)



class Picture(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        nombre = random.randrange(1,5)
        #nombre = 2


        
        if nombre == 1:
            self.title = "Proverbe"
            self.titre = Label(self, text=self.title, font=('Helvetica', 17), fg = "lawn green", bg = "black")
            self.titre.pack(side=TOP, anchor = CENTER)
            
            image = Image.open(chemin+"picture/muhammad.jpg")
            image = image.resize((100, 100), Image.ANTIALIAS)
            image = image.convert('RGB')
            photo = ImageTk.PhotoImage(image)
            icone = Label(self, image = photo, bg="black")
            icone.image = photo
            icone.pack(anchor=CENTER)


            citation = """Les religions contiennent
toutes les mêmes vérités"""

            phrase = Label(self, text=citation, font=('Helvetica', 7),bg="black", fg="white")
            phrase.pack(side=TOP, anchor=CENTER)




        if nombre == 2:
            self.title = "Proverbe"
            self.titre = Label(self, text=self.title, font=('Helvetica', 17), fg = "lawn green", bg = "black")
            self.titre.pack(side=TOP, anchor = CENTER)

            image = Image.open(chemin+"picture/happy.jpg")
            image = image.resize((100, 100), Image.ANTIALIAS)
            image = image.convert('RGB')
            photo = ImageTk.PhotoImage(image)
            icone = Label(self, image = photo, bg="black")
            icone.image = photo
            icone.pack(anchor=CENTER)
            
	    citation = """La seul façon de prédire
l’avenir est de le créer"""
	    phrase = Label(self, text=citation, font=('Helvetica', 7),bg="black", fg="white")
	    phrase.pack(side=TOP, anchor=CENTER)






        if nombre == 3:
            self.title = "Proverbe du jour"
            self.titre = Label(self, text=self.title, font=('Helvetica', 12), fg = "lawn green", bg = "black")
            self.titre.pack(side=TOP, anchor = CENTER)

            image = Image.open(chemin+"picture/YES.png")
            image = image.resize((100, 100), Image.ANTIALIAS)
            image = image.convert('RGB')
            photo = ImageTk.PhotoImage(image)
            icone = Label(self, image = photo, bg="black")
            icone.image = photo
            icone.pack(anchor=CENTER)
            
            
	    citation = """Celui qui veut réussir
trouve toujours un moyen"""
	    phrase = Label(self, text=citation, font=('Helvetica', 7),bg="black", fg="white")
	    phrase.pack(side=TOP, anchor=CENTER)



        if nombre == 4:
            self.title = "Savez vous ?"
            self.titre = Label(self, text=self.title, font=('Helvetica', 16), fg = "lawn green", bg = "black")
            self.titre.pack(side=TOP, anchor = CENTER)
        
            image = Image.open(chemin +"picture/rocher.jpg")
            image = image.resize((100, 100), Image.ANTIALIAS)
            image = image.convert('RGB')
            photo = ImageTk.PhotoImage(image)

            self.pic = Label(self, image=photo)
            self.pic.image = photo
            self.pic.pack(anchor=CENTER)

            message = """En France, une commune
s'appelle Rocher en Ardèche"""

            self.message = Label(self, text = message, font=('Helvetica', 7), fg="white", bg="black")
            self.message.pack(side=TOP, anchor=CENTER)
        


    
class Balance(Frame):
    def __init__(self, parent, event_name="Event 1"):
        Frame.__init__(self, parent, bg='black')

        image = Image.open(chemin +"picture/santer.png")
        image = image.resize((35, 35), Image.ANTIALIAS)
        image = image.convert('RGB')
        photo = ImageTk.PhotoImage(image)

        self.pic = Label(self, image=photo)
        self.pic.image = photo
        self.pic.pack(side=RIGHT, anchor = CENTER)

        self.pic2 = Label(self, image=photo)
        self.pic2.image = photo
        self.pic2.pack(side=LEFT, anchor = CENTER)
        
        self.title = "Suivi Santé"
        self.balance = Label(self, text=self.title, font=('Helvetica', 16), fg="lawn green", bg="black")
        self.balance.pack(side=TOP, anchor=CENTER)

        
class FullscreenWindow:

    def __init__(self):
        self.tk = Tk()
        self.tk.configure(background='black')
        self.topFrame = Frame(self.tk, background = 'black')
        self.bottomFrame = Frame(self.tk, background = 'black')
        self.centerFrame = Frame(self.tk, background = "black")
        self.topFrame.pack(side = TOP, fill=BOTH, expand = YES)
        self.bottomFrame.pack(side = BOTTOM, fill=BOTH, expand = YES)
        self.centerFrame.pack(side=TOP, fill=BOTH, expand= YES)
        self.state = False
        self.toggle_fullscreen()
        #self.tk.bind("<Return>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)

        # clock
        self.clock = Clock(self.topFrame)
        self.clock.pack(side=RIGHT, anchor=NE, padx=0, pady=30)
        # MESSAGE SLOGAN
        self.slogan = Slogan(self.centerFrame)
        self.slogan.pack(side=TOP, anchor=N, padx=0, pady=0)
        # weather
        self.weather = Weather(self.topFrame)
        self.weather.pack(side=LEFT, anchor=N, padx=0, pady=30)



        # news
        self.news = News(self.bottomFrame)
        self.news.pack(side=LEFT, anchor=S, padx=0, pady=30)
        # picture
        self.picture = Picture(self.bottomFrame)
        self.picture.pack(side=RIGHT, anchor=SW, padx=0, pady=30)
        # health monitoring
        #self.balance = Balance(self.centerFrame)
        #self.balance.pack(anchor = CENTER)

        #Sensor
        self.sensor = Sensor(self.centerFrame)
        self.sensor.pack()

        #Button
        #self.button = Button(self.centerFrame)
        #self.button.pack()




        #self.messageSysteme = Label(self.centerFrame, text = "Age= ?")
        #self.messageSysteme.pack()

        #self.messageSysteme2 = Label(self.centerFrame, text="Sexe=?")
        #self.messageSysteme2.pack()

        #self.messageSysteme3 = Label(self.centerFrame, text="Taille=?")
        #self.messageSysteme3.pack()



        #self.bouton = Bouton(self.centerFrame)
        #self.bouton.pack()



        
      

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"

if __name__ == '__main__':
    w = FullscreenWindow()
    w.tk.mainloop()


