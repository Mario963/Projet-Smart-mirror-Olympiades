#!/usr/bin/env python3
# -*-coding:Utf-8 -*
 
import speech_recognition as sr                     #On renomme la librairie "speech_recognition" par "sr", question de pratique

 
# Ici, on record l'audio

r = sr.Recognizer()                                 #On crée une variable "r" qui reprend la fonction "Recognizer" (voir doc)

with sr.Microphone() as source:                     #Ici on utilise la fonction "Microphone" afin d'indiquer au programme d'utiliser le micro par défault et on la désigne comme "source"

    print("Parlez")                                 #Affiche "Parlez" lorsque le programme est prêt à reçevoir de nouvelles commandes
    
    audio = r.listen(source, timeout = 10)          #On record l'audio grâce à la fonction "listen" de la "source", on stock ensuite l'audio dans la variable "audio"
    
 
# Partie reconnaissance vocale en utilisant l'API google

try:    #On essaye d'afficher ce que l'utilisateur a dit
    
#On utilise la fonction "recognize_google" qui prend les données de la variable "audio" et qui fait la reconnaissance vocale avec l'API Google, en indiquant la langue, ici le français
    
    print("Vous avez dit: " + r.recognize_google(audio, language = "fr-FR"))        #Donc si on traduit la ligne, cela nous donne: Affiche "Vous avez dit:" puis affiche ce que la fonction "recognize_google" renvoie
    


    
except sr.UnknownValueError:                                                                      #Si il y a l'erreur "UnknownValueError", on la relève
    
    print("Google Speech Recognition n'a pas compris ce que vous avez dit")                       #On affiche donc que comme quoi Google n'a pas compris
except sr.RequestError as e:                                                                      #Si il y a l'erreur "RequestError", on la relève et on la désigne comme "e"
    
    print("Could not request results from Google Speech Recognition service; {0}".format(e))      #On affiche qu'on ne peut pas récupérer les résultats des services Google
