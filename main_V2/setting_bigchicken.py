"""
Set all actions, goals and current world states here!!
this .py file is the only place you will need to change
=======================================================
"""
# ( ( x, y ), 1 for cup still there 0 for cup gone,  2  for green 3 for red, type : private 0 or public 1 )
cup_state = [ { 'location' : ( 510, 450 ), 'state' : 1, 'color' : 2, 'type' : 0 } , { 'location' : ( 1200, 300 ), 'state' : 1, 'color' : 2, 'type' : 0 },
                { 'location' : ( 400, 300 ), 'state' : 1, 'color' : 3, 'type' : 0 }, { 'location' : ( 1080, 450 ), 'state' : 1, 'color' : 3, 'type' : 0 } ,
                { 'location' : ( 1650, 1665 ), 'state' : 1, 'color' : 2, 'type' : 0 }, { 'location' : ( 1955, 1995 ), 'state' : 1, 'color' : 2, 'type' : 0 },
                { 'location' : ( 1955, 1605 ), 'state' : 1, 'color' : 3, 'type' : 0 }, { 'location' : ( 1650, 1935 ), 'state' : 1, 'color' : 3, 'type' : 0 },
                { 'location' : ( 100, 670 ), 'state' : 1, 'color' : 2, 'type' : 1 }, { 'location' : ( 800, 1100 ), 'state' : 1, 'color' : 2, 'type' : 1 },
                { 'location' : ( 1200, 1730 ), 'state' : 1, 'color' : 2, 'type' : 1 } , { 'location' : ( 400, 2050 ), 'state' : 1, 'color' : 2, 'type' : 1 },
                { 'location' : ( 400, 950 ), 'state' : 1, 'color' : 3, 'type' : 1 }, { 'location' : ( 1200, 1270 ), 'state' : 1, 'color' : 3, 'type' : 1 },
                { 'location' : ( 800, 1900 ), 'state' : 1, 'color' : 3, 'type' : 1 }, { 'location' : ( 100, 2330 ), 'state' : 1, 'color' : 3, 'type' : 1 } ]  

class Mission_precondition:
    def __init__(self, name, location, NS, reef_p, reef_l, reef_r, windsock, flag, lhouse, time, reward, effect):
        self.name = name
        self.location = location
        self.NS = NS
        self.reef_p = reef_p
        self.reef_l = reef_l
        self.reef_r = reef_r
        self.windsock = windsock
        self.flag = flag
        self.lhouse = lhouse
        self.time = time
        self.reward = reward
        self.cost = 0
        self.check = 0
        self.cup = None
        self.effect = effect
    def myfunc(self, name):
        print("mission " + name, self.NS, self.windsock, self.flag, self.lhouse, self.time)

class current_state:
    def __init__(self, name, location, NS, reef_p, reef_l, reef_r, windsock, flag, lhouse, time):
        self.name = name
        self.location = location 
        self.NS = NS
        self.reef_p = reef_p
        self.reef_l = reef_l
        self.reef_r = reef_r
        self.windsock = windsock
        self.flag = flag
        self.lhouse = lhouse
        self.time = time
        self.placecup_reef = 0
        self.check = 0
        self.candidate = []
        self.achieved = []
        self.cup_order = []
        self.emergency = 0
    def myfunc(self, name):
        print(name, self.NS, self.windsock, self.flag, self.lhouse, self.time, self.candidate)

class robotsetting:
    def __init__(self, a, b):
        self.cupstorage = a
        self.freestorage = a
        self.reef = b
        # print("debug", self.cupstorage , self.freestorage)
    def cup(self, num):
        # print("debug", self.cupstorage , num)
        self.freestorage = self.freestorage - num
        # print("free storage = ", self.freestorage)
#setting of mission precondition 
#name, location, NS, reefp, reefr, reefl, windsock, flag, lhouse, time, reward, effect[reefp, reefr, reefl, windsock, flag, lhouse]
windsock = Mission_precondition( "windsock", ( 2000, 430 ), None, None, None, None, 0, None, None, 10, 80, [None, None, None, 1, None, None, None])
# windsock.myfunc("windsock")
lhouse = Mission_precondition( "lhouse", ( 0, 300 ), None, None, None, None, None, None, 0, 2, 50,[None, None, None, None, None, 1])
# lhouse.myfunc("lhouse")
getcup = Mission_precondition( "getcup", ( 0, 0 ), None, None, None, None, None, None, None, 5, 20,[None, None, None, None, None, None])
# getcup.myfunc("getcup")
#reef cup counts separately
reef_private = Mission_precondition( "reef_private", ( 1600, 0 ), None, None, 1, None, None, None, None, 9, 100,[0, None, None, None, None, None])
# reef_private.myfunc("reef_private")
reef_left = Mission_precondition( "reef_left", ( 0, 850 ), None, None, None, 1, None, None, None, 9, 200,[None, None, 0, None, None, None])
# reef_left.myfunc("reef_left")
reef_right = Mission_precondition( "reef_right", ( 0, 2150 ), None, None, None, 1, None, None, None, 9, 200,[None, 0, None, None, None, None])
# reef_right.myfunc("reef_right")
placecup_reef = Mission_precondition( "placecup_reef", ( 800, 200 ), None, None, None, None, None, None, None, 5, 10000,[None, None, None, None, None, None])
# placecup_reef.myfunc("placecup_reef")
placecupP = Mission_precondition( "placecupP", ( 515, 200 ), None, None, None, None, None, None, None, 5, 40,[None, None, None, None, None, None])
# placecupP.myfunc("placecupP")
placecupH = Mission_precondition( "placecupH", ( 1850, 1800 ), None, None, None, None, None, None, None, 5, 40,[None, None, None, None, None, None])
# placecupH.myfunc("placecupH")
#temporay set that it has to be done last
anchorN = Mission_precondition( "anchorN", (300, 200 ), None, None, None, None, None, None, None, 2, 10000,[None, None, None, None, None, None])
# anchorN.myfunc("anchorN")
anchorS = Mission_precondition( "anchorS", ( 1300, 200 ), None, None, None, None, None, None, None, 2, 10000,[None, None, None, None, None, None])
# anchorS.myfunc("anchorS")
flag = Mission_precondition( "flag", None, None, None, None, 1, 1, 0, 1, 0, 20000,[None, None, None, 1, None, 1])
# flag.myfunc("flag") 

#setting of current state
#name, location, NS, reef_p, reef_l, reef_r, windsock, flag, lhouse, time):
cur = current_state( "cur", ( 800, 200, 0 ), 0, 1, 1, 1, 0, 0, 0, 0)
cur.myfunc("current") 

#setting of robot1 cup capacity and if can pick cup from reef
current_cup = 0
robot1 = robotsetting(12, 0)
# robot1 = robotsetting(5, 1)
robot1.cup(current_cup)

