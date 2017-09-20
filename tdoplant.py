#!/usr/bin/env python

from shutil import copyfile
from datetime import datetime
from numpy import genfromtxt
from matplotlib.dates import DateFormatter
import subprocess
import re
import numpy as np
import matplotlib
import matplotlib.dates as mdates
import pandas as pd
import sys

print "De plant aan z'n wortels aan het sjorren..."
# ff lekker iets instellen
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ff lekker de probe uitlezen
miFloraResult = None
tries = 0
while miFloraResult is None:
    if tries > 10:
	sys.exit("10 pogingen verder, wie is hier nu de snackbar?")
    try:
	miFlora = subprocess.Popen('/home/pi/go/bin/miflora C4:7C:8D:63:64:E1 hci0', shell=True, stdout=subprocess.PIPE)
	result = miFlora.stdout.read()
	if "Error" not in result:
		miFloraResult = result
		print "miFlora uitgelezen"
	else:
		print "Fout bij uitlezen miFlora"
    except:
         pass
    tries = tries + 1

# ff lekker zoeken in het resultaat
miTemp = float(re.search(r"Temperature:(\d*[.\d]*)", miFloraResult).group(1))
miMoist = int(re.search(r"Moisture:(\d*)", miFloraResult).group(1))
miConductivity = int(re.search(r"Conductivity:(\d*)", miFloraResult).group(1))
miLight = int(re.search(r"Light:(\d*)", miFloraResult).group(1))
miBattery = int(re.search(r"Battery:(\d*)", miFloraResult).group(1))

# ff lekker bepalen welke afbeeldingen we moeten gebruiken
if miTemp < 18:
       	temp = 'temp1.jpg'
elif miTemp <= 25:
       	temp = 'temp2.jpg'
elif miTemp > 25:
       	temp = 'temp3.jpg'

if miMoist < 20:
       	moist = 'moist1.jpg'
elif miMoist <= 60:
       	moist = 'moist2.jpg'
elif miMoist > 60:
       	moist = 'moist3.jpg'

if miConductivity < 300:
	condu = 'condu1.jpg'
elif miConductivity <= 1200:
        condu = 'condu2.jpg'
elif miConductivity > 1200:
        condu = 'condu3.jpg'

if miLight < 25:
        licht = 'licht1.jpg'
elif miLight <= 500:
        licht = 'licht2.jpg'
elif miLight > 500:
        licht = 'licht3.jpg'

# ff lekker de waarden backkuppen in een tekstbestand
dt = datetime.now().strftime('%Y-%m-%d %H:%M')

text_file = open("vocht.txt", "a")
text_file.write (dt +","+ str(miMoist) + "\n")
text_file.close()

text_file = open("voeding.txt", "a")
text_file.write (dt +","+ str(miConductivity) + "\n")
text_file.close()

text_file = open("temp.txt", "a")
text_file.write (dt +","+ str(miTemp) + "\n")
text_file.close()

text_file = open("licht.txt", "a")
text_file.write (dt +","+ str(miLight) + "\n")
text_file.close()

# ff lekker wat database onderhoud plegen
maxLines = 1000

with open('voeding.txt', 'r') as fcount:
        removeLines = sum(1 for line in fcount) - maxLines
if removeLines > 0:
        data="".join(open("voeding.txt").readlines()[removeLines:])
        open("voeding.txt","wb").write(data)

with open('licht.txt', 'r') as fcount:
        removeLines = sum(1 for line in fcount) - maxLines
if removeLines > 0:
        data="".join(open("licht.txt").readlines()[removeLines:])
        open("licht.txt","wb").write(data)

with open('temp.txt', 'r') as fcount:
        removeLines = sum(1 for line in fcount) - maxLines
if removeLines > 0:
        data="".join(open("temp.txt").readlines()[removeLines:])
        open("temp.txt","wb").write(data)

with open('vocht.txt', 'r') as fcount:
        removeLines = sum(1 for line in fcount) - maxLines
if removeLines > 0:
        data="".join(open("vocht.txt").readlines()[removeLines:])
        open("vocht.txt","wb").write(data)

# ff lekker wat grafiekjes plotten
	# licht
headers = ['Date','Lux']
df = pd.read_csv('licht.txt',names=headers)
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d %H:%M:%S.%f')
df['Date'] = df['Date'].map(lambda x: datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S'))
x = df['Date']
y = df['Lux']
plt.ylabel('Lux')
plt.plot(x,y)
formatter = DateFormatter('%d-%m %H:%M')
plt.gcf().axes[0].xaxis.set_major_formatter(formatter)
plt.title('Lichtsterkte')
plt.gcf().autofmt_xdate()
plt.savefig("/var/www/html/admin/plant/plotlicht.png")

        # temp
plt.clf()
headers = ['Date','Temp']
df = pd.read_csv('temp.txt',names=headers)
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d %H:%M:%S.%f')
df['Date'] = df['Date'].map(lambda x: datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S'))
x = df['Date']
y = df['Temp']
plt.ylabel('Celcius')
plt.plot(x,y)
formatter = DateFormatter('%d-%m %H:%M')
plt.gcf().axes[0].xaxis.set_major_formatter(formatter)
plt.title('Temperatuur')
plt.gcf().autofmt_xdate()
plt.savefig("/var/www/html/admin/plant/plottemp.png")

        # voeding
plt.clf()
headers = ['Date','Conductivity']
df = pd.read_csv('voeding.txt',names=headers)
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d %H:%M:%S.%f')
df['Date'] = df['Date'].map(lambda x: datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S'))
x = df['Date']
y = df['Conductivity']
plt.ylabel('microSiemens/cm')
plt.plot(x,y)
formatter = DateFormatter('%d-%m %H:%M')
plt.gcf().axes[0].xaxis.set_major_formatter(formatter)
plt.title('Voeding')
plt.gcf().autofmt_xdate()
plt.savefig("/var/www/html/admin/plant/plotvoeding.png")

        # vocht
plt.clf()
headers = ['Date','Moist']
df = pd.read_csv('vocht.txt',names=headers)
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d %H:%M:%S.%f')
df['Date'] = df['Date'].map(lambda x: datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S'))
x = df['Date']
y = df['Moist']
plt.ylabel('Vocht percentage')
plt.plot(x,y)
formatter = DateFormatter('%d-%m %H:%M')
plt.gcf().axes[0].xaxis.set_major_formatter(formatter)
plt.title('Water')
plt.gcf().autofmt_xdate()
plt.savefig("/var/www/html/admin/plant/plotvocht.png")

# ff lekker een html'etje opbouwen van het resultaat
text_file = open("/var/www/html/admin/plant/plant.html", "w")
text_file.write("<html>")
text_file.write("<head>")
text_file.write("<title>Plant stats!!!11</title>")
text_file.write("<meta http-equiv=\"refresh\" content=\"10\">")
text_file.write("</head>")
text_file.write("<body>")
text_file.write("<basefont face='Verdana' size='2'")
text_file.write("<p><h1>plant stats!!!11</h1></p>")
text_file.write("<p><img src='images/"+ moist +"'>  <img src='images/"+ condu +"'> <img src='images/"+ temp +"'> <img src='images/"+ licht +"'></p>")
text_file.write("<p><h2>Ruwe data</font></h2></p>")
text_file.write("Temperatuur: " +  str(miTemp) + " graden")
text_file.write("</br>Vochtigheid: " + str(miMoist) + "%")
text_file.write("</br>Voeding: " +  str(miConductivity) + " uS/cm")
text_file.write("</br>Lichtsterkte: " +  str(miLight) + " lux")
text_file.write("</br>MiFlora batterij: " +  str(miBattery) + "%")
text_file.write("</br></br>laatste update: " + datetime.now().strftime('%d %B %H:%M:%S'))
text_file.write("<p><b><h2>Specs</h2></b></p>")
text_file.write("Chlorophytum comosum oftewel een graslelie. Water nodig indien onder de 20% vochtigheid.")
text_file.write("</br>Voedsel geven onder de 200 us/cm, maar niet meer dan 1200 us/cm.")
text_file.write("<p><b><h2>Historie</h2></b></p>")
text_file.write("</br><img src='plotvocht.png'>")
text_file.write("</br><img src='plotvoeding.png'>")
text_file.write("</br><img src='plottemp.png'>")
text_file.write("</br><img src='plotlicht.png'>")
text_file.write("</font></body>")
text_file.write("</html>")
text_file.close()
