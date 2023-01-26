import tkinter as tk
import subprocess as sub
import threading
#import RPi.GPIO as GPIO
import csv
from time import sleep
from tkinter import *
from tkinter import messagebox
from datetime import datetime
from functools import partial

#Vars

AFlasks = ["error", "Flasche 1", "Flasche 2", "Flasche 3", "Flasche 4"]
AProcent = [0,0,0,0,0]
Player = []
Weight = []
Gender = []
LastDrink = []
nrDrinks = []
promille = []
Drink = [0,0,0,0,0]
UpdateSB = [0,0]

#Methods

def toggleKeyboard(event):
    #sub.call(['/usr/bin/toggle-keyboard.sh'])
    return

def showFlask(count, button):   
    def submitFlask():
        try:
            float(EAlk.get())

            if len(EName.get()) != 0:
                AFlasks[count] = EName.get()
                AProcent[count] = float(EAlk.get())
                button["text"] = AFlasks[count]
                toggleKeyboard("<FocusIn>")
                flask.destroy()

            else:
                messagebox.showwarning("showwarning", "Bitte einen Namen eingeben")
                flask.attributes("-topmost", True)
                flask.attributes("-topmost", False)

        except:
            messagebox.showwarning("showwarning", "Bitte einene Zahl als Alkoholgehalt eingeben")
            flask.attributes("-topmost", True)
            flask.attributes("-topmost", False)

        return

    flask = tk.Toplevel(FFlasks)
    flask.geometry("+200+50")

    LName = tk.Label(flask, text = "Name der Flasche "+str(count)+": ")
    LName["font"] = "Arial 34 bold"
    EName = tk.Entry(flask)
    EName["font"] = "Arial 34"
    EName.bind("<FocusIn>", toggleKeyboard)
    
    LAlk = tk.Label(flask, text = "Alkoholgehalt der Flasche "+str(count)+": ")
    LAlk["font"] = "Arial 34 bold"
    EAlk = tk.Entry(flask)
    EAlk["font"] = "Arial 34"

    BSubmit = tk.Button(flask, text = "Ok", command = submitFlask)
    BSubmit["font"] = "Arial 34 bold"
    
    LName.pack()
    EName.pack()
    LAlk.pack()
    EAlk.pack()
    BSubmit.pack()
    return

def showWindowNewPlayer():            
    def submitplayer():
        if len(EName.get()) != 0:
            if len(EGewicht.get()) != 0:
                try:
                    int(EGewicht.get())

                    if gender.get() != 0:
                        Player.append(EName.get())
                        Weight.append(int(EGewicht.get()))
                        Gender.append(gender.get())

                        LastDrink.append(datetime.strptime("0001-01-01 00:00:00.0", '%Y-%m-%d %H:%M:%S.%f'))
                        nrDrinks.append(0)
                        promille.append(0)
                        ClearPrintScoreBoard()
                        toggleKeyboard("<FocusIn>")
                        NewPlayer.destroy()

                    else:
                        messagebox.showwarning("showwarning", "Bitte einen Geschlecht waehlen")
                        NewPlayer.attributes("-topmost", True)
                        NewPlayer.attributes("-topmost", False)

                except:
                    messagebox.showwarning("showwarning", "Bitte einene Zahl als Gewicht eingeben")
                    NewPlayer.attributes("-topmost", True)
                    NewPlayer.attributes("-topmost", False)

            else:
                messagebox.showwarning("showwarning", "Bitte einen Gewicht eingeben")
                NewPlayer.attributes("-topmost", True)
                NewPlayer.attributes("-topmost", False)

        else:
            messagebox.showwarning("showwarning", "Bitte einen Namen eingeben")
            NewPlayer.attributes("-topmost", True)
            NewPlayer.attributes("-topmost", False)

        return

    NewPlayer = tk.Toplevel(FGame)
    NewPlayer.geometry("+250+50")

    LName = tk.Label(NewPlayer, text = "Name:")
    LName["font"] = "Arial 34 bold"
    EName = tk.Entry(NewPlayer)
    EName["font"] = "Arial 34 bold"
    EName.bind("<FocusIn>", toggleKeyboard)

    LGewicht = tk.Label(NewPlayer, text = "Gewicht:")
    LGewicht["font"] = "Arial 34 bold"
    EGewicht = tk.Entry(NewPlayer)
    EGewicht["font"] = "Arial 34 bold"

    LGeschlecht = tk.Label(NewPlayer, text = "Geschlecht:")
    LGeschlecht["font"] = "Arial 34 bold"
    
    gender = DoubleVar()
    CBmale = tk.Radiobutton(NewPlayer, indicatoron = 0, text = "Maenlich", variable = gender, value = 0.7)
    CBmale["font"] = "Arial 34 bold"
    CBfemale = tk.Radiobutton(NewPlayer, indicatoron = 0, text = "Weiblich", variable = gender, value = 0.6)
    CBfemale["font"] = "Arial 34 bold"

    BSubmit = tk.Button(NewPlayer, text = "Ok", command = submitplayer)
    BSubmit["font"] = "Arial 34 bold" 
    
    LName.pack()
    EName.pack()
    LGewicht.pack()
    EGewicht.pack()
    LGeschlecht.pack()
    CBmale.pack()
    CBfemale.pack()
    BSubmit.pack()
    return

def showWindowNewDrink():
    def nextFrameDrink():
        def submitdrink():
            Drink[1] = SF1.get()
            Drink[2] = SF2.get()
            Drink[3] = SF3.get()
            Drink[4] = SF4.get()

            if 0 < Drink[1] + Drink[2] + Drink[3] + Drink[4] <= 100:
                makedrink()
                activePlayer = Player.index(LBPlayers.get("active"))

                if activePlayer > -1:
                    UpdateSB[0] = activePlayer
                    LastDrink[activePlayer] = datetime.now()

                    #Alk im glas
                    GetrunkenerAlk = 0
                    if SF1.get() > 0 and AProcent[1] > 0:
                        GetrunkenerAlk += (Drink[0] * (SF1.get() / 100)) * (AProcent[1] / 100)
                    if SF2.get() > 0 and AProcent[2] > 0:
                        GetrunkenerAlk += (Drink[0] * (SF2.get() / 100)) * (AProcent[2] / 100)
                    if SF3.get() > 0 and AProcent[3] > 0:
                        GetrunkenerAlk += (Drink[0] * (SF3.get() / 100)) * (AProcent[3] / 100)
                    if SF4.get() > 0 and AProcent[4] > 0:
                        GetrunkenerAlk += (Drink[0] * (SF4.get() / 100)) * (AProcent[4] / 100)

                    #Alk von ml in g
                    GetrunkenerAlk = GetrunkenerAlk * 0.8
                    Promille = GetrunkenerAlk / (Weight[activePlayer] * Gender[activePlayer])
                    Promille += promille[activePlayer]
                    Promille = round(Promille, 3)

                    UpdateSB[1] = Promille
                    updateScoreBoard()

                    UpdateSB[0] = 0
                    UpdateSB[1] = 0

                NewDrink.destroy()
                nextFrameDrink.destroy()

            else:
                messagebox.showwarning("showwarning", "Bitte Werte eingeben die kleiner 101 und groesser 0 sind")
                nextFrameDrink.attributes("-topmost", True)
                nextFrameDrink.attributes("-topmost", False)
            
            return
        
        if Drink[0] == 0 or Player.index(LBPlayers.get("active")) < 0:
            messagebox.showwarning("showwarning", "Bitte Einen Player und eine Glasgroesse auswaehlen")
            NewDrink.attributes("-topmost", True)
            NewDrink.attributes("-topmost", False)
            return
            

        nextFrameDrink = tk.Toplevel(NewDrink)
        nextFrameDrink.attributes('-fullscreen', True)
    
        LFlask1 = tk.Label(nextFrameDrink, text = AFlasks[1] + ": ")
        LFlask1["font"] = "Arial 34"
        SF1 = tk.Scale(nextFrameDrink, from_ = 0, to = 100, orient = tk.HORIZONTAL, resolution = 10)
        SF1["font"] = "Arial 34 bold"
        SF1["length"] = 300

        LFlask2 = tk.Label(nextFrameDrink, text = AFlasks[2] + ": ")
        LFlask2["font"] = "Arial 34"
        SF2 = tk.Scale(nextFrameDrink, from_ = 0, to = 100, orient = tk.HORIZONTAL, resolution = 10)
        SF2["font"] = "Arial 34 bold"
        SF2["length"] = 300

        LFlask3 = tk.Label(nextFrameDrink, text = AFlasks[3] + ": ")
        LFlask3["font"] = "Arial 34"
        SF3 = tk.Scale(nextFrameDrink, from_ = 0, to = 100, orient = tk.HORIZONTAL, resolution = 10)
        SF3["font"] = "Arial 34 bold"
        SF3["length"] = 300

        LFlask4 = tk.Label(nextFrameDrink, text = AFlasks[4] + ": ")
        LFlask4["font"] = "Arial 34"
        SF4 = tk.Scale(nextFrameDrink, from_ = 0, to = 100, orient = tk.HORIZONTAL, resolution = 10)
        SF4["font"] = "Arial 34 bold"
        SF4["length"] = 300

        BSubmit = tk.Button(nextFrameDrink, text = "Ok", command = submitdrink)
        BSubmit["font"] = "Arial 34 bold"

        LFlask1.grid(row = 2, column = 0)
        SF1.grid(row = 2, column = 1, columnspan = 3)
        LFlask2.grid(row = 3, column = 0)
        SF2.grid(row = 3, column = 1, columnspan = 3)
        LFlask3.grid(row = 4, column = 0)
        SF3.grid(row = 4, column = 1, columnspan = 3)
        LFlask4.grid(row = 5, column = 0)
        SF4.grid(row = 5, column = 1, columnspan = 3)
        BSubmit.grid(row = 6, column = 0, columnspan = 4, pady = 30)

    def selected500ml():
        Drink[0] = 500
        B100["bg"] = "lightgrey"
        B100["activebackground"] = "lightgrey"
        B250["bg"] = "lightgrey"
        B250["activebackground"] = "lightgrey"
        B500["bg"] = "#00FF00"
        B500["activebackground"] = "#00FF00"
        return

    def selected250ml():
        Drink[0] = 250
        B100["bg"] = "lightgrey"
        B100["activebackground"] = "lightgrey"
        B250["bg"] = "#00FF00"
        B250["activebackground"] = "#00FF00"
        B500["bg"] = "lightgrey"
        B500["activebackground"] = "lightgrey"
        return

    def selected100ml():
        Drink[0] = 100
        B100["bg"] = "#00FF00"
        B100["activebackground"] = "#00FF00"
        B250["bg"] = "lightgrey"
        B250["activebackground"] = "lightgrey"
        B500["bg"] = "lightgrey"
        B500["activebackground"] = "lightgrey"
        return

    if AFlasks[1] == "Flasche 1" and AFlasks[2] == "Flasche 2" and AFlasks[3] == "Flasche 3" and AFlasks[4] == "Flasche 4":
        messagebox.showwarning("showwarning", "Bitte zuerst Flaschen einpflegen")
        return

    NewDrink = tk.Toplevel(FNewDrink)
    NewDrink.attributes('-fullscreen', True)
    
    LName = tk.Label(NewDrink, text = "Player: ")
    LName["font"] = "Arial 34"

    LBPlayers = tk.Listbox(NewDrink)
    LBPlayers["font"] = "Arial 34"
    for item in Player:
        LBPlayers.insert(tk.END, item)

    LGlas = tk.Label(NewDrink, text = "Glasgroesse: ")
    LGlas["font"] = "Arial 34"

    B100 = tk.Button(NewDrink, text = "100ml", command = selected100ml)
    B100["font"] = "Arial 34 bold"
    B250 = tk.Button(NewDrink, text = "250ml", command = selected250ml)
    B250["font"] = "Arial 34 bold"
    B500 = tk.Button(NewDrink, text = "500ml", command = selected500ml)
    B500["font"] = "Arial 34 bold"
    
    Bnext = tk.Button(NewDrink, text = "Next", command = nextFrameDrink)
    Bnext["font"] = "Arial 34 bold"
    
    scrollbar1 = Scrollbar(NewDrink)
    scrollbar1.config(command = LBPlayer.yview)
    LBPlayer.config(yscrollcommand = scrollbar1.set)

    LName.grid(row = 0, column = 0)
    LBPlayers.grid(row = 0, column = 1, columnspan = 3)
    scrollbar1.grid(row = 0, column = 5)
    LGlas.grid(row = 1, column = 0)
    B100.grid(row = 1, column = 1)
    B250.grid(row = 1, column = 2)
    B500.grid(row = 1, column = 3)
    Bnext.grid(row = 1, column = 4)
    return

def updateScoreBoard():
    nrDrinks[UpdateSB[0]] += 1
    promille[UpdateSB[0]] = UpdateSB[1]
    ClearPrintScoreBoard()
    return

def ClearPrintScoreBoard():
    LBPlayer.delete(0, tk.END)
    LBDrinks.delete(0, tk.END)
    LBPromille.delete(0, tk.END)
    idx = 0
    while idx < len(Player):
        LBPlayer.insert(tk.END, Player[idx])
        LBDrinks.insert(tk.END, nrDrinks[idx])
        LBPromille.insert(tk.END, promille[idx])
        idx += 1
    updateHTML()
    return

def updateHTML():
    #File = open('/var/www/html/index.html', 'w')
    #File.write('<!DOCTYPE html><html><body>')
    #File.write('<h1 style="font-size:800%;">Scoreboard:</h1>')
    #File.write('<font size="200%"><table border="5px" cellpadding="20px">')
    #File.write('<tr><td>Player:</td><td>Drinks:</td><td>Promille:</td></tr>')
    #for item in range(len(Player)):
    #    File.write('<tr><td>'+Player[item]+'</td><td>'+str(nrDrinks[item])+'</td><td>'+str(promille[item])+'</td></tr>')
    #File.write('</table></font>')
    #File.close()
    saveScoreboard()
    return

def saveScoreboard():
    #File = open('/home/pi/Desktop/score.csv', 'w')
    File = open('C:/Users/max-g/Desktop/score.csv', 'w')
    for item in range(len(Player)):
        File.write(Player[item]+";"+str(Weight[item])+";"+str(Gender[item])+";"+str(LastDrink[item])+";"+str(nrDrinks[item])+";"+str(promille[item])+";\n")
    File.close()
    return

def makedrink():
    size = Drink[0]
    
    timepercl = 2
    saugtime = 5
    
    cl1 = round(size/1000 * Drink[1])
    cl2 = round(size/1000 * Drink[2])
    cl3 = round(size/1000 * Drink[3])
    cl4 = round(size/1000 * Drink[4])
    
    pump1 = 17
    pump2 = 23
    pump3 = 27
    pump4 = 22
    
    pump1duration = timepercl*cl1
    pump2duration = timepercl*cl2
    pump3duration = timepercl*cl3
    pump4duration = timepercl*cl4

    #GPIO.setmode(GPIO.BCM)
    #GPIO.setup(pump1, GPIO.OUT)
    #GPIO.setup(pump2, GPIO.OUT)
    #GPIO.setup(pump3, GPIO.OUT)
    #GPIO.setup(pump4, GPIO.OUT)

    #GPIO.output(pump1, GPIO.HIGH)
    #GPIO.output(pump2, GPIO.HIGH)
    #GPIO.output(pump3, GPIO.HIGH)
    #GPIO.output(pump4, GPIO.HIGH)

    if cl1 > 0: pump1duration += saugtime
    if cl2 > 0: pump2duration += saugtime
    if cl3 > 0: pump3duration += saugtime
    if cl4 > 0: pump4duration += saugtime

    while pump1duration > 0 or pump2duration > 0 or pump3duration > 0 or pump4duration > 0:

        print(pump1duration)
        print(pump2duration)
        print(pump3duration)
        print(pump4duration)

        if pump1duration > 0:
            #GPIO.output(pump1, GPIO.LOW)
            print("Pump1 on")
            pump1duration -= 1

        else:
            #GPIO.output(pump1, GPIO.HIGH)
            print("Pump1 off")

        if pump2duration > 0:
            #GPIO.output(pump2, GPIO.LOW)
            print("Pump2 on")
            pump2duration -= 1

        else:
            #GPIO.output(pump2, GPIO.HIGH)
            print("Pump2 off")
        
        if pump3duration > 0:
            #GPIO.output(pump3, GPIO.LOW)
            print("Pump3 on")
            pump3duration -= 1

        else:
            #GPIO.output(pump3, GPIO.HIGH)
            print("Pump3 off")
        
        if pump4duration > 0:
            #GPIO.output(pump4, GPIO.LOW)
            print("Pump4 on")
            pump4duration -= 1

        else:
            #GPIO.output(pump4, GPIO.HIGH)
            print("Pump4 off")
            
        sleep(1)
    
    #GPIO.cleanup()
    return

#GUI
root = tk.Tk()
root.attributes('-fullscreen', True)

#Flaschen Buttons
FFlasks = tk.Frame(root)

BF1 = tk.Button(FFlasks, text = AFlasks[1])
BF1.configure(command=partial(showFlask, 1, BF1))
BF1["font"] = "Arial 34 bold"
BF1["height"] = 1
BF1["width"] = 8

BF2 = tk.Button(FFlasks, text = AFlasks[2])
BF2.configure(command=partial(showFlask, 2, BF2))
BF2["font"] = "Arial 34 bold"
BF2["height"] = 1
BF2["width"] = 8

BF3 = tk.Button(FFlasks, text = AFlasks[3])
BF3.configure(command=partial(showFlask, 3, BF3))
BF3["font"] = "Arial 34 bold"
BF3["height"] = 1
BF3["width"] = 8

BF4 = tk.Button(FFlasks, text = AFlasks[4])
BF4.configure(command=partial(showFlask, 4, BF4))
BF4["font"] = "Arial 34 bold"
BF4["height"] = 1
BF4["width"] = 8

FFlasks.pack()
BF4.pack(side = tk.RIGHT)
BF3.pack(side = tk.RIGHT)
BF2.pack(side = tk.RIGHT)
BF1.pack(side = tk.RIGHT)

#Game
FGame = tk.Frame(root)

#AddPlayer
BAddPlayer = tk.Button(FGame, text = "Add Player +", command = showWindowNewPlayer)
BAddPlayer["font"] = "Arial 34 bold"
BAddPlayer["height"] = 1

#Scoreboeard
LPlayer = tk.Label(FGame, text = "Player:")
LPlayer["font"] = "Arial 34 bold"
LBPlayer = tk.Listbox(FGame)
LBPlayer["font"] = "Arial 34"
LBPlayer["width"] = 12
LBPlayer["height"] = 6
scrollbar = Scrollbar(FGame)

LDrinks = tk.Label(FGame, text = "Drinks:")
LDrinks["font"] = "Arial 34 bold"
LBDrinks = tk.Listbox(FGame)
LBDrinks["font"] = "Arial 34"
LBDrinks["width"] = 6
LBDrinks["height"] = 6

LPromille = tk.Label(FGame, text = "Promille:")
LPromille["font"] = "Arial 34 bold"
LBPromille = tk.Listbox(FGame)
LBPromille["font"] = "Arial 34"
LBPromille["width"] = 6
LBPromille["height"] = 6

#Game Pack
FGame.pack(side = tk.RIGHT)
BAddPlayer.grid(row = 0, column = 0, columnspan = 3, pady = 20)
LPlayer.grid(row = 1, column = 0)
LDrinks.grid(row = 1, column = 1)
LPromille.grid(row = 1, column = 2)
LBPlayer.grid(row = 2, column = 0)
scrollbar.grid(row = 2, column = 3)
LBDrinks.grid(row = 2, column = 1)
LBPromille.grid(row = 2, column = 2)

def OnVsb(*args):
    LBPlayer.yview(*args)
    LBDrinks.yview(*args)
    LBPromille.yview(*args)
    return

def OnMouseWheel(event):
    LBPlayer.yview("scroll", event.delta,"units")
    LBDrinks.yview("scroll", event.delta,"units")
    LBPromille.yview("scroll", event.delta,"units")
    return "break"

scrollbar.config(command = OnVsb)
LBPlayer.config(yscrollcommand = scrollbar.set)
LBPlayer.bind("<MouseWheel>", OnMouseWheel)
LBDrinks.config(yscrollcommand = scrollbar.set)
LBDrinks.bind("<MouseWheel>", OnMouseWheel)
LBPromille.config(yscrollcommand = scrollbar.set)
LBPromille.bind("<MouseWheel>", OnMouseWheel)

#New Drink
FNewDrink = tk.Frame(root)
BNewDrink = tk.Button(FNewDrink, text = "Make new Drink", command = showWindowNewDrink)
BNewDrink["font"] = "Arial 25 bold"
BNewDrink["height"] = 1
BNewDrink["width"] = 15

#p = sub.Popen(['hostname -I'], shell = True, stdout = sub.PIPE)
#ipAdress = p.communicate()
#ipAdress = str(ipAdress[0])
#ipAdress = ipAdress[2:-3]

#LipAdress = tk.Label(FNewDrink, text = "Um das Scoreboard auf dem Smartphone zu sehen, gebe in deinem Browser diese Adresse ein: "+ipAdress)
#LipAdress["font"] = "Arial 15"
#LipAdress["wraplength"] = 300

FNewDrink.pack(side = tk.LEFT)
BNewDrink.grid(row = 0, column = 0, padx = 10)
#LipAdress.grid(row = 2, column = 0)

#with open ('/home/pi/Desktop/score.csv', 'r') as file:
with open ('C:/Users/max-g/Desktop/score.csv', 'r') as file:
    csvreader = csv.reader(file, delimiter=";")
    ctr = 0
    for row in csvreader:   
        Player.append(row[0])
        Weight.append(float(row[1]))
        Gender.append(float(row[2]))
        LastDrink.append(datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S.%f'))
        nrDrinks.append(int(row[4]))
        promille.append(float(row[5]))
    ClearPrintScoreBoard()
    
def reducePromille():
    print("Promille Check")
    if len(promille) > 0:
        for i in range(len(promille)):
            difference = datetime.now() - LastDrink[i]
            difference = difference.total_seconds() / 60
            if difference > 1:
                if promille[i] - 0.025 > 0:
                    print("Prommille Abgezogen")
                    LastDrink[i] = datetime.now()
                    promille[i] = round(promille[i] - 0.025, 3)
                    ClearPrintScoreBoard()
                
                else:
                    promille[i] = 0

    sleep(5)
    reducePromille()

promille_thread = threading.Thread(target=reducePromille)
promille_thread.start()

root.mainloop()