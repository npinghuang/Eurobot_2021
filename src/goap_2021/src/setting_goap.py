"""
Set all actions, goals and current world states here!!
this .py file is the only place you will need to change
=======================================================
"""
#!/usr/bin/env python
#coding=utf-8

# from srv import *
class current_state:
<<<<<<< HEAD
    def __init__(self, name, location, NS, reef_p, reef_l, reef_r, windsock, flag, lhouse, time, emergency, e1_location, e2_location, friend_pos ):
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
		self.leaf = []
		self.mission_list = []
		self.cup_state = []
		self.achieved = []
		self.cup_order = []
		self.emergency = emergency
		self.enemy_1 = e1_location
		self.enemy_2 = e2_location
		self.friend_pos = friend_pos
=======
    def __init__(self, name, location, NS, reef_p, reef_l, reef_r, windsock, flag, lhouse, time, emergency, e1_location, e2_location):
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
		self.leaf = []
        self.mission_list = []
		self.cup_state = []
        self.achieved = []
        self.cup_order = []
        self.emergency = emergency
        self.enemy_1 = e1_location
        self.enemy_2 = e2_location
>>>>>>> 9c6e1c731b2f77c52d988a4b79fa69f73164b842
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

class Mission_precondition:
    def __init__(self, no, name, location, NS, reef_p, reef_l, reef_r, windsock, flag, lhouse, time, reward, effect):
        self.no = no
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

#setting of mission precondition
def mission_precondition(req):
	#setting of robot1 cup capacity and if can pick cup from reef
	current_cup = 0
	robot1 = robotsetting(12, 0)
	robot1.cup(current_cup)
	#setting of current state
	( x, y , theta ) = ( req.my_pos[0], req.my_pos[1], req.my_pos[2])
	e1 = (req.enemy_pos[0], req.enemy_pos[1])
	e2 = (req.enemy_pos[2], req.enemy_pos[3])
<<<<<<< HEAD
	# name, location, NS, reef_p, reef_l, reef_r, windsock, flag, lhouse, time, emergency, e1_location, e2_location, friend_pos
	cur = current_state( "cur", ( x, y , theta ), req.ns, req.action_list[8], req.action_list[6], req.action_list[7], req.action_list[1], req.action_list[3], req.action_list[2], req.time, req.emergency, e1, e2, req.friend_pos)
=======
	#name, location, NS, reef_p, reef_l, reef_r, windsock, flag, lhouse, time, e1_location, e2_location
	cur = current_state( "cur", ( x, y , theta ), req.ns, req.action_list[8], req.action_list[6], req.action_list[7], req.action_list[1], req.action_list[3], req.action_list[2], req.time, req.emergency, e1, e2)
>>>>>>> 9c6e1c731b2f77c52d988a4b79fa69f73164b842
	if req.team == 0: 
	    # blue : ( no, ( x, y ), 1 for cup still there 0 for cup gone,  2  for green 3 for red, type : private 0 or public 1 )
	    cur.cup_state = [  { 'no' : 1, 'location' : ( 1200, 300, 0 ), 'state' : 1, 'color' : 2, 'type' : 0 }, { 'no' : 2, 'location' : ( 1085, 445, 0 ), 'state' : 1, 'color' : 3, 'type' : 0 },
			{ 'no' : 3, 'location' : ( 515, 445, 0 ), 'state' : 1, 'color' : 2, 'type' : 0 } , { 'no' : 4,'location' : ( 400, 300, 0 ), 'state' : 1, 'color' : 3, 'type' : 0 },
			{ 'no' : 5, 'location' : ( 100, 670, 0 ), 'state' : 1, 'color' : 2, 'type' : 1 }, { 'no' : 6, 'location' : ( 400, 956, 0 ), 'state' : 1, 'color' : 3, 'type' : 1 }, 
			{ 'no' : 7, 'location' : ( 800, 1100, 0 ), 'state' : 1, 'color' : 2, 'type' : 1 }, { 'no' : 8, 'location' : ( 1200, 1270, 0 ), 'state' : 1, 'color' : 3, 'type' : 1 },
			{ 'no' : 9, 'location' : ( 1200, 1730, 0 ), 'state' : 1, 'color' : 2, 'type' : 1 }, { 'no' : 10, 'location' : ( 800, 1900, 0 ), 'state' : 1, 'color' : 3, 'type' : 1 },
			{ 'no' : 11, 'location' : ( 400, 2044, 0 ), 'state' : 1, 'color' : 2, 'type' : 1 },  { 'no' : 12, 'location' : ( 100, 2330, 0 ), 'state' : 1, 'color' : 3, 'type' : 1 },
			{ 'no' : 13, 'location' : ( 1655, 1665, 0 ), 'state' : 1, 'color' : 2, 'type' : 0 }, { 'no' : 14, 'location' : ( 1655, 1935, 0 ), 'state' : 1, 'color' : 3, 'type' : 0 },
			{ 'no' : 15, 'location' : ( 1955, 1605, 0 ), 'state' : 1, 'color' : 3, 'type' : 0 }, { 'no' : 16, 'location' : ( 1955, 1995, 0 ), 'state' : 1, 'color' : 2, 'type' : 0 },
			{ 'no' : 17, 'location' : ( 0, 0, 0 ), 'state' : 0, 'color' : 3, 'type' : 1 }, { 'no' : 18, 'location' : ( 0, 0, 0 ), 'state' : 0, 'color' : 3, 'type' : 1 },
			{ 'no' : 19, 'location' : ( 0, 0, 0 ), 'state' : 0, 'color' : 3, 'type' : 1 }, { 'no' : 20, 'location' : ( 0, 0, 0 ), 'state' : 0, 'color' : 3, 'type' : 1 },
			{ 'no' : 21, 'location' : ( 0, 0, 0 ), 'state' : 0, 'color' : 3, 'type' : 1 }, { 'no' : 22, 'location' : ( 0, 0, 0 ), 'state' : 0, 'color' : 3, 'type' : 1 },
			{ 'no' : 23, 'location' : ( 0, 0, 0 ), 'state' : 0, 'color' : 3, 'type' : 1 }, { 'no' : 24, 'location' : ( 0, 0, 0 ), 'state' : 0, 'color' : 3, 'type' : 1 }]

<<<<<<< HEAD
	    #no, name, location, NS, reefp, reefr, reefl, windsock, flag, lhouse, time, reward, effect[reefp, reefr, reefl, windsock, flag, lhouse]
	    windsock = Mission_precondition( 1, "windsock", ( 2000, 430, 0), None, None, None, None, 0, None, None, 2, 80, [None, None, None, 1, None, None,])
	    # windsock.myfunc("windsock")
=======
	    #name, location, NS, reefp, reefr, reefl, windsock, flag, lhouse, time, reward, effect[reefp, reefr, reefl, windsock, flag, lhouse]
	    windsock = Mission_precondition( 1, "windsock", ( 2000, 430, 0), None, None, None, None, 0, None, None, 2, 80, [None, None, None, 1, None, None, None])
>>>>>>> 9c6e1c731b2f77c52d988a4b79fa69f73164b842
	    lhouse = Mission_precondition( 2, "lhouse", ( 0, 300, 0 ), None, None, None, None, None, None, 0, 2, 50,[None, None, None, None, None, 1])
	    getcup = Mission_precondition( 12, "getcup", ( 0, 0, 0), None, None, None, None, None, None, None, 2, 20,[None, None, None, None, None, None])
	    #reef cup counts separately
	    reef_private = Mission_precondition( 8, "reef_private", ( 1600, 0, 0 ), None, None, 1, None, None, None, None, 9, 100,[0, None, None, None, None, None])
	    reef_left = Mission_precondition( 6, "reef_left", ( 0, 850, 0 ), None, None, None, 1, None, None, None, 9, 200,[None, None, 0, None, None, None])
	    reef_right = Mission_precondition(7, "reef_right", ( 0, 2150, 0 ), None, None, None, 1, None, None, None, 9, 200,[None, 0, None, None, None, None])
	    placecup_reef = Mission_precondition( 11, "placecup_reef", ( 800, 200, 0 ), None, None, None, None, None, None, None, 5, 10000,[None, None, None, None, None, None])
	    placecupP = Mission_precondition( 10, "placecupP", ( 515, 200, 0 ), None, None, None, None, None, None, None, 5, 40,[None, None, None, None, None, None])
	    placecupH = Mission_precondition( 9, "placecupH", ( 1850, 1800, 0 ), None, None, None, None, None, None, None, 5, 40,[None, None, None, None, None, None])
	    #temporay set that it has to be done last
	    anchorN = Mission_precondition( 4, "anchorN", (300, 200, 0 ), 0, None, None, None, None, None, None, 2, 10000,[None, None, None, None, None, None])
	    anchorS = Mission_precondition( 5, "anchorS", ( 1300, 200, 0 ), 1, None, None, None, None, None, None, 2, 10000,[None, None, None, None, None, None])
<<<<<<< HEAD
	    # anchorS.myfunc("anchorS")
	    flag = Mission_precondition( 3, "flag", None, None, None, None, 1, 1, 0, 1, 0, 20000,[None, None, None, None, 1, None])
	    # flag.myfunc("flag")  


=======
	    flag = Mission_precondition( 3, "flag", None, None, None, None, 1, 1, 0, 1, 0, 20000,[None, None, None, 1, None, 1])

>>>>>>> 9c6e1c731b2f77c52d988a4b79fa69f73164b842
	elif req.team == 1: 
		# yellow : ( no, ( x, y ), 1 for cup still there 0 for cup gone,  2  for green 3 for red, type : private 0 or public 1 )
	    cur.cup_state = [  { 'no' : 1, 'location' : ( 1200, 2700, 0 ), 'state' : 1, 'color' : 2, 'type' : 0 }, { 'no' : 2, 'location' : ( 1085, 2555, 0 ), 'state' : 1, 'color' : 3, 'type' : 0 },
			{ 'no' : 3, 'location' : ( 515, 2555, 0 ), 'state' : 1, 'color' : 2, 'type' : 0 } , { 'no' : 4,'location' : ( 400, 2700, 0 ), 'state' : 1, 'color' : 3, 'type' : 0 },
			{ 'no' : 5, 'location' : ( 100, 670, 0 ), 'state' : 1, 'color' : 2, 'type' : 1 }, { 'no' : 6, 'location' : ( 400, 956, 0 ), 'state' : 1, 'color' : 3, 'type' : 1 }, 
			{ 'no' : 7, 'location' : ( 800, 1100, 0 ), 'state' : 1, 'color' : 2, 'type' : 1 }, { 'no' : 8, 'location' : ( 1200, 1270, 0 ), 'state' : 1, 'color' : 3, 'type' : 1 },
			{ 'no' : 9, 'location' : ( 1200, 1730, 0 ), 'state' : 1, 'color' : 2, 'type' : 1 }, { 'no' : 10, 'location' : ( 800, 1900, 0 ), 'state' : 1, 'color' : 3, 'type' : 1 },
			{ 'no' : 11, 'location' : ( 400, 2044, 0 ), 'state' : 1, 'color' : 2, 'type' : 1 },  { 'no' : 12, 'location' : ( 100, 2330, 0 ), 'state' : 1, 'color' : 3, 'type' : 1 },
			{ 'no' : 13, 'location' : ( 1655, 1065, 0 ), 'state' : 1, 'color' : 2, 'type' : 0 }, { 'no' : 14, 'location' : ( 1655, 1335, 0 ), 'state' : 1, 'color' : 3, 'type' : 0 },
			{ 'no' : 15, 'location' : ( 1955, 1005, 0 ), 'state' : 1, 'color' : 3, 'type' : 0 }, { 'no' : 16, 'location' : ( 1955, 1395, 0 ), 'state' : 1, 'color' : 2, 'type' : 0 },
			{ 'no' : 17, 'location' : ( 0, 0, 0 ), 'state' : 0, 'color' : 3, 'type' : 1 }, { 'no' : 18, 'location' : ( 0, 0, 0 ), 'state' : 0, 'color' : 3, 'type' : 1 },
			{ 'no' : 19, 'location' : ( 0, 0, 0 ), 'state' : 0, 'color' : 3, 'type' : 1 }, { 'no' : 20, 'location' : ( 0, 0, 0 ), 'state' : 0, 'color' : 3, 'type' : 1 },
			{ 'no' : 21, 'location' : ( 0, 0, 0 ), 'state' : 0, 'color' : 3, 'type' : 1 }, { 'no' : 22, 'location' : ( 0, 0, 0 ), 'state' : 0, 'color' : 3, 'type' : 1 },
			{ 'no' : 23, 'location' : ( 0, 0, 0 ), 'state' : 0, 'color' : 3, 'type' : 1 }, { 'no' : 24, 'location' : ( 0, 0, 0 ), 'state' : 0, 'color' : 3, 'type' : 1 }]
		
<<<<<<< HEAD
	    #name, location, NS, reefp, reefr, reefl, windsock, flag, lhouse, time, reward, effect[reefp, reefr, reefl, windsock, flag, lhouse]
	    windsock = Mission_precondition( 1, "windsock", ( 2000, 2330, 0), None, None, None, None, 0, None, None, 2, 80, [None, None, None, 1, None, None])
=======
		#name, location, NS, reefp, reefr, reefl, windsock, flag, lhouse, time, reward, effect[reefp, reefr, reefl, windsock, flag, lhouse]
	    windsock = Mission_precondition( 1, "windsock", ( 2000, 2330, 0), None, None, None, None, 0, None, None, 2, 80, [None, None, None, 1, None, None, None])
>>>>>>> 9c6e1c731b2f77c52d988a4b79fa69f73164b842
	    lhouse = Mission_precondition( 2, "lhouse", ( 0, 2775, 0 ), None, None, None, None, None, None, 0, 2, 50,[None, None, None, None, None, 1])
	    getcup = Mission_precondition( 12, "getcup", ( 0, 0, 0), None, None, None, None, None, None, None, 2, 20,[None, None, None, None, None, None])
	    #reef cup counts separately
	    reef_private = Mission_precondition( 8, "reef_private", ( 1600, 3000, 0 ), None, None, 1, None, None, None, None, 9, 100,[0, None, None, None, None, None])
	    reef_left = Mission_precondition( 6, "reef_left", ( 0, 850, 0 ), None, None, None, 1, None, None, None, 9, 200,[None, None, 0, None, None, None])
	    reef_right = Mission_precondition(7, "reef_right", ( 0, 2150, 0 ), None, None, None, 1, None, None, None, 9, 200,[None, 0, None, None, None, None])
	    placecup_reef = Mission_precondition( 11, "placecup_reef", ( 800, 2775, 0 ), None, None, None, None, None, None, None, 5, 10000,[None, None, None, None, None, None])
	    placecupP = Mission_precondition( 10, "placecupP", ( 515, 2775, 0 ), None, None, None, None, None, None, None, 5, 40,[None, None, None, None, None, None])
	    placecupH = Mission_precondition( 9, "placecupH", ( 1850, 1200, 0 ), None, None, None, None, None, None, None, 5, 40,[None, None, None, None, None, None])
	    #temporay set that it has to be done last
	    anchorN = Mission_precondition( 4, "anchorN", (300, 2775, 0 ), 0, None, None, None, None, None, None, 2, 10000,[None, None, None, None, None, None])
	    anchorS = Mission_precondition( 5, "anchorS", ( 1300, 2775, 0 ), 1, None, None, None, None, None, None, 2, 10000,[None, None, None, None, None, None])
<<<<<<< HEAD
	    flag = Mission_precondition( 3, "flag", None, None, None, None, 1, 1, 0, 1, 0, 20000,[None, None, None,None, 1,  None])	
=======
	    flag = Mission_precondition( 3, "flag", None, None, None, None, 1, 1, 0, 1, 0, 20000,[None, None, None, 1, None, 1])
>>>>>>> 9c6e1c731b2f77c52d988a4b79fa69f73164b842
	cur.leaf = [windsock, lhouse, getcup, reef_private, reef_right, reef_left, placecup_reef, placecupP, placecupH, anchorN, anchorS, flag]
	#cur.myfunc("current")
	#print("emergency", cur.emergency) 

	#refresh cup state
<<<<<<< HEAD
	c = 0
	ccup = req.cup
	for i in range (len(cur.cup_state)):
		c = int(ccup) % 2
		cur.cup_state[i]['state'] = c
		# print("c", c, i, cup)
		ccup = int(ccup / 2)	
=======
	# tmp = 0
	# for c in req.cup:
	#     cur.cup_state[tmp]['state'] = c
	#     tmp += 1
	c = 0
	for i in range (len(cur.cup_state)):
		c = int(req.cup) % 2
		cur.cup_state[i]['state'] = c
		# print("c", c, i, cup)
		cup = int(cup / 2)		
>>>>>>> 9c6e1c731b2f77c52d988a4b79fa69f73164b842
	return cur, robot1
	
