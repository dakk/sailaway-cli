import requests

class Sailaway:
    def __init__ (self):
        self.cookies = dict(CGISESSID=SESSIONID)

    def login (self, username, password):
        self.username = username
        self.password = password
        self.cookies = dict(CGISESSID=SESSIONID)

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

