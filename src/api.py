import time
import requests
import json

class Sailaway:
    def __init__ (self):
        self.headers = {}
    
        #try:
        if True:
            f = open ('login.auth', 'r')
            d = json.loads (f.read ())
            self.email = d['email']
            self.password = d['password']
        #except:
        #    print (e)
        #    self.email = None
        #    self.password = None

    def _saveLogin (self):
        f = open ('login.auth', 'w')
        f.write (json.dumps ({ 'email': self.email, 'password': self.password }))
        f.close ()

    def login (self, email = None, password = None):
        if email != None and password != None:
            self.email = email
            self.password = password

        data = { 'submitlogin': 'Login', 'email': email, 'pwd': password, 'page': 'http://sailaway.world/cgi-bin/sailaway/missions.pl' }
        r = requests.post ('https://sailaway.world/cgi-bin/sailaway/weblogin.pl', data=data)
        print (r.headers)
        session = r.headers['Set-Cookie'].split ('=')[1].split (';')[0]
        self.headers = { "Cookie": "CGISESSID=" + session }
        self._saveLogin ()
        time.sleep (1)

    def getMission (self, missionid):
        r = requests.get ('https://sailaway.world/cgi-bin/sailaway/GetMission.pl?misnr=' + str (missionid), headers=self.headers)
        return r.json ()

    def getLeaderBoard (self, missionid):
        r = requests.get ('https://sailaway.world/cgi-bin/sailaway/GetLeaderboard.pl?misnr=' + str (missionid), headers=self.headers)
        return r.json ()

    def getMissions (self, history = False, rtype = 0):
        if history:
            hist = 1
        else:
            hist = 0

        r = requests.get ('https://sailaway.world/cgi-bin/sailaway/GetMissions.pl?race=1&tutorial=0&hist=' + str (hist) + '&racetype=' + str (rtype), headers=self.headers)
        return r.json ()

    def getUserBoats (self):
        print (self.headers)
        r = requests.get ('https://sailaway.world/cgi-bin/sailaway/GetUserBoats.pl', headers=self.headers)
        return r.json ()

    def getBoatInfo (self):
        r = requests.get ('https://sailaway.world/cgi-bin/sailaway/BoatInfo.pl?ubtnr=' + str (boatid), headers=self.headers)
        return r.json ()

    def getTrips (self, boatid):
        r = requests.get ('https://sailaway.world/cgi-bin/sailaway/Trip.pl?action=list&ubtnr=' + str (boatid), headers=self.headers)
        return r.json ()

    def deleteTrip (self, boatid, tripid):
        r = requests.get ('https://sailaway.world/cgi-bin/sailaway/Trip.pl?action=del&trpnr=' + str (tripid) + '&ubtnr=' + str (boatid), headers=self.headers)
        return r.json ()

    def saveTrip (self, boatid, tripid, checkpoints=[]):
        pass