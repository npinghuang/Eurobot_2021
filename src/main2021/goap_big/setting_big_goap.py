"""
Set all actions, goals and current world states here!!
this .py file is the only place you will need to change
=======================================================
"""
#!/usr/bin/env python
#coding=utf-8
import math

velocity = 500
angular_velocity = 200
margin = 30 #safety distance between other robot
# from srv import *
# name, location, NS, reef_p, reef_l, reef_r, windsock, flag, lhouse, time, emergency, e1_location, e2_location, friend_pos

class current_state:
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
		self.mission = None
		self.previous_mission = None


    def myfunc(self, name):
        print(name, self.NS, self.windsock, self.flag, self.lhouse, self.time, self.candidate)
cur = current_state( "cur", ( None, None, None ), None, None, None,  None, None, None, None, None, None, None, None, None)
cur.candidate = []

class robotsetting:
    def __init__(self, a, b):
		self.cupstorage = a #max cup storage
		self.freestorage = a #current free cup storage
		self.reef = b
		self.claw = [ 0, 0, 0, 0] # 0 for red~ 1 for green 2for green  ~ 3 for red
		self.suction = [ 0, 0, 0, 0, 0, 0, 0, 0  ] # 0 ~ 3 for red, 4 ~ 7 for green
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
        self.cup = []
        self.effect = effect
        self.little_mission_count = 0
        self.little_mission_pos = []
        self.little_mission_no = []
    def myfunc(self, name):
        print("mission " + name, self.NS, self.windsock, self.flag, self.lhouse, self.time)

#setting of mission precondition
def mission_precondition(req):
	#setting of robot1 cup capacity and if can pick cup from reef
	# current_cup = 0
	robot1 = robotsetting(12, 0)
	# robot1.cup(current_cup)
	
	#robot1 geometric setting 
	a = 40.0
	b = 50.0
	c = 80.0
	d = 70.0
	theta_claw = ( math.pi ) / 6
	theta_suction = ( math.pi ) / 4
	#state : 0 for no cup, 1 for have cup, color : 2  for green 3 for red, 
	robot1.claw = [ {'no' : 0, 'name' : 'frontleft', 'location' : ( a, b, theta_claw), 'state' : 0, 'color' : 2}, {'no' : 1, 'name' : 'frontright', 'location' : ( a, -b, -theta_claw), 'state' : 0, 'color' : 3},
								{'no' : 2, 'name' : 'backleft', 'location' :  ( -a, b, ( math.pi - theta_claw)), 'state' : 0, 'color' : 3}, {'no' : 3, 'name' : 'backright', 'location' : ( -a, -b, ( math.pi + theta_claw)), 'state' : 0, 'color' : 2}]
	robot1.suction = [ {'no' : 0, 'name' : 'frontleftup', 'location' : ( c, d, theta_suction), 'state' : 0, 'color' : 2}, {'no' : 1, 'name' : 'frontleftdown', 'location' : ( c, d, theta_suction), 'state' : 0, 'color' : 2},
										{'no' : 2, 'name' : 'frontrightup', 'location' : ( c, -d, -theta_suction), 'state' : 0, 'color' : 3}, {'no' : 3, 'name' : 'frontrightdown', 'location' : ( c, -d, -theta_suction), 'state' : 0, 'color' : 3},
										{'no' : 4, 'name' : 'backleftup', 'location' :  ( -c, d,( math.pi - theta_suction)), 'state' : 0, 'color' : 3}, {'no' : 5, 'name' : 'backleftdown', 'location' : ( -c, d,( math.pi - theta_suction)), 'state' : 0, 'color' : 3},
										{'no' : 6, 'name' : 'backrightup', 'location' : ( -c, -d,( math.pi + theta_suction)), 'state' : 0, 'color' : 2}, {'no' : 7, 'name' : 'backrightdown ', 'location' : ( -c, -d,( math.pi + theta_suction)), 'state' : 0, 'color' : 2}]
	# update hand status and robot freestorage
	current_cup = 0
	for i in range (0, len(req.hand)):
		if req.hand[i] == 1:
			current_cup += 1
		if i < 4:
			robot1.claw[i]['state'] = req.hand[i]
		else:
			robot1.suction[i - 4]['state'] = req.hand[i]
	robot1.cup( current_cup )
	#setting of current state
	( x, y , theta ) = ( req.my_pos[0], req.my_pos[1], req.my_pos[2])
	e1 = (req.enemy1_pos[0], req.enemy1_pos[1])
	e2 = (req.enemy2_pos[0], req.enemy2_pos[1])
	# name, location, NS, reef_p, reef_l, reef_r, windsock, flag, lhouse, time, emergency, e1_location, e2_location, friend_pos
	# cur = current_state( "cur", ( x, y , theta ), req.ns, req.action_list[8], req.action_list[6], req.action_list[7], req.action_list[1], 
	# req.action_list[3], req.action_list[2], req.time, req.emergency, e1, e2, req.friend_pos)
	# cur.name = "cur"
	cur.location = [x, y , theta]
	cur.NS = req.ns
	cur.reef_p = req.action_list[8]
	cur.reef_l = req.action_list[6]
	cur.reef_r = req.action_list[7]
	cur.windsock = req.action_list[1]
	cur.flag = req.action_list[3]
	cur.lhouse = req.action_list[2]
	cur.time = req.time
	cur.emergency = req.emergency
	cur.enemy_1= e1
	cur.enemy_2 = e2
	cur.friend_pos = req.friend_pos
	# ( no, ( x, y ), 1 for cup still there 0 for cup gone,  2  for green 3 for red, type : private 0 or public 1 )
	cur.cup_state = [  { 'no' : 2, 'location' : [1200, 300, 0], 'state' : 1, 'color' : 2, 'type' : 0 , 'robot_pos' : []}, { 'no' : 4, 'location' : [ 1085, 445, 0 ], 'state' : 1, 'color' : 3, 'type' : 0 ,'robot_pos' : []},
			{ 'no' : 3, 'location' :[ 515, 445, 0], 'state' : 1, 'color' : 2, 'type' : 0 , 'robot_pos' : []} , { 'no' :1,'location' : [ 400, 300, 0 ], 'state' : 1, 'color' : 3, 'type' : 0 , 'robot_pos' : []},
			{ 'no' : 5, 'location' : [ 100, 670, 0 ], 'state' : 1, 'color' : 2, 'type' : 1 , 'robot_pos' : []}, { 'no' : 6, 'location' : [ 400, 956, 0 ], 'state' : 1, 'color' : 3, 'type' : 1,  'robot_pos' : []}, 
			{ 'no' : 9, 'location' : [ 800, 1100, 0 ], 'state' : 1, 'color' : 2, 'type' : 1 , 'robot_pos' : []},{ 'no' : 10, 'location' : [ 1200, 1270, 0 ], 'state' : 1, 'color' : 3, 'type' : 1 , 'robot_pos' : []},
			{ 'no' : 8, 'location' : [ 1655, 1065, 0 ], 'state' : 0, 'color' : 2, 'type' : 0 ,'robot_pos' : []}, { 'no' : 11, 'location' : [ 1655, 1335, 0 ], 'state' : 0, 'color' : 3, 'type' : 0 ,'robot_pos' : []},
			{ 'no' : 7, 'location' : [ 1955, 1005, 0 ], 'state' : 0, 'color' : 3, 'type' : 0 ,'robot_pos' : []}, { 'no' : 12, 'location' : [ 1955, 1395, 0 ], 'state' : 0, 'color' : 2, 'type' : 0 ,'robot_pos' : []},
			{ 'no' : 15, 'location' : [ 1200, 1730, 0 ], 'state' : 1, 'color' : 2, 'type' : 1 , 'robot_pos' : []}, { 'no' : 16, 'location' : [ 800, 1900, 0 ], 'state' : 1, 'color' : 3, 'type' : 1 ,'robot_pos' : []},
			{ 'no' : 19, 'location' : [ 400, 2044, 0 ], 'state' : 1, 'color' : 2, 'type' : 1 ,'robot_pos' : []},  { 'no' : 20, 'location' : [ 100, 2330, 0 ], 'state' : 1, 'color' : 3, 'type' : 1 ,'robot_pos' : []},
			{ 'no' : 14, 'location' : [ 1655, 1665, 0 ], 'state' : 0, 'color' : 2, 'type' : 0 ,'robot_pos' : []}, { 'no' : 17, 'location' : [ 1655, 1935, 0 ], 'state' : 0, 'color' : 3, 'type' : 0 ,'robot_pos' : []},
			{ 'no' : 13, 'location' : [ 1955, 1605, 0 ], 'state' : 0, 'color' : 3, 'type' : 0 ,'robot_pos' : []}, { 'no' : 18, 'location' : [ 1955, 1995, 0 ], 'state' : 0, 'color' : 2, 'type' : 0 ,'robot_pos' : []},
			{ 'no' : 24, 'location' : [ 1200, 2700, 0 ], 'state' : 1, 'color' : 2, 'type' : 0 ,'robot_pos' : []}, { 'no' : 22, 'location' : [ 1085, 2555, 0 ], 'state' : 1, 'color' : 3, 'type' : 0 ,'robot_pos' : []},
			{ 'no' : 21, 'location' : [ 515, 2555, 0 ], 'state' : 1, 'color' : 2, 'type' : 0 ,'robot_pos' : []} , { 'no' : 23,'location' : [ 400, 2700, 0 ], 'state' : 1, 'color' : 3, 'type' : 0 ,'robot_pos' : []},
			{ 'no' : 25, 'location' : [ 0, 0, 0 ], 'state' : 0, 'color' : 3, 'type' : 1 ,'robot_pos' : []}, { 'no' : 26, 'location' : [ 0, 0, 0 ], 'state' : 0, 'color' : 3, 'type' : 1 ,'robot_pos' : []},
			{ 'no' : 27, 'location' : [ 0, 0, 0 ], 'state' : 0, 'color' : 3, 'type' : 1 ,'robot_pos' : []}, { 'no' : 28, 'location' : [ 0, 0, 0 ], 'state' : 0, 'color' : 3, 'type' : 1 ,'robot_pos' : []},
			{ 'no' : 29, 'location' : [ 0, 0, 0 ], 'state' : 0, 'color' : 3, 'type' : 1 ,'robot_pos' : []}, { 'no' : 30, 'location' : [ 0, 0, 0 ], 'state' : 0, 'color' : 3, 'type' : 1 ,'robot_pos' : []},
			{ 'no' : 31, 'location' : [ 0, 0, 0 ], 'state' : 0, 'color' : 3, 'type' : 1 ,'robot_pos' : []}, { 'no' : 32, 'location' : [ 0, 0, 0 ], 'state' : 0, 'color' : 3, 'type' : 1 ,'robot_pos' : []}]
	if req.team == 0: 
	    #no, name, location, NS, reefp, reefr, reefl, windsock, flag, lhouse, time, reward, effect[reefp, reefr, reefl, windsock, flag, lhouse]
	    windsock = Mission_precondition( 1, "windsock", ( 2000, 430, 0), None, None, None, None, 0, None, None, 8, 80, [None, None, None, 1, None, None,])
	    lhouse = Mission_precondition( 2, "lhouse", ( 0, 300, 0 ), None, None, None, None, None, None, 0, 2, 50,[None, None, None, None, None, 1])
	    getcup = Mission_precondition( 12, "getcup", ( 0, 0, 0), None, None, None, None, None, None, None, 5, 20,[None, None, None, None, None, None])
		#special case for cup 12 34
	    getcup_12 = Mission_precondition( 13, "getcup_12", ( 1085, 400, 0), None, None, None, None, None, None, None, 5, 1300,[None, None, None, None, None, None])
	    getcup_34 = Mission_precondition( 14, "getcup_34", ( 500, 400, 0), None, None, None, None, None, None, None, 5, 1300,[None, None, None, None, None, None])
		#reef cup counts separately
	    reef_private = Mission_precondition( 8, "reef_private", ( 1600, 0, 0 ), None, None, 1, None, None, None, None, 9, 100,[0, None, None, None, None, None])
	    reef_left = Mission_precondition( 6, "reef_left", ( 0, 850, 0 ), None, None, None, 1, None, None, None, 9, 200,[None, None, 0, None, None, None])
	    reef_right = Mission_precondition(7, "reef_right", ( 0, 2150, 0 ), None, None, None, 1, None, None, None, 9, 200,[None, 0, None, None, None, None])
	    placecup_reef = Mission_precondition( 11, "placecup_reef", ( 800, 200, 0 ), None, None, None, None, None, None, None, 10, 10000,[None, None, None, None, None, None])
	    placecupP = Mission_precondition( 10, "placecupP", ( 515, 200, 0 ), None, None, None, None, None, None, None, 10, 40,[None, None, None, None, None, None])
	    placecupH = Mission_precondition( 9, "placecupH", ( 1900, 1800, 0 ), None, None, None, None, None, None, None, 10, 40,[None, None, None, None, None, None])
	    #temporay set that it has to be done last
	    anchorN = Mission_precondition( 4, "anchorN", (300, 200, 0 ), 0, None, None, None, None, None, None, 2, 10000,[None, None, None, None, None, None])
	    anchorS = Mission_precondition( 5, "anchorS", ( 1300, 200, 0 ), 1, None, None, None, None, None, None, 2, 10000,[None, None, None, None, None, None])
	    flag = Mission_precondition( 3, "flag", None, None, None, None, 1, 1, 0, 1, 0, 20000,[None, None, None, None, 1, None])
		# little mission blue
	    windsock.little_mission_count = 2
	    windsock.location = [1850, 200, math.pi/2]
	    windsock.little_mission_pos = [ [1850, 200, math.pi/2], [1850, 700, math.pi/2]]
	    windsock.little_mission_no = [ 1, 15]
	    lhouse.little_mission_count = 3
	    lhouse.location = [100, 275, math.pi ]
	    lhouse.little_mission_pos = [ [150, 275, math.pi ], [ 100, 275, math.pi], [150, 275, math.pi]]
	    lhouse.little_mission_no = [ 2, 16, 17]
	    placecupH.little_mission_count = 7
	    placecupH.little_mission_pos =[ [1900, 1800, 0],  [1870, 1800, 0],  [1650, 1800, 0],  [1900, 1800, math.pi],  [1800, 1800, math.pi], [1770, 1800, math.pi], [1650, 1800, math.pi]]
	    placecupH.little_mission_no = [ 9, 18, 19, 20, 21, 22, 23 ]

	elif req.team == 1: 
		#name, location, NS, reefp, reefr, reefl, windsock, flag, lhouse, time, reward, effect[reefp, reefr, reefl, windsock, flag, lhouse]
	    windsock = Mission_precondition( 1, "windsock", ( 2000, 2330, 0), None, None, None, None, 0, None, None, 8, 100, [None, None, None, 1, None, None])
	    lhouse = Mission_precondition( 2, "lhouse", ( 0, 2775, 0 ), None, None, None, None, None, None, 0, 2, 1000,[None, None, None, None, None, 1])
	    getcup = Mission_precondition( 12, "getcup", ( 0, 0, 0), None, None, None, None, None, None, None, 5, 20,[None, None, None, None, None, None])
	    #special case for cup 12 34
	    getcup_12 = Mission_precondition( 13, "getcup_12", ( 1085, 2600, 0), None, None, None, None, None, None, None, 10, 13000,[None, None, None, None, None, None])
	    getcup_34 = Mission_precondition( 14, "getcup_34", ( 500, 2600, 0), None, None, None, None, None, None, None, 10, 13000,[None, None, None, None, None, None])
		#reef cup counts separately
	    reef_private = Mission_precondition( 8, "reef_private", ( 1600, 3000, 0 ), None, None, 1, None, None, None, None, 9, 100,[0, None, None, None, None, None])
	    reef_left = Mission_precondition( 6, "reef_left", ( 0, 850, 0 ), None, None, None, 1, None, None, None, 9, 200,[None, None, 0, None, None, None])
	    reef_right = Mission_precondition(7, "reef_right", ( 0, 2150, 0 ), None, None, None, 1, None, None, None, 9, 200,[None, 0, None, None, None, None])
	    placecup_reef = Mission_precondition( 11, "placecup_reef", ( 800, 2775, 0 ), None, None, None, None, None, None, None, 10, 10000,[None, None, None, None, None, None])
	    placecupP = Mission_precondition( 10, "placecupP", ( 515, 2775, 0 ), None, None, None, None, None, None, None, 10, 40,[None, None, None, None, None, None])
	    placecupH = Mission_precondition( 9, "placecupH", ( 1850, 1200, 0 ), None, None, None, None, None, None, None, 10, 40,[None, None, None, None, None, None])
	    #temporay set that it has to be done last
	    anchorN = Mission_precondition( 4, "anchorN", (300, 2775, 0 ), 0, None, None, None, None, None, None, 2, 10000,[None, None, None, None, None, None])
	    anchorS = Mission_precondition( 5, "anchorS", ( 1300, 2775, 0 ), 1, None, None, None, None, None, None, 2, 10000,[None, None, None, None, None, None])
	    flag = Mission_precondition( 3, "flag", None, None, None, None, 1, 1, 0, 1, 0, 20000,[None, None, None,None, 1,  None])	

		# little mission yellow
	    windsock.little_mission_count = 2
	    windsock.location = [1850, 2800, math.pi/2]
	    windsock.little_mission_pos = [ [1850, 2800, math.pi/2], [1850, 2300, math.pi/2]]
	    windsock.little_mission_no = [ 1, 15]
	    lhouse.little_mission_count = 3
	    lhouse.location = [150, 2725, math.pi]
	    lhouse.little_mission_pos = [ [150, 2725, math.pi ], [ 100, 2725,math.pi], [150, 2725, math.pi ]]
	    lhouse.little_mission_no = [ 2, 16, 17]
	    placecupH.little_mission_count = 7
	    placecupH.little_mission_pos =[ [1900, 1200, 0],  [1870, 1200, 0],  [1650, 1200, 0],  [1900, 1200, math.pi],  [1800, 1200, math.pi], [1770, 1200, math.pi], [1650, 1200, math.pi]]
	    placecupH.little_mission_no = [ 9, 18, 19, 20, 21, 22, 23 ]
	 # change item in this array to set what action is to be considered in goap
	cur.leaf = [ windsock, lhouse, getcup, getcup_12, getcup_34, placecupH, anchorN, anchorS, flag]
	# cur.myfunc("current")
	#refresh cup state
	c = 0
	ccup = req.cup
	for i in range (len(cur.cup_state)):
		c = int(ccup) % 2
		if c == 0:
			cur.cup_state[i]['state'] = c
		# print("c", c, i, cup)
		ccup = int(ccup / 2)	
	return cur, robot1
	
def cup_location_transfrom(cup_state):
	#clean previous robot pos
	for cup in cup_state:
		del cup['robot_pos'][:]
	# set parameter here 
	r = 80 #expansion radius
	n = 8 # how many dot per each cup
	x = 0.0
	y = 0.0
	theta = 0.0
	border = 125 #margin from each border
	cup_margin = 200 #margin for not to hit other cup
	angle = math.pi / n 
	# obstacle at harbour
	bump_middle = [ 1700, 1490 ]
	bump_right_blue = [ 1850, 2090 ]
	bump_left_yellow = [ 1850, 955 ]
	for cup in cup_state:
		cup['robot_pos'] = []
		if cup['state'] == 1:
			for i in range ( int(-n / 2), int( n / 2 ) ):
				x = cup['location'][0] + ( r * math.sin( i * angle ))
				y = cup['location'][1] + ( r * math.cos( i * angle ))
				theta = i * angle
				case = 1
				
				if x > border and x < ( 2000 - border ) and y > border and y < ( 3000 - border ): #check if hit the wall or not
					if (cup['no'] <= 7 and cup['no'] >= 14) and (cup['no'] <= 17 and cup['no'] >= 18): #check if hit the wall at harbour 
						if (x > ( bump_middle[0] - 30 ) and x < ( 2000 )) or (y > ( bump_middle[1] - border ) and y < ( bump_middle[1] + border )): #left one
							case = 0
						#for blue
						if (x > ( bump_right_blue[0] - 30 ) and x < ( 2000 )) or (y > ( bump_right_blue[1] - border ) and y < ( bump_right_blue[1] + border )): #right one
							case = 0
						#for yellow
						if (x > ( bump_left_yellow[0] - 30 ) and x < ( 2000 )) or (y > ( bump_left_yellow[1] - border ) and y < ( bump_left_yellow[1] + border )): #right one
							case = 0
					#check if hit other cup or not
					tmp = 0
					
					while tmp != -1 and tmp < len(cup_state) and case == 1:
						if cup['no'] != cup_state[tmp]['no'] and cup_state[tmp]['state'] == 1: #not to examine the same cup
							d = distance( cup_state[tmp]['location'], [ x, y ] )
							if d < cup_margin:
								tmp = -1
							else:
								tmp += 1
						else:
							tmp += 1
					if tmp != -1 and case == 1:
						# print("cup pos no: ", cup['no'], x, y, theta)
						cup['robot_pos'].append( [x, y, theta] )
		# print("cup", cup['no'], len(cup['robot_pos']))

def distance(a, b):
	if a != None and b != None:
		d =int((abs( a[0] - b[0] )**2 + abs( a[1] - b[1])**2))**0.5
		return d
	else:
		return None
