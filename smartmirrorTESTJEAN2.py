# smartmirror.py
# requirements
# requests, feedparser, traceback, Pillow

from tkinter import *
import locale
import threading
import time
import requests
import json
import traceback
import feedparser
import speech_recognition as sr                     #On renomme la librairie "speech_recognition" par "sr", question de pratique
import re

r = sr.Recognizer()

class recordAudio(Frame):

    def __init__(self,parent, *arg, **kwargs):
        Frame.__init__(self,parent, bg="black")
        self.commande = ''
        
        self.test()
        
    def test(self):
        
        with sr.Microphone() as source:

            r.adjust_for_ambient_noise(source, duration=0.5)

            print("PARLEZ")
            
            audio = r.listen(source)
    
        try:
      
            self.commande = r.recognize_google(audio, language = "fr-FR")        
            self.commande = self.commande.lower()

            print(self.commande)

         
        except sr.UnknownValueError:                                                   
    
            print("Je n'ai pas compris ce que vous avez dit")   
    
        except sr.RequestError as e:
    
            print("Erreur lors de la reconnaissance vocale; vérifiez que vous êtes bien connecté à internet", e)
        
        
class FullscreenWindow:

    def __init__(self):
        self.tk = Tk()
        self.tk.configure(background='black')
        self.topFrame = Frame(self.tk, background = 'black')
        self.bottomFrame = Frame(self.tk, background = 'black')
        self.topFrame.pack(side = TOP, fill=BOTH, expand = YES)
        self.bottomFrame.pack(side = BOTTOM, fill=BOTH, expand = YES)
        self.state = False
        self.tk.bind("<Return>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)
        
        self.test = recordAudio(self.topFrame)
        self.test.pack(side=RIGHT, anchor=N, padx=100, pady=60)
        
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

