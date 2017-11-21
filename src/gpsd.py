import socket
import time
import json
from threading import Thread

def checksum_NMEA (stringa_input):
    # Calcolo del checksum in formato NMEA - attenzione, per semplicità le eccezioni non sono gestite
    payload_start = stringa_input.find('$') + 1  # trova il primo carattere dopo $
    payload_end   = stringa_input.find('*')      # trova il carattere *
    payload = stringa_input [ payload_start : payload_end ]   # dati di cui fare XOR
    ck = 0
    for ch in payload:      # ciclo di calcolo del checksum
        ck = ck ^ ord(ch)   # XOR
    str_ck = '%02X' % ck    # trasforma il valore calcolato in una stringa di 2 caratteri
    return(str_ck)

class GPSD:
    def __init__ (self):
        self.currentPacket = None
        self.lat = None
        self.lon = None
        self.speed = None
        self.hdg = None
        self.conf = 'nmea'

    def updatePosition (self, lat, lon, speed, hdg):
        self.lat = lat
        self.lon = lon
        self.speed = speed * 0.5144
        self.speedkn = speed
        self.hdg = hdg

    def prepareJSONData (self):
        if not self.lat or not self.lon:
            return None

        return {
            "device": "sailaway",
            "class": "TPV",
            "lat": self.lat,
            "lon": self.lon,
            #"alt": 0,
            "track": self.hdg,
            "speed": self.speed, #meter per second
            "mode": 2,
            #"time":"2010-04-30T11:48:20.10Z",
            "ept":0.005,
            "epx":15.319,
            "epy":17.054,
            "epv":124.484,
            "climb":-0.085,
            "eps":34.11
        }

    def prepareNMEAData (self):
        if not self.lat or not self.lon:
            return []

        hdt = "$GPHDT," + str (self.hdg) + ",T*"
        hdt += checksum_NMEA (hdt)

        gll = "$GPGLL,"

        gll += str (int (abs (self.lat))) + "." + str (int (abs ((self.lat - int (self.lat)) * 60))) + ","
        if self.lat > 0:
            gll += 'N,'
        else:
            gll += 'S,'

        gll += str (int (abs (self.lon))) + "." + str (int (abs ((self.lon - int (self.lon)) * 60))) + ","
        if self.lon > 0:
            gll += 'E*'
        else:
            gll += 'W*'
        gll += checksum_NMEA (gll)
            
        return [
            bytes (hdt + '\n', 'ascii'),
            bytes (gll + '\n', "ascii")
        ]

    def serveClient (self, api, boatid, client):
        i = 0
		
        time.sleep (1)
        client.send (bytes (json.dumps ({"class":"VERSION","release":"3.17","rev":"3.17","proto_major":3,"proto_minor":12}) + '\n', 'ascii'))
        conf = client.recv (1024)
        self.conf = 'nmea'

        # TODO check if it wants json or nmea 

        time.sleep (1)
        client.send (bytes (json.dumps ({"class":"DEVICES","devices":[{"class":"DEVICE","path":"sailaway", "activated":1269959537.20,"native":0,"bps":4800,"parity":"N", "stopbits":1,"cycle":1.00}]}) + '\n', 'ascii'))
        client.send (bytes (json.dumps ({"class":"WATCH","enable":True,"json":True,"nmea":True,"raw":0,"scaled":False,"timing":False,"split24":False,"pps":False}) + '\n', 'ascii'))
        

        while True:
            if self.conf == 'nmea':
                for p in self.prepareNMEAData ():
                    client.send (p)
            elif self.conf == 'json':
                pack = self.prepareJSONData ()
                if pack:
                    client.send (bytes (json.dumps (self.currentPacket) + '\n', 'ascii'))

            time.sleep (1)            

            if i % 5 == 0:
                print ('Updating positon')
                bi = api.getBoatInfo (boatid)
                self.updatePosition (float (bi ['ubtlat']), float (bi['ubtlon']), float (bi['ubtspeedoverground']), float (bi['ubtheading']))
                
            i += 1
            
        
    def serve (self, api, boatid, port):
        self.socket = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind (("127.0.0.1", port))
        self.socket.listen (5)

        #pt = Thread (target=self.poolPosition, args=(api, boatid,))
        #pt.run()

        print ('Serving GPSD at port')
        while True:
            (client, address) = self.socket.accept ()
            print ('New connection')
            ct = Thread (target=self.serveClient, args=(api, boatid, client,))
            ct.run()
