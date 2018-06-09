#!/usr/bin/env python
#coding:utf-8
#sudo kill $(pgrep omxplayer)  TERMINATE SONG


# on importe les librairies necessaires
import collections
import time
import bluetooth # sous Py3 c'est "socket" mais pb de syntaxe
import sys
import subprocess
import speech_recognition as sr                     #On renomme la librairie "speech_recognition" par "sr", question de pratique
import re
#from jean1 import *
from mirroir2 import *
import os
import signal

                               #On crée une variable "r" qui reprend la fonction "Recognizer" (voir doc)

CONTINUOUS_REPORTING = "04"  # Easier as string with leading zero

COMMAND_REPORTING = 12
COMMAND_REQUEST_STATUS = 15
COMMAND_REGISTER = 16
COMMAND_READ_REGISTER = 17

#input is Wii device to host
INPUT_STATUS = 20
INPUT_READ_DATA = 21

EXTENSION_8BYTES = 32
#end "hex" values

BUTTON_DOWN_MASK = 8

TOP_RIGHT = 0
BOTTOM_RIGHT = 1
TOP_LEFT = 2
BOTTOM_LEFT = 3

BLUETOOTH_NAME = "Nintendo RVL-WBC-01" #le nom de la balance ( info bluetooth )
Commande = []
r = sr.Recognizer()
reload(sys)
sys.setdefaultencoding("utf-8")
def led_santerouge():
    subprocess.call('sudo pigs p 22 255', shell = True)
    time.sleep(0.1)
    subprocess.call('sudo pigs p 22 0', shell = True)
    time.sleep(0.1)
    subprocess.call('sudo pigs p 22 255', shell = True)
    time.sleep(0.1)
    subprocess.call('sudo pigs p 22 0', shell = True)

def led_santebleu():
    subprocess.call('sudo pigs p 17 255', shell = True)
    time.sleep(0.1)
    subprocess.call('sudo pigs p 17 0', shell = True)
    time.sleep(0.1)
    subprocess.call('sudo pigs p 17 255', shell = True)
    time.sleep(0.1)
    subprocess.call('sudo pigs p 17 0', shell = True)
def led_santevert():
    subprocess.call('sudo pigs p 27 255', shell = True)
    time.sleep(0.1)
    subprocess.call('sudo pigs p 27 0', shell = True)
    time.sleep(0.1)
    subprocess.call('sudo pigs p 27 255', shell = True)
    time.sleep(0.1)
    subprocess.call('sudo pigs p 27 0', shell = True)

def led_santeoff():
    subprocess.call('sudo pigs p 22 0', shell = True)
    subprocess.call('sudo pigs p 17 0', shell = True)
    subprocess.call('sudo pigs p 27 0', shell = True)
    #time.sleep(0.25)
    
    
def recognizeSante():
    del Commande[:]
    time.sleep(1)
    commande = ""
    reload(sys)
    sys.setdefaultencoding("utf-8")
    led_santevert()
##    with sr.Microphone() as source:         
##            led_santeoff()
##            led_sante()
##            r.adjust_for_ambient_noise(source, duration=1)  #Appel à une fonction pour ajuster la sensibilité du microphone en fonction du volume sonore ambient
##            r.pause_threshold = 0.8
##            print("Dite age/sexe/taille")                                 #Affiche "Parlez" lorsque le programme est prêt à reçevoir de nouvelles commandes
##
##            
##        
##            audio = r.listen(source, phrase_time_limit = 5)          #La variable "audio" stock ce que la fonction "listen" renvoie c'est-à-dire ce que l'utilisateur dit à la "source"
##     
##    # Partie reconnaissance vocale en utilisant l'API google
##
##           
##    try:    #On essaye d'afficher ce que l'utilisateur a dit
##
##            
##        
##        commande = r.recognize_google(audio, language = "fr-FR")    #La variable "commande" s'attribue ce que la fonction recognize_google renvoie
##        print("Vous avez dit: " + commande)
##        
##    except sr.UnknownValueError:                                                                      #Si il y a l'erreur "UnknownValueError", on la relève, lorsque l'audio n'est pas compréhensible
##        commande = "trsd"
##        print("Je n'ai pas compris ce que vous avez dit")                       #On affiche donc que comme quoi Google n'a pas compris
##        pass
##
##    except sr.RequestError as e:                                                                      #Si il y a l'erreur "RequestError", on la relève et on la désigne comme "e", lorsque la connection internet est désactivée ou si les identifiants ne sont pas valides
##
##        print("Erreur lors de la reconnaissance vocale; vérifiez que vous êtes bien connecté à internet", e)      #On affiche qu'on ne peut pas récupérer les résultats des services Google, puis on affiche la raison juste après en renomant l'erreur "e"
##
##    
    while 1:
        with sr.Microphone() as source:

            

            r.adjust_for_ambient_noise(source, duration=1)  #Appel à une fonction pour ajuster la sensibilité du microphone en fonction du volume sonore ambient
            r.pause_threshold = 0.8
            led_santeoff()
            
            print("Dite age/sexe/taille!!!!!!")
            
            
        
            audio = r.listen(source, phrase_time_limit = 5)          #La variable "audio" stock ce que la fonction "listen" renvoie c'est-à-dire ce que l'utilisateur dit à la "source"
        try:

            commande = r.recognize_google(audio, language = "fr-FR")    #La variable "commande" s'attribue ce que la fonction recognize_google renvoie
            print("Vous avez dit: " + commande)

        except sr.UnknownValueError:                                                                      #Si il y a l'erreur "UnknownValueError", on la relève, lorsque l'audio n'est pas compréhensible
            commande = "fjifj"
            print("Je n'ai pas compris ce que vous avez dit")                       #On affiche donc que comme quoi Google n'a pas compris
            pass

        except sr.RequestError as e:                                                                      #Si il y a l'erreur "RequestError", on la relève et on la désigne comme "e", lorsque la connection internet est désactivée ou si les identifiants ne sont pas valides

            print("Erreur lors de la reconnaissance vocale; vérifiez que vous êtes bien connecté à internet", e)      #On affiche qu'on ne peut pas récupérer les résultats des services Google, puis on affiche la raison juste après en renomant l'erreur "e"

            
        if "ans" in commande:
            print("1")
            pass
            if "homme" in commande:
                print("2")
                pass
            elif "femme" in commande:
                pass
            
            if "mesure" or "mètre" in commande:
                print("3")
                break

        else:
            led_santerouge()
    led_santebleu()    
    if "ans" in commande:   
        commande = commande.split()
        index = commande.index("ans")
        index = index - 1
        age_jean = int(commande[index])
        Commande.append(age_jean)
        print(Commande)
##        if age_jean =<100:
##            test = 1
##        else:
##            test = 101
##            pass
    if "homme" in commande:
        sexe_jean = 1
        print (sexe_jean)
        Commande.append(sexe_jean)

        print(Commande)
        
    elif "femme" in commande:
        sexe_jean = 0
        print (sexe_jean)
        Commande.append(sexe_jean)

        print(Commande)

    if "mesure" in commande:
        #taille_jean = int(re.findall('\d+',commande)[1])
        #if taille_jean == 1:
            #taille_jean = int(re.findall('\d+',commande)[2])
        index2 = commande.index("mesure")
        index2 = index2 +3
        taille_jean = int(commande[index2]) + 100
        print(taille_jean)
        Commande.append(taille_jean)

        print(Commande)
          
            
    if "mètre" in commande:
        
        index3 = commande.index("mètre")
        index3 = index3 +1
        taille_jean = int(commande[index3]) + 100
        print(taille_jean)
        Commande.append(taille_jean)

        print(Commande)

##    while test >100:
##        subprocess.call('sudo pigs p 22 0', shell = True)
##        subprocess.call('sudo pigs p 17 0', shell = True)
##        subprocess.call('sudo pigs p 27 0', shell = True)
##        


    else:
        pass

#########PARTIE SANTE SALIM#########
statut_sante = []    
def Sante():
       
       time.sleep(5)
       print("Lancement de la partie santé!")
       print("La liste contient:", Commande)
       processor = EventProcessor()
       address = "00:1F:C5:A1:FC:E0" 
       board = Wiiboard(processor)
       if len(sys.argv) == 1: #Si dans la liste des arguments il y en a 1 
           print ("Appuyez sur le bouton sync rouge SVP ...")
        
       else:
           address = sys.argv[1] #Sinon si utilisateur entre une commande du type : balance.py <address mac>
       try:
            #Deconnexion de tout les appareils bluetooth au prealable connecter pour eviter des bugs
            #Disconnect already-connected devices.
            # This is basically Linux black magic just to get the thing to work.
           subprocess.check_output(["bluez-test-input", "disconnect", address], stderr=subprocess.STDOUT)
           subprocess.check_output(["bluez-test-input", "disconnect", address], stderr=subprocess.STDOUT)
       except:
           pass
       led_santebleu()
       print ("En cours de connexion...")

       board.wait(5000) # Pose de 5sec pour que l'utilisateur appuie sur le bouton sync
       erreur = False
       try :
           board.connect(address)
       except:
           erreur = True
           pass

       if erreur == True :
           pass

        
       else:
           led_santeoff()
           board.receive()
            
            
           if address is None:
               print("Aucun suivi ne peut etre fait")
               pass
           else:    
                print ('Vous pesez actuellement:'), processor.weight,'KG'

                ########### JEAN VALUE ###########
                try :
                    taille = Commande[2]#int(taille_jean)
                    poids = processor.weight
                    sexe = Commande[1]#int(sexe_jean) # Pour femme ==0 Pour homme == 1
                    age = Commande[0]#int(age_jean)
                    print("taille:", taille)
                    print("age:", age)
                    print("sexe:", sexe)
                except IndexError:
                    pass
                
                #type(taille)
                
                ########### END JEAN VALUE ###########
                
                IMC = monitoring_IMC(taille, poids)
                IMC_value.append(IMC)
                

                IMG = monitoring_IMG(IMC, age, sexe)
                IMG_value.append(IMG)

                poids_value.append(poids)
                statut_sante.append(1)
                board.disconnect()
                

sauvegarde = []

##########RECONNAISSANCE PRINCIPALE APRES LE MAIN##########
Aide = []
def recordAudio():
    del Aide[:]
    commande = ""

    while 1:
        
        
        with sr.Microphone() as source:         

            r.adjust_for_ambient_noise(source, duration=1)  #Appel à une fonction pour ajuster la sensibilité du microphone en fonction du volume sonore ambient
            r.pause_threshold = 0.8
            led_santebleu()
            print("Parlez")                                 #Affiche "Parlez" lorsque le programme est prêt à reçevoir de nouvelles commandes

            audio = r.listen(source, phrase_time_limit = 5)          #La variable "audio" stock ce que la fonction "listen" renvoie c'est-à-dire ce que l'utilisateur dit à la "source
        
        try:
            
            commande = r.recognize_google(audio, language = "fr-FR")
            print("Vous avez dit: " + commande)
            sauvegarde.append(commande)
            commande = commande.lower()

####CONDITION POUR AIDE UTILISATEUR####
            if "aide" in commande:
                truc = 1
                Aide.append(truc)
                print(Aide)
                break
####CONDITION POUR REDEMARRAGE RASPBERRY#####
            if "urgen" in commande:
               subprocess.call(['sudo reboot "Reboot du systeme par bouton GPIO" &'], shell=True)
                
            
####CONDITION POUR SANTE####
            
            if "santé" in commande:
               recognizeSante()
               print(Commande)
               Sante()
               break
            
            if "tente" in commande:
               recognizeSante()
               print(Commande)
               Sante()
               break

####CONDITION POUR FERMER UN PROCESSUS OU ETEINDRE LES LED####
            
            if "étein" in commande:
                if "led" in commande:
                     subprocess.call('sudo pigs p 22 0', shell = True)
                     subprocess.call('sudo pigs p 17 0', shell = True)
                     subprocess.call('sudo pigs p 27 0', shell = True)
                     
                if "lumière" in commande:
                    subprocess.call('sudo pigs p 26 0', shell = True)

                if "radio" in commande:
                
                    subprocess.call('sudo killall chromium-browser', shell = True)
                    
                if "musique" in commande:
                    try:
                        os.killpg(os.getpgid(p.pid), signal.SIGTERM)
                    
                    except UnboundLocalError:
                        subprocess.call('sudo kill $(pgrep omxplayer)', shell = True)

                break
            
            if "coupe" in commande:
                if "radio" in commande:
                
                    subprocess.call('sudo killall chromium-browser', shell = True)
                    
                
                if "musique" in commande:
                    try:
                        os.killpg(os.getpgid(p.pid), signal.SIGTERM)
                    
                    except UnboundLocalError:
                        subprocess.call('sudo kill $(pgrep omxplayer)', shell = True)
                         
                break

####CONDITION POUR ALLUMER LES LED####
            
            if "lumière" in commande:
                subprocess.call('sudo pigs p 26 100', shell = True) #GPIO 26 BLANC
                break
                
            if "led" in commande:
                
                if "rouge" in commande:
                    subprocess.call('sudo pigs p 22 255', shell = True) #GPIO 27 ROUGE

                if "bleu" in commande:
                    subprocess.call('sudo pigs p 17 255', shell = True) #GPIO 22 BLEU
                
                if "vert" in commande:
                    subprocess.call('sudo pigs p 27 255', shell = True) #GPIO 17 VERT
                
                if "verte" in commande:
                    subprocess.call('sudo pigs p 27 255', shell = True) #GPIO 17 VERT
                    
                break

            if "lettre" in commande:
                
                if "rouge" in commande:
                    subprocess.call('sudo pigs p 22 255', shell = True) #GPIO 27 ROUGE

                if "bleu" in commande:
                    subprocess.call('sudo pigs p 17 255', shell = True) #GPIO 22 BLEU
                
                if "vert" in commande:
                    subprocess.call('sudo pigs p 27 255', shell = True) #GPIO 17 VERT
                
                if "verte" in commande:
                    subprocess.call('sudo pigs p 27 255', shell = True) #GPIO 17 VERT
                    
                break

            if "laine" in commande:
                
                if "rouge" in commande:
                    subprocess.call('sudo pigs p 22 255', shell = True) #GPIO 27 ROUGE

                if "bleu" in commande:
                    subprocess.call('sudo pigs p 17 255', shell = True) #GPIO 22 BLEU
                
                if "vert" in commande:
                    subprocess.call('sudo pigs p 27 255', shell = True) #GPIO 17 VERT
                
                if "verte" in commande:
                    subprocess.call('sudo pigs p 27 255', shell = True) #GPIO 17 VERT
                    
                break
####CONDITIONS POUR LANCER UN PROCESSUS (MUSIQUE / RADIO)####
                
            if "lance" in commande:       
                if "sheeran" in commande:
                    p = subprocess.Popen(['omxplayer /home/pi/Desktop/chanson1.mp3 '], stdin=subprocess.PIPE, shell=True, preexec_fn=os.setsid)#stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    
                if "chirac" in commande:
                    p = subprocess.Popen(['omxplayer /home/pi/Desktop/chanson1.mp3 '], stdin=subprocess.PIPE, shell=True, preexec_fn=os.setsid)#stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    
                        
                if "radio" in commande:
                    subprocess.call("sudo nohup chromium-browser --no-sandbox --app=http://icecast.skyrock.net/s/natio_mp3_128k&", shell = True)

                break
            if "sheeran" in commande:
                p = subprocess.Popen(['omxplayer /home/pi/Desktop/chanson1.mp3 '], stdin=subprocess.PIPE, shell=True, preexec_fn=os.setsid)#stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                break 
            if "chirac" in commande:
                p = subprocess.Popen(['omxplayer /home/pi/Desktop/chanson1.mp3 '], stdin=subprocess.PIPE, shell=True, preexec_fn=os.setsid)#stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                break  

            if "met" in commande:       
                if "sheeran" in commande:
                    p = subprocess.Popen(['omxplayer /home/pi/Desktop/chanson1.mp3 '], stdin=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
                   
                if "chirac" in commande:
                    p = subprocess.Popen(['omxplaye /home/pi/Desktop/chanson1.mp3'], stdin=subprocess.PIPE, shell=True, preexec_fn=os.setsid)#stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    
                        
                if "radio" in commande:
                    subprocess.call("sudo nohup chromium-browser --no-sandbox --app=http://icecast.skyrock.net/s/natio_mp3_128k&", shell = True)
                break
            
            if "mé" in commande:       
                if "sheeran" in commande:
                    p = subprocess.Popen(['omxplayer /home/pi/Desktop/chanson1.mp3 '], stdin=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
                   
                if "chirac" in commande:
                    p = subprocess.Popen(['omxplayer /home/pi/Desktop/chanson1.mp3 '], stdin=subprocess.PIPE, shell=True, preexec_fn=os.setsid)#stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    
                        
                if "radio" in commande:
                    subprocess.call("sudo nohup chromium-browser --no-sandbox --app=http://icecast.skyrock.net/s/natio_mp3_128k&", shell = True)
                break


        except sr.UnknownValueError:                                                                      #Si il y a l'erreur "UnknownValueError", on la relève, lorsque l'audio n'est pas compréhensible

            print("Je n'ai pas compris ce que vous avez dit")                       #On affiche donc que comme quoi Google n'a pas compris
            pass

        except sr.RequestError as e:                                                                      #Si il y a l'erreur "RequestError", on la relève et on la désigne comme "e", lorsque la connection internet est désactivée ou si les identifiants ne sont pas valides

            print("Erreur lors de la reconnaissance vocale; vérifiez que vous êtes bien connecté à internet", e)      #On affiche qu'on ne peut pas récupérer les résultats des services Google, puis on affiche la raison juste après en renomant l'erreur "e"


class EventProcessor:
    def __init__(self):
        self._measured = False
        self.done = False
        self._events = []

    def mass(self, event):
        if event.totalWeight > 10: #le poid doit etre superieur a 10kg
            self._events.append(event.totalWeight)
            if not self._measured:
                print ("Veuillez patienter je mesure...")
                self._measured = True
        elif self._measured:
            self.done = True

    @property
    def weight(self):
        if not self._events:
            return 0
        histogram = collections.Counter(round(num, 1) for num in self._events)
        return histogram.most_common(1)[0][0]


class BoardEvent:
    def __init__(self, topLeft, topRight, bottomLeft, bottomRight):

        self.topLeft = topLeft
        self.topRight = topRight
        self.bottomLeft = bottomLeft
        self.bottomRight = bottomRight
        #convenience value
        self.totalWeight = topLeft + topRight + bottomLeft + bottomRight # on additionne les 4 capteurs ( jauges de contraintes )


class Wiiboard:
    def __init__(self, processor):
        # Sockets and status
        self.receivesocket = None
        self.controlsocket = None

        self.processor = processor
        self.calibration = []
        self.calibrationRequested = False
        self.address = None
        self.buttonDown = False
        for i in xrange(3):
            self.calibration.append([])
            for j in xrange(4):
                self.calibration[i].append(10000)  # high dummy value so events with it don't register

        self.status = "Déconnexion"
        self.lastEvent = BoardEvent(0, 0, 0, 0)

        try:
            self.receivesocket = bluetooth.BluetoothSocket(bluetooth.L2CAP)
            self.controlsocket = bluetooth.BluetoothSocket(bluetooth.L2CAP)
            
        except ValueError:
            raise Exception("Erreur: Bluetooth non trouver")

    def isConnected(self): #Fonction verification connecter
        return self.status == "Connecter"
    
    def isnotConnected(self): #Fonction verification deconnecter
        if self.status == "Deconnecter":
            print("Probleme de connexion a la Wiiboard")
            sys.exit()

    # Connect to the Wiiboard at bluetooth address <address>
    
    def connect(self, address): #Fonction connecter la balance
        if address is None:
            print ("Adresse inexistante veuillez vérifier)")
            return

        self.receivesocket.connect((address, 0x13)) #utilisation du module bluetooth l.89 : 
        self.controlsocket.connect((address, 0x11)) #utilisateur du module bluetooth l.90 :
        
        
        if self.receivesocket and self.controlsocket:
            print ("Connecter a la Wiiboard --> addresse : ") + address
            self.status = "Connecter"
            self.address = address
            self.calibrate()
            useExt = ["00", COMMAND_REGISTER, "04", "A4", "00", "40", "00"]
            self.send(useExt)
            self.setReportingType()
            print ("Wiiboard connecter")
        else:
            sys.exit()
            print ("Impossible de se connecter à la Wiiboard --> addresse :") + address
    

    def receive(self):
        #try:
        #   self.receivesocket.settimeout(0.1)       #not for windows?
        while self.status == "Connecter" and not self.processor.done:
            data = self.receivesocket.recv(25)
            intype = int(data.encode("hex")[2:4])
            if intype == INPUT_STATUS:
                # TODO: Status input received. It just tells us battery life really
                self.setReportingType()
            elif intype == INPUT_READ_DATA:
                if self.calibrationRequested:
                    packetLength = (int(str(data[4]).encode("hex"), 16) / 16 + 1)
                    self.parseCalibrationResponse(data[7:(7 + packetLength)])

                    if packetLength < 16:
                        self.calibrationRequested = False
            elif intype == EXTENSION_8BYTES:
                self.processor.mass(self.createBoardEvent(data[2:12]))
            else:
                led_santebleu()
                print ("C'est partit vous pouvez vous pesez !")

        self.status = "Deconnecter"
        self.disconnect()
        led_santeoff()

    def disconnect(self): #Fonction pour deconnecter la balance
        if self.status == "Connecter":
            self.status = "En cours de Deconnexion"
            while self.status == "En cours de Deconnexion":
                self.wait(100)
        try:
            self.receivesocket.close() #Appel du module bluetooth fonction close
        except:
            pass
        try:
            self.controlsocket.close() #Appel du module bluetooth fonction close
        except:
            pass
        print ("Balance deconnecter")

    def createBoardEvent(self, bytes):
        bytes = bytes[2:12]

        rawTR = (int(bytes[0].encode("hex"), 16) << 8) + int(bytes[1].encode("hex"), 16)
        rawBR = (int(bytes[2].encode("hex"), 16) << 8) + int(bytes[3].encode("hex"), 16)
        rawTL = (int(bytes[4].encode("hex"), 16) << 8) + int(bytes[5].encode("hex"), 16)
        rawBL = (int(bytes[6].encode("hex"), 16) << 8) + int(bytes[7].encode("hex"), 16)

        topLeft = self.calcMass(rawTL, TOP_LEFT)
        topRight = self.calcMass(rawTR, TOP_RIGHT)
        bottomLeft = self.calcMass(rawBL, BOTTOM_LEFT)
        bottomRight = self.calcMass(rawBR, BOTTOM_RIGHT)
        boardEvent = BoardEvent(topLeft, topRight, bottomLeft, bottomRight)
        return boardEvent

    def calcMass(self, raw, pos):
        val = 0.0
        #calibration[0] is calibration values for 0kg
        #calibration[1] is calibration values for 17kg
        #calibration[2] is calibration values for 34kg
        if raw < self.calibration[0][pos]:
            return val
        elif raw < self.calibration[1][pos]:
            val = 17 * ((raw - self.calibration[0][pos]) / float((self.calibration[1][pos] - self.calibration[0][pos])))
        elif raw > self.calibration[1][pos]:
            val = 17 + 17 * ((raw - self.calibration[1][pos]) / float((self.calibration[2][pos] - self.calibration[1][pos])))

        return val

    def getEvent(self):
        return self.lastEvent


    def parseCalibrationResponse(self, bytes):
        index = 0
        if len(bytes) == 16:
            for i in xrange(2):
                for j in xrange(4):
                    self.calibration[i][j] = (int(bytes[index].encode("hex"), 16) << 8) + int(bytes[index + 1].encode("hex"), 16)
                    index += 2
        elif len(bytes) < 16:
            for i in xrange(4):
                self.calibration[2][i] = (int(bytes[index].encode("hex"), 16) << 8) + int(bytes[index + 1].encode("hex"), 16)
                index += 2

    # Send <data> to the Wiiboard
    # <data> should be an array of strings, each string representing a single hex byte
    def send(self, data):
        if self.status != "Connecter":
            return
        data[0] = "52"

        senddata = ""
        for byte in data:
            byte = str(byte)
            senddata += byte.decode("hex")

        self.controlsocket.send(senddata)


    def calibrate(self):
        message = ["00", COMMAND_READ_REGISTER, "04", "A4", "00", "24", "00", "18"]
        self.send(message)
        self.calibrationRequested = True

    def setReportingType(self):
        bytearr = ["00", COMMAND_REPORTING, CONTINUOUS_REPORTING, EXTENSION_8BYTES]
        self.send(bytearr)

    def wait(self, millis): #Fonction attente
        time.sleep(millis / 1000.0)

#### TKINTER VARIABLE ####
IMC_value = []
IMG_value = []
poids_value = []
message_IMG = []
message_IMC = []
#### TKINTER VARIABLE ####

def monitoring_IMC(taille, poids): # Fonction pour calculer l'IMC

     
    taille = int(taille)
    
    poids = float(poids)
    
    print("taille imc:", taille)
    print("poids IMC:", poids)

    IMC = poids/((float(taille)/100)**2) 

    IMC = float(IMC)
    IMC = round(IMC,1)
    
    print("IMC:", IMC)

    if IMC < 16.5:
        messageIMC = "Vous etes anorexique, avec un IMC de "

    elif IMC >= 16.5 and IMC < 18.5:
        messageIMC = "Vous etes maigre, avec un IMC de "

    elif IMC >= 18.5 and IMC < 25:
        messageIMC = "Vous etes normal, avec un IMC de "

    elif IMC >= 25 and IMC < 30:
        messageIMC = "Vous etes en surpoids, avec un IMC de "  

    elif IMC >= 30 and IMC < 35:
        messageIMC = "Vous etes en obesite moderer, avec un IMC de "    

    elif IMC >= 35 and IMC <40:
        messageIMC = "Vous etes en obesite elevee, avec un IMC de "

    elif IMC > 40:
        messageIMC = "Vous etes en obesite morbide, avec un IMC de "
    else: 
        messageIMC = "Erreur de calcul de l'IMC"    

    message_IMC.append(messageIMC)
    print(message_IMC)    

    return IMC

def monitoring_IMG(IMC,age,sexe): # Fonction pour calculer l'IMG
    IMC = round(IMC,1)
    IMG = (1.20*IMC)+(0.23*age)-(10.8-sexe)-5.4
    IMG = round(IMG,1)

    if sexe == 1:
        if IMG < 25:
            messageIMG = " Taux de graisse normal de "

        elif IMG >= 25 and IMG < 30:
            messageIMG = "Taux de graisse legerement superieur a la normal : " 

        elif IMG >= 30:
            messageIMG = "Taux de graisse important de "

        else :
            messageIMG = "Erreur de calcul IMG ( Pb : Sexe ) "    

    if sexe == 0 :
        if IMG < 15:
            messageIMG ="Taux de graisse normal de "   

        elif IMG >= 15 and IMG < 20:
            messageIMG = "Taux de graisse legerement superieur a la normal : "   

        elif IMG >= 20:
            messageIMG = "Taux de graisse important de "    

        else :
            messageIMG = "Erreur de calcul IMG ( Pb : Sexe ) "  
    print("IMG= ", IMG)
    message_IMG.append(messageIMG)
    print(message_IMG)    

    return IMG
    

def main():
    recordAudio()
       
if __name__ == "__main__":
    main() # Ici on execute la fonction (main) comme programme principale
    print(IMC_value)
    print(IMG_value)

