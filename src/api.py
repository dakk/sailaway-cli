import requests

class Sailaway:
    def __init__ (self):
        self.cookies = dict()
    
        try:
            f = open ('login.auth', 'r')
            d = json.load (f.read ())
            self.email = d['email']
            self.password = d['password']
        except:
            self.email = None
            self.password = None

    def _saveLogin (self):
        f = open ('login.auth', 'w')
        f.write (json.dumps ({ 'email': self.email, 'password': self.password }))
        f.close ()

    def login (self, email, password):
        self.email = email
        self.password = password
        data = { 'submitlogin': 'Login', 'email': email, 'pwd': password, 'page': 'http://sailaway.world/cgi-bin/sailaway/missions.pl' }
        r = requests.post ('https://sailaway.world/cgi-bin/sailaway/weblogin.pl?page=http://sailaway.world/cgi-bin/sailaway/missions.pl', data=data)
        session = r.headers['Set-Cookie'].split ('=')[1]
        self.cookies = dict(CGISESSID=session)
        self._saveLogin ()

    def getMission (self, missionid):
        r = requests.get ('https://sailaway.world/cgi-bin/sailaway/GetMission.pl?misnr=' + str (missionid), cookies=self.cookies)
        return r.json ()

    def getLeaderBoard (self, missionid):
        r = requests.get ('https://sailaway.world/cgi-bin/sailaway/GetLeaderboard.pl?misnr=' + str (missionid), cookies=self.cookies)
        return r.json ()

    def getMissions (self, history = False, rtype = 0):
        if history:
            hist = 1
        else:
            hist = 0

        r = requests.get ('https://sailaway.world/cgi-bin/sailaway/GetMissions.pl?race=1&tutorial=0&hist=' + str (hist) + '&racetype=' + str (rtype), cookies=self.cookies)
        return r.json ()

    def getUserBoats (self):
        r = requests.get ('https://sailaway.world/cgi-bin/sailaway/GetUserBoats.pl', cookies=self.cookies)
        return r.json ()

    def getBoatInfo (self):
        r = requests.get ('https://sailaway.world/cgi-bin/sailaway/BoatInfo.pl?ubtnr=' + str (boatid), cookies=self.cookies)
        return r.json ()

    def getTrips (self, boatid):
        r = requests.get ('https://sailaway.world/cgi-bin/sailaway/Trip.pl?action=list&ubtnr=' + str (boatid), cookies=self.cookies)
        return r.json ()

    def deleteTrip (self, boatid, tripid):
        r = requests.get ('https://sailaway.world/cgi-bin/sailaway/Trip.pl?action=del&trpnr=' + str (tripid) + '&ubtnr=' + str (boatid), cookies=self.cookies)
        return r.json ()

    def saveTrip (self, boatid, tripid, checkpoints=[]):
        pass