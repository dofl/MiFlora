import subprocess
import re
import paho.mqtt.client as mqtt
import time

def probeUitlezen(macAdd):

        miFloraResult = None
        tries = 0
        while miFloraResult is None:
                if tries > 10:
                        sys.exit("10 tries, stopping")

                try:
                        miFlora = subprocess.Popen('/home/pi/go/bin/miflora '+ macAdd +' hci0', shell=True, stdout=subprocess.PIPE)
                        result = miFlora.stdout.read()
                        print result
                        if "Error" not in result:
                                miFloraResult = result
                                print "miFlora uitgelezen"

                                miTemp = float(re.search(r"Temperature:(\d*[.\d]*)", miFloraResult).group(1))
                                miMoist = int(re.search(r"Moisture:(\d*)", miFloraResult).group(1))
                                miConductivity = int(re.search(r"Conductivity:(\d*)", miFloraResult).group(1))
                                miLight = int(re.search(r"Light:(\d*)", miFloraResult).group(1))
                                miBattery = int(re.search(r"Battery:(\d*)", miFloraResult).group(1))

                                client = mqtt.Client("test")
                                client.connect("192.168.1.3", 32768)
                                client.publish("miflower/"+ macAdd +"/temp",miTemp)
                                client.publish("miflower/"+ macAdd +"/moist",miMoist)
                                client.publish("miflower/"+ macAdd +"/conductivity",miConductivity)
                                client.publish("miflower/"+ macAdd +"/light",miLight)
                                client.publish("miflower/"+ macAdd +"/battery",miBattery)
                        else:
                                print "Fout bij uitlezen miFlora"
                except Exception as e:
                        print "Foutmelding bij uitlezen probe: " + str(e)
                        pass
                        tries = tries + 1

probeUitlezen("C4:7C:8D:65:C4:6F") # banaan
probeUitlezen("C4:7C:8D:63:64:E1") # groene plant
probeUitlezen("C4:7C:8D:65:CB:DE") # hangplant
probeUitlezen("C4:7C:8D:63:7E:38") # keuken
