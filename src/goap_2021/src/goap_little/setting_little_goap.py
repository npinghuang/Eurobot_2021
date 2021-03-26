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
		self.depth_a = 5
		self.previous_mission = None

    def myfunc(self, name):
        print(name, self.NS, self.windsock, self.flag, self.lhouse, self.time, self.candidate)
# self, name, location, NS, reef_p, reef_l, reef_r, windsock, flag, lhouse, time, emergency, e1_location, e2_location, friend_pos 
cur = current_state( "cur", ( None, None, None ), None, 1, 1, 1, None, None, None, None, None, None, None, None)
cur.candidate = []

class robotsetting:
    def __init__(self, a, b):
		self.cupstorage = a #max cup storage
		self.freestorage = a #current free cup storage
		self.reef = b
		self.hand_little = 0
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
	robot1 = robotsetting(5,1)
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
	robot1.hand_little = req.hand[0]
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
	if req.action_list[8] == 1:
		cur.reef_p = 0
	if req.action_list[7] == 1:
		cur.reef_r = 0
	if req.action_list[6] == 1:
		cur.reef_l = 0
	# cur.reef_p = req.action_list[8]
	# cur.reef_l = req.action_list[6]
	# cur.reef_r = req.action_list[7]
	cur.windsock = req.action_list[1]
	cur.flag = req.action_list[3]
	cur.lhouse = req.action_list[2]
	cur.time = req.time
	cur.emergency = req.emergency
	cur.enemy_1= e1
	cur.enemy_2 = e2
	cur.friend_pos = req.friend_pos
	if req.team == 0: 
		# blue : ( no, ( x, y ), 1 for cup still there 0 for cup gone,  2  for green 3 for red, type : private 0 or public 1 )
		cur.cup_state = [  { 'no' : 1, 'location' : [1200, 300, 0], 'state' : 1, 'color' : 2, 'type' : 0 , 'robot_pos' : []}, { 'no' : 2, 'location' : [ 1085, 445, 0 ], 'state' : 1, 'color' : 3, 'type' : 0 ,'robot_pos' : []},
			{ 'no' : 3, 'location' :[ 515, 445, 0], 'state' : 1, 'color' : 2, 'type' : 0 , 'robot_pos' : []} , { 'no' : 4,'location' : [ 400, 300, 0 ], 'state' : 1, 'color' : 3, 'type' : 0 , 'robot_pos' : []},
			{ 'no' : 5, 'location' : [ 100, 670, 0 ], 'state' : 1, 'color' : 2, 'type' : 1 , 'robot_pos' : []}, { 'no' : 6, 'location' : [ 400, 956, 0 ], 'state' : 1, 'color' : 3, 'type' : 1,  'robot_pos' : []}, 
			{ 'no' : 7, 'location' : [ 800, 1100, 0 ], 'state' : 1, 'color' : 2, 'type' : 1 , 'robot_pos' : []},{ 'no' : 8, 'location' : [ 1200, 1270, 0 ], 'state' : 1, 'color' : 3, 'type' : 1 , 'robot_pos' : []},
			{ 'no' : 9, 'location' : [ 1200, 1730, 0 ], 'state' : 1, 'color' : 2, 'type' : 1 , 'robot_pos' : []}, { 'no' : 10, 'location' : [ 800, 1900, 0 ], 'state' : 1, 'color' : 3, 'type' : 1 ,'robot_pos' : []},
			{ 'no' : 11, 'location' : [ 400, 2044, 0 ], 'state' : 1, 'color' : 2, 'type' : 1 ,'robot_pos' : []},  { 'no' : 12, 'location' : [ 100, 2330, 0 ], 'state' : 1, 'color' : 3, 'type' : 1 ,'robot_pos' : []},
			{ 'no' : 13, 'location' : [ 1655, 1665, 0 ], 'state' : 0, 'color' : 2, 'type' : 0 ,'robot_pos' : []}, { 'no' : 14, 'location' : [ 1655, 1935, 0 ], 'state' : 0, 'color' : 3, 'type' : 0 ,'robot_pos' : []},
			{ 'no' : 15, 'location' : [ 1955, 1605, 0 ], 'state' : 0, 'color' : 3, 'type' : 0 ,'robot_pos' : []}, { 'no' : 16, 'location' : [ 1955, 1995, 0 ], 'state' : 0, 'color' : 2, 'type' : 0 ,'robot_pos' : []},
			{ 'no' : 17, 'location' : [ 0, 0, 0 ], 'state' : 0, 'color' : 3, 'type' : 1 ,'robot_pos' : []}, { 'no' : 18, 'location' : [ 0, 0, 0 ], 'state' : 0, 'color' : 3, 'type' : 1 ,'robot_pos' : []},
			{ 'no' : 19, 'location' : [ 0, 0, 0 ], 'state' : 0, 'color' : 3, 'type' : 1 ,'robot_pos' : []}, { 'no' : 20, 'location' : [ 0, 0, 0 ], 'state' : 0, 'color' : 3, 'type' : 1 ,'robot_pos' : []},
			{ 'no' : 21, 'location' : [ 0, 0, 0 ], 'state' : 0, 'color' : 3, 'type' : 1 ,'robot_pos' : []}, { 'no' : 22, 'location' : [ 0, 0, 0 ], 'state' : 0, 'color' : 3, 'type' : 1 ,'robot_pos' : []},
			{ 'no' : 23, 'location' : [ 0, 0, 0 ], 'state' : 0, 'color' : 3, 'type' : 1 ,'robot_pos' : []}, { 'no' : 24, 'location' : [ 0, 0, 0 ], 'state' : 0, 'color' : 3, 'type' : 1 ,'robot_pos' : []}]

		#no, name, location, NS, reefp, reefr, reefl, windsock, flag, lhouse, time, reward, effect[reefp, reefr, reefl, windsock, flag, lhouse]
		windsock = Mission_precondition( 1, "windsock", ( 2000, 430, 0), None, None, None, None, 0, None, None, 8, 50, [None, None, None, 1, None, None,])
		lhouse = Mission_precondition( 2, "lhouse", ( 0, 300, 0 ), None, None, None, None, None, None, 0, 2, 50,[None, None, None, None, None, 1])
		getcup = Mission_precondition( 12, "getcup", ( 0, 0, 0), None, None, None, None, None, None, None, 5, 20,[None, None, None, None, None, None])
		#special case for cup 12 34
		getcup_12 = Mission_precondition( 13, "getcup_12", ( 1085, 400, 0), None, None, None, None, None, None, None, 5, 1300,[None, None, None, None, None, None])
		getcup_34 = Mission_precondition( 14, "getcup_34", ( 500, 400, 0), None, None, None, None, None, None, None, 5, 1300,[None, None, None, None, None, None])
		#reef cup counts separately
		reef_private = Mission_precondition( 8, "reef_private", ( 1600, 0, 0 ), None, 1, None,  None, None, None, None, 9, 500,[0, None, None, None, None, None])
		reef_left = Mission_precondition( 6, "reef_left", ( 50, 850, 0 ), None, None, None, 1, None, None, None, 9, 200,[None, None, 0, None, None, None])
		reef_right = Mission_precondition(7, "reef_right", ( 50, 2150, 0 ), None, None,1, None,  None, None, None, 9, 200,[None, 0, None, None, None, None])
		placecup_reef = Mission_precondition( 11, "placecup_reef", ( 800, 200, 0 ), None, None, None, None, None, None, None, 10, 10000,[None, None, None, None, None, None])
		placecupP = Mission_precondition( 10, "placecupP", ( 515, 200, 0 ), None, None, None, None, None, None, None, 10, 40,[None, None, None, None, None, None])
		placecupH = Mission_precondition( 9, "placecupH", ( 1850, 1800, 0 ), None, None, None, None, None, None, None, 10, 40,[None, None, None, None, None, None])
		#temporay set that it has to be done last
		anchorN = Mission_precondition( 4, "anchorN", (300, 200, 0 ), 0, None, None, None, None, None, None, 2, 10000,[None, None, None, None, None, None])
		anchorS = Mission_precondition( 5, "anchorS", ( 1300, 200, 0 ), 1, None, None, None, None, None, None, 2, 10000,[None, None, None, None, None, None])
		flag = Mission_precondition( 3, "flag", None, None, None, None, 1, 1, 0, 1, 0, 20000,[None, None, None, None, 1, None])

		#little mission blue
		windsock.little_mission_count = 2
		windsock.location = [1850, 200, math.pi / 2]
		windsock.little_mission_pos = [ [1850, 200, math.pi / 2], [1850, 700, math.pi / 2]]
		windsock.little_mission_no = [ 1, 15]
		lhouse.little_mission_count = 3
		lhouse.location = [100, 275, math.pi ]
		lhouse.little_mission_pos = [ [100, 275, math.pi ], [ 50, 275, math.pi], [100, 275, math.pi ]]
		lhouse.little_mission_no = [ 2, 16, 17]
		reef_left.little_mission_count = 3
		reef_left.location = [80, 850, math.pi]
		reef_left.little_mission_pos = [ [80, 850, math.pi], [50, 850, math.pi],  [80, 850, math.pi]]
		reef_left.little_mission_no = [ 7, 26, 27]
		reef_right.little_mission_count = 3
		reef_right.location = [80, 850, math.pi]
		reef_right.little_mission_pos = [ [80, 850, math.pi], [50, 2150, math.pi],  [80, 850, math.pi]]
		reef_right.little_mission_no = [ 6, 24, 25]
		reef_private.little_mission_count = 3
		reef_private.location = [1600, 80, -math.pi / 2]
		reef_private.little_mission_pos = [ [1600, 80, -math.pi / 2], [1600, 50, -math.pi / 2],  [1600, 80, -math.pi / 2]]
		reef_private.little_mission_no = [ 8, 28, 29]
		placecup_reef.little_mission_count = 2
		placecup_reef.little_mission_no = [ 11, 30]
		placecup_reef.little_mission_pos = [[ 800, 200, 0 ],[ 800, 200, 0 ] ]
	elif req.team == 1: 
		# yellow : ( no, ( x, y ), 1 for cup still there 0 for cup gone,  2  for green 3 for red, type : private 0 or public 1 )
		cur.cup_state = [  { 'no' : 1, 'location' : [ 1200, 2700, 0 ], 'state' : 1, 'color' : 2, 'type' : 0 ,'robot_pos' : []}, { 'no' : 2, 'location' : [ 1085, 2555, 0 ], 'state' : 1, 'color' : 3, 'type' : 0 ,'robot_pos' : []},
			{ 'no' : 3, 'location' : [ 515, 2555, 0 ], 'state' : 1, 'color' : 2, 'type' : 0 ,'robot_pos' : []} , { 'no' : 4,'location' : [ 400, 2700, 0 ], 'state' : 1, 'color' : 3, 'type' : 0 ,'robot_pos' : []},
			{ 'no' : 5, 'location' : [ 100, 670, 0 ], 'state' : 1, 'color' : 2, 'type' : 1 ,'robot_pos' : []}, { 'no' : 6, 'location' : [ 400, 956, 0 ], 'state' : 1, 'color' : 3, 'type' : 1 ,'robot_pos' : []}, 
			{ 'no' : 7, 'location' : [ 800, 1100, 0 ], 'state' : 1, 'color' : 2, 'type' : 1 ,'robot_pos' : []}, { 'no' : 8, 'location' : [ 1200, 1270, 0 ], 'state' : 1, 'color' : 3, 'type' : 1 ,'robot_pos' : []},
			{ 'no' : 9, 'location' : [ 1200, 1730, 0 ], 'state' : 1, 'color' : 2, 'type' : 1 ,'robot_pos' : []}, { 'no' : 10, 'location' : [ 800, 1900, 0 ], 'state' : 1, 'color' : 3, 'type' : 1 ,'robot_pos' : []},
			{ 'no' : 11, 'location' : [ 400, 2044, 0 ], 'state' : 1, 'color' : 2, 'type' : 1 ,'robot_pos' : []},  { 'no' : 12, 'location' : [ 100, 2330, 0 ], 'state' : 1, 'color' : 3, 'type' : 1 ,'robot_pos' : []},
			{ 'no' : 13, 'location' : [ 1655, 1065, 0 ], 'state' : 0, 'color' : 2, 'type' : 0 ,'robot_pos' : []}, { 'no' : 14, 'location' : [ 1655, 1335, 0 ], 'state' : 0, 'color' : 3, 'type' : 0 ,'robot_pos' : []},
			{ 'no' : 15, 'location' : [ 1955, 1005, 0 ], 'state' : 0, 'color' : 3, 'type' : 0 ,'robot_pos' : []}, { 'no' : 16, 'location' : [ 1955, 1395, 0 ], 'state' : 0, 'color' : 2, 'type' : 0 ,'robot_pos' : []},
			{ 'no' : 17, 'location' : [ 0, 0, 0 ], 'state' : 0, 'color' : 3, 'type' : 1 ,'robot_pos' : []}, { 'no' : 18, 'location' : [ 0, 0, 0 ], 'state' : 0, 'color' : 3, 'type' : 1 ,'robot_pos' : []},
			{ 'no' : 19, 'location' : [ 0, 0, 0 ], 'state' : 0, 'color' : 3, 'type' : 1 ,'robot_pos' : []}, { 'no' : 20, 'location' : [ 0, 0, 0 ], 'state' : 0, 'color' : 3, 'type' : 1 ,'robot_pos' : []},
			{ 'no' : 21, 'location' : [ 0, 0, 0 ], 'state' : 0, 'color' : 3, 'type' : 1 ,'robot_pos' : []}, { 'no' : 22, 'location' : [ 0, 0, 0 ], 'state' : 0, 'color' : 3, 'type' : 1 ,'robot_pos' : []},
			{ 'no' : 23, 'location' : [ 0, 0, 0 ], 'state' : 0, 'color' : 3, 'type' : 1 ,'robot_pos' : []}, { 'no' : 24, 'location' : [ 0, 0, 0 ], 'state' : 0, 'color' : 3, 'type' : 1 ,'robot_pos' : []}]
		
		#name, location, NS, reefp, reefr, reefl, windsock, flag, lhouse, time, reward, effect[reefp, reefr, reefl, windsock, flag, lhouse]
		windsock = Mission_precondition( 1, "windsock", ( 2000, 2330, 0), None, None, None, None, 0, None, None, 8, 50, [None, None, None, 1, None, None])
		lhouse = Mission_precondition( 2, "lhouse", ( 0, 2775, 0 ), None, None, None, None, None, None, 0, 2, 50,[None, None, None, None, None, 1])
		getcup = Mission_precondition( 12, "getcup", ( 0, 0, 0), None, None, None, None, None, None, None, 5, 20,[None, None, None, None, None, None])
		#special case for cup 12 34
		getcup_12 = Mission_precondition( 13, "getcup_12", ( 1085, 2600, 0), None, None, None, None, None, None, None, 10, 1300,[None, None, None, None, None, None])
		getcup_34 = Mission_precondition( 14, "getcup_34", ( 500, 2600, 0), None, None, None, None, None, None, None, 10, 1300,[None, None, None, None, None, None])
		#reef cup counts separately
		reef_private = Mission_precondition( 8, "reef_private", ( 1600, 3000, 0 ), None, None, 1, None, None, None, None, 9, 500,[0, None, None, None, None, None])
		reef_left = Mission_precondition( 6, "reef_left", ( 0, 850, 0 ), None, None, None, 1, None, None, None, 9, 200,[None, None, 0, None, None, None])
		reef_right = Mission_precondition(7, "reef_right", ( 0, 2150, 0 ), None, None, None, 1, None, None, None, 9, 200,[None, 0, None, None, None, None])
		placecup_reef = Mission_precondition( 11, "placecup_reef", ( 800, 2775, 0 ), None, None, None, None, None, None, None, 10, 10000,[None, None, None, None, None, None])
		placecupP = Mission_precondition( 10, "placecupP", ( 515, 2775, 0 ), None, None, None, None, None, None, None, 10, 40,[None, None, None, None, None, None])
		placecupH = Mission_precondition( 9, "placecupH", ( 1850, 1200, 0 ), None, None, None, None, None, None, None, 10, 40,[None, None, None, None, None, None])
		#temporay set that it has to be done last
		anchorN = Mission_precondition( 4, "anchorN", (300, 2775, 0 ), 0, None, None, None, None, None, None, 2, 10000,[None, None, None, None, None, None])
		anchorS = Mission_precondition( 5, "anchorS", ( 1300, 2775, 0 ), 1, None, None, None, None, None, None, 2, 10000,[None, None, None, None, None, None])
		flag = Mission_precondition( 3, "flag", None, None, None, None, 1, 1, 0, 1, 0, 20000,[None, None, None,None, 1,  None])	

		#little mission yellow
		windsock.little_mission_count = 2
		windsock.location = [1850, 2800, 90]
		windsock.little_mission_pos = [ [1850, 2800, 90], [1850, 2300, 90]]
		windsock.little_mission_no = [ 1, 15]
		lhouse.little_mission_count = 3
		lhouse.location = [100, 3725, 180 ]
		lhouse.little_mission_pos = [ [100, 3725, 180 ], [ 50, 3725, 180], [100, 3725, 180 ]]
		lhouse.little_mission_no = [ 2, 16, 17]
		reef_left.little_mission_count = 3
		reef_left.location = [80, 850, math.pi]
		reef_left.little_mission_pos = [ [80, 850, math.pi], [50, 850, math.pi],  [80, 850, math.pi]]
		reef_left.little_mission_no = [ 6, 24, 25]
		reef_right.little_mission_count = 3
		reef_right.location = [80, 850, math.pi]
		reef_right.little_mission_pos = [ [80, 2150, math.pi], [50, 2150, math.pi],  [80, 2150, math.pi]]
		reef_right.little_mission_no = [ 7, 26, 27]
		reef_private.little_mission_count = 3
		reef_private.location = [1600, 3920, math.pi / 2]
		reef_private.little_mission_pos = [ [1600, 3920, math.pi / 2], [1600, 3950, math.pi / 2],  [1600, 3920, math.pi / 2]]
		reef_private.little_mission_no = [ 8, 28, 29]
		placecup_reef.little_mission_count = 2
		placecup_reef.little_mission_no = [ 11, 30]
		placecup_reef.little_mission_pos = [[ 800, 2700, 0 ],[ 800, 2700, 0 ] ]
	cur.leaf = [ windsock, lhouse, reef_private, reef_right, reef_left, placecup_reef,  anchorN, anchorS, flag] # change item in this array to set what action is to be considered in goap
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
	# cur.reef_l = 1
	# cur.reef_p = 1
	# cur.reef_r = 1
	return cur, robot1
	
def cup_location_transfrom(cup_state):
	#clean previous robot pos
	for cup in cup_state:
		del cup['robot_pos'][:]
	# set parameter here 
	r = 50 #expansion radius
	n = 8 # how many dot per each cup
	x = 0
	y = 0
	theta = 0
	border = 100 #margin from each border
	cup_margin = 200 #margin for not to hit other cup
	angle = math.pi / n 
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
					if cup['no'] <= 16 and cup['no'] >= 13: #check if hit the wall at harbour 
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
						cup['robot_pos'].append( [x, y, theta] )
		# print("cup", cup['no'], len(cup['robot_pos']))

def distance(a, b):
	if a != None and b != None:
		d =int((abs( a[0] - b[0] )**2 + abs( a[1] - b[1])**2))**0.5
		return d
	else:
		return None
