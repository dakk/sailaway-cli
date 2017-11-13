import socket
from threading import Thread

class GPSD:
    def __init__ (self):
        self.currentPacket = None

    def updatePosition (self, lat, lon, speed, hdg):
        self.currentPacket = {
            "class": "TPV",
            "lat": lat,
            "lon": lon,
            "track": hdg,
            "speed": speed, #meter per second
            "mode": 2
        }

    def serveClient (self, api, boatid, client):
        while True:
            bi = api.getBoatInfo (boatid)
            print (bi)
            #self.updatePosition ()


    def serve (self, api, boatid, port):
        self.socket = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind (("127.0.0.1", port))
        self.socket.listen (5)

        print ('Serving GPSD at port')
        while True:
            (client, address) = self.socket.accept ()
            print ('New connection')
            ct = Thread (target=self.serveClient, args=(api, boatid, client,))
            ct.run()