import math
current.cup_state[a]['hand'] = ,current.cup_state[b]['hand'] = 0
#old cup_cost
def cup_cost(req, current, mission, robot):
    cup_location_transfrom(current.cup_state)
    #see claw suction state ( whether they have room to take cup )]
    front_claw = [ 0, 0 ]
    back_claw = [ 0, 0 ]
    front_suction = [ 0, 0 ] #[0] for green [1] for red
    back_suction = [ 0, 0 ] #[0] for green [1] for red
    for claw in robot.claw:
        if claw['state'] == 0: #claw['color'] == cup['color'] and  
            if claw['no'] <= 1:
                front_claw[ claw['color'] - 2 ] = 1
            elif claw['no'] > 1:
                back_claw[ claw['color'] - 2 ] = 1
    for suc in robot.suction:
        if suc['state'] == 0: # suc['color'] == cup['color'] and 
            if suc['no'] <= 3 and front_suction [ suc['color'] - 2 ] == 0:
                front_suction [ suc['color'] - 2 ] = 1
            elif suc['no'] > 3 and back_suction [ suc['color'] - 2 ] == 0:
                back_suction [ suc['color'] - 2 ] = 1
    for cup in current.cup_state:
		#determine front or back
        case = ''
        if (front_suction[ cup['color'] - 2 ] ==1 or front_claw[ cup['color'] - 2 ]  == 1) and (back_suction[ cup['color'] - 2 ] == 1 or back_claw[ cup['color'] - 2 ] == 1):
            case = front_back_determination( current.location, cup['location'])
        elif back_suction[ cup['color'] - 2 ] == 1 or back_claw[ cup['color'] - 2 ] == 1:
            case = 'back'
        elif front_suction[ cup['color'] - 2 ] ==1 or front_claw[ cup['color'] - 2 ]  == 1:
            case = 'front'
		
        #determine the closest distance between each cup
        if case == 'front':
            turn = 0
        elif case == 'back':
            turn = -math.pi
        if len(cup['robot_pos']) > 0:
            # print("cup debug", cup['no'], cup['robot_pos'][0])
            d = distance( cup['robot_pos'][0], current.location)
            for pos in cup['robot_pos']:
                pos[2] += turn
                dd = distance( pos, current.location)
                if dd > d:
                    cup['robot_pos'].remove(pos)
                else:
                    d = dd
            cup['distance'] = d
        else:
            cup['distance'] = 9999999999
        
	#find closest cup
    def myFunc(e):
        return e['distance']
    current.cup_state.sort(key=myFunc)
    i = 1
    c = 0
    #check if cup is still there and determine use which hand
    # case = 'none'
    while i == 1 :
        case = 'none'
        if current.cup_state[c]['state'] == 1:
            if req.friend_action[0] == 12: #check it is not the same cup as friend's action
                if req.friend_action[1] != current.cup_state[c]['no']:
                    mission = current.cup_state[c]
                    mission.location = current.cup_state[c]['robot_pos'][0]
                    #both front and back hand is availalbe
                    if (front_claw[ (current.cup_state[c]['color'] - 2)] == 1 or front_suction[ (current.cup_state[c]['color'] - 2)] == 1) and (back_claw[ (current.cup_state[c]['color'] - 2)] == 1 or back_suction[ (current.cup_state[c]['color'] - 2)] == 1): #determine use front or back
                        case = front_back_determination( current.location, current.cup_state[c]['robot_pos'][0])
                        # i = 0
                    elif front_claw[ (current.cup_state[c]['color'] - 2)] == 1 or front_suction[ (current.cup_state[c]['color'] - 2)] == 1: #only front is available
                        case = 'front'
                        # i = 0
                    elif back_claw[ (current.cup_state[c]['color'] - 2)] == 1 or back_suction[ (current.cup_state[c]['color'] - 2)] == 1: #only back is available
                        case = 'back'
                        # i = 0
                    else:
                        c += 1
                    if case != 'none':
                        mission = current.cup_state[c]
                else: 
                    c += 1
            else:
                #both front and back hand is availalbe
                if (front_claw[ (current.cup_state[c]['color'] - 2)] == 1 or front_suction[ (current.cup_state[c]['color'] - 2)] == 1) and (back_claw[ (current.cup_state[c]['color'] - 2)] == 1 or back_suction[ (current.cup_state[c]['color'] - 2)] == 1): #determine use front or back
                    case = front_back_determination( current.location, current.cup_state[c]['robot_pos'][0])
                    # i = 0
                elif front_claw[ (current.cup_state[c]['color'] - 2)] == 1 or front_suction[ (current.cup_state[c]['color'] - 2)] == 1: #only front is available
                    case = 'front'
                    # i = 0
                elif back_claw[ (current.cup_state[c]['color'] - 2)] == 1 or back_suction[ (current.cup_state[c]['color'] - 2)] == 1: #only back is available
                    case = 'back'
                    # i = 0
                else:
                    c += 1
                if case != 'none':
                    mission = current.cup_state[c]
                
            # print( 'cup debug', current.cup_state[c])
        elif current.cup_state[c]['state'] == 0:
            print("debug no cup", current.cup_state[c]['no'])
            c += 1 
        if c >= len(current.cup_state) - 1:
            mission = None
            i = 0
            return mission
        # else:
        #     print("you should think carefully cup state", current.cup_state[c]['state'])
        #     if len(current.cup_state[c]['robot_pos']) > 0:
        #         mission = current.cup_state[c]
        #         mission['location'] = current.cup_state[c]['robot_pos'][0]
        #         # print("de", mission['no'], case, current.cup_state[c]['no'])
        #         i = 0
        #     else:
        #         c += 1
	print("so crazy", c,  mission)
    if case == 'front' and mission != None:
        print("check if there is bug")
        if mission['color'] == 2:
            if front_claw[0] == 1:
                mission['location'][0] -= robot.claw[0]['location'][0] * math.cos(robot.claw[0]['location'][2])
                mission['location'][1] -= robot.claw[0]['location'][1] * math.sin(robot.claw[0]['location'][2])
                mission['location'][2] += robot.claw[0]['location'][2]
                mission['hand'] = 0
            elif front_suction[0] == 1:
                mission['location'][0] -= robot.suction[0]['location'][0] * math.cos(robot.suction[0]['location'][2])
                mission['location'][1] -= robot.suction[0]['location'][1] * math.sin(robot.suction[0]['location'][2])
                mission['location'][2] += robot.suction[0]['location'][2]
                mission['hand' ] = 4
            else:
                case = 'back'
        else:#red
            if front_claw[1] == 1:
                mission['location'][0] -= robot.claw[1]['location'][0] * math.cos(robot.claw[1]['location'][2])
                mission['location'][1] -= robot.claw[1]['location'][1] * math.sin(robot.claw[1]['location'][2])
                mission['location'][2] += robot.claw[1]['location'][2]
                # tmp = mission['location'][2] + robot.claw[1]['location'][2]
                # mission['location'][2] = tmp
                mission['hand'] = 1
            elif front_suction[1] == 1:
                mission['location'][0] -= robot.suction[2]['location'][0] * math.cos(robot.suction[2]['location'][2])
                mission['location'][1] -= robot.suction[2]['location'][1] * math.sin(robot.suction[2]['location'][2])
                mission['location'][2] += robot.suction[2]['location'][2]
                mission['hand' ] = 5
    elif case == 'back' and mission != None:
        if mission['color'] == 2:
            if back_claw[0] == 1:
                mission['location'][0] -= robot.claw[3]['location'][0] * math.cos(robot.claw[3]['location'][2])
                mission['location'][1] -= robot.claw[3]['location'][1] * math.sin(robot.claw[3]['location'][2])
                mission['location'][2] += robot.claw[3]['location'][2]
                mission['hand'] = 3
            elif back_suction[0] == 1:
                mission['location'][0] -= robot.suction[7]['location'][0] * math.cos(robot.suction[7]['location'][2])
                mission['location'][1] -= robot.suction[7]['location'][1] * math.sin(robot.suction[7]['location'][2])
                mission['location'][2] += robot.suction[7]['location'][2]
                mission['hand' ] = 7
            else:
                mission = None
        else:#red
            if back_claw[1] == 1:
                mission['location'][0] -= robot.claw[2]['location'][0] * math.cos(robot.claw[2]['location'][2])
                mission['location'][1] -= robot.claw[2]['location'][1] * math.sin(robot.claw[2]['location'][2])
                mission['location'][2] += robot.claw[2]['location'][2]
                mission['hand'] = 2
            elif back_suction[1] == 1:
                mission['location'][0] -= robot.suction[6]['location'][0] * math.cos(robot.suction[6]['location'][2])
                mission['location'][1] -= robot.suction[6]['location'][1] * math.sin(robot.suction[6]['location'][2])
                mission['location'][2] += robot.suction[6]['location'][2]
                mission['hand' ] = 6   
    elif case == 'none':
        mission = None
    # if mission != None:
        # print("cup", mission['no'], mission['location'], case) #,  mission['hand']
    del front_claw[:]
    del back_claw[:]
    del front_suction[:]
    del back_suction[:]
    return mission
# blue : [ no, [ x, y ], 1 for cup still there 0 for cup gone,  2  for green 3 for red, type : private 0 or public 1 ]
cup_state = [  { 'no' : 1, 'location' : [1200, 300, 0], 'state' : 1, 'color' : 2, 'type' : 0 }, { 'no' : 2, 'location' : [ 1085, 445, 0 ], 'state' : 1, 'color' : 3, 'type' : 0 },
			{ 'no' : 3, 'location' :[ 515, 445, 0], 'state' : 1, 'color' : 2, 'type' : 0 } , { 'no' : 4,'location' : [ 400, 300, 0 ], 'state' : 1, 'color' : 3, 'type' : 0 },
			{ 'no' : 5, 'location' : [ 100, 670, 0 ], 'state' : 1, 'color' : 2, 'type' : 1 }, { 'no' : 6, 'location' : [ 400, 956, 0 ], 'state' : 1, 'color' : 3, 'type' : 1 }, 
			{ 'no' : 7, 'location' : [ 800, 1100, 0 ], 'state' : 1, 'color' : 2, 'type' : 1 }, { 'no' : 8, 'location' : [ 1200, 1270, 0 ], 'state' : 1, 'color' : 3, 'type' : 1 },
			{ 'no' : 9, 'location' : [ 1200, 1730, 0 ], 'state' : 1, 'color' : 2, 'type' : 1 }, { 'no' : 10, 'location' : [ 800, 1900, 0 ], 'state' : 1, 'color' : 3, 'type' : 1 },
			{ 'no' : 11, 'location' : [ 400, 2044, 0 ], 'state' : 1, 'color' : 2, 'type' : 1 },  { 'no' : 12, 'location' : [ 100, 2330, 0 ], 'state' : 1, 'color' : 3, 'type' : 1 },
			{ 'no' : 13, 'location' : [ 1655, 1665, 0 ], 'state' : 1, 'color' : 2, 'type' : 0 }, { 'no' : 14, 'location' : [ 1655, 1935, 0 ], 'state' : 1, 'color' : 3, 'type' : 0 },
			{ 'no' : 15, 'location' : [ 1955, 1605, 0 ], 'state' : 1, 'color' : 3, 'type' : 0 }, { 'no' : 16, 'location' : [ 1955, 1995, 0 ], 'state' : 1, 'color' : 2, 'type' : 0 },
			{ 'no' : 17, 'location' : [ 0, 0, 0 ], 'state' : 0, 'color' : 3, 'type' : 1 }, { 'no' : 18, 'location' : [ 0, 0, 0 ], 'state' : 0, 'color' : 3, 'type' : 1 },
			{ 'no' : 19, 'location' : [ 0, 0, 0 ], 'state' : 0, 'color' : 3, 'type' : 1 }, { 'no' : 20, 'location' : [ 0, 0, 0 ], 'state' : 0, 'color' : 3, 'type' : 1 },
			{ 'no' : 21, 'location' : [ 0, 0, 0 ], 'state' : 0, 'color' : 3, 'type' : 1 }, { 'no' : 22, 'location' : [ 0, 0, 0 ], 'state' : 0, 'color' : 3, 'type' : 1 },
			{ 'no' : 23, 'location' : [ 0, 0, 0 ], 'state' : 0, 'color' : 3, 'type' : 1 }, { 'no' : 24, 'location' : [ 0, 0, 0 ], 'state' : 0, 'color' : 3, 'type' : 1 }]
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
						# print("bump", cup['no'], x, y, case)
					#check if hit other cup or not
					tmp = 0
					while tmp != -1 and tmp < len(cup_state) and case == 1:
						if cup['no'] != cup_state[tmp]['no'] and cup_state[tmp]['state'] == 1: #not to examine the same cup
							d = distance( cup_state[tmp]['location'], [ x, y ] )
							# print("debug", cup['no'], cup_state[tmp]['no'], d)
							if d < cup_margin:
								tmp = -1
							else:
								tmp += 1
						else:
							tmp += 1
					if tmp != -1 and case == 1:
						cup['robot_pos'].append( [x, y, theta] )
						# print("robot pos", cup['no'], [x, y, theta] )
					# else:
					# 	print("boom")
		print("cup", cup['no'], len(cup['robot_pos']))



def front_back_determination( current, pos):
	x = current[0]
	y = current[1]
	theta = current[2]
	
	line = ( y + x / (math.tan(theta))) * pos[0] + ( x + y * ( math.tan( theta ))) * pos[1]
	tmp = ( y + x / (math.tan(theta))) * ( x + y * ( math.tan( theta )))
	# 1 for back 0 for front
	if line < tmp:
		return 'back'
	else:
		return 'front'
def distance(a, b):
    d =int((abs( a[0] - b[0] )**2 + abs( a[1] - b[1])**2))**0.5
    return d	
# cup_location_transfrom(cup_state)
cc = front_back_determination( [800, 1500, math.pi  ], cup_state[0]['location'])

print("hungry", cc)

def cup_cost(req, current, mission, robot):
    #see claw suction state ( whether they have room to take cup )
    claw_pos = []
    suction_pos = []
    front_claw = [ 0, 0 ]
    back_claw = [ 0, 0 ]
    front_suction = [ 0, 0 ] #[0] for green [1] for red
    back_suction = [ 0, 0 ] #[0] for green [1] for red
    for claw in robot.claw:
        if claw['state'] == 0: #claw['color'] == cup['color'] and  
            if claw['no'] <= 1:
                front_claw[ claw['color'] - 2 ] = 1
            elif claw['no'] > 1:
                back_claw[ claw['color'] - 2 ] = 1
    for suc in robot.suction:
        if suc['state'] == 0: # suc['color'] == cup['color'] and 
            if suc['no'] <= 3 and front_suction [ suc['color'] - 2 ] == 0:
                front_suction [ suc['color'] - 2 ] = 1
            elif suc['no'] > 3 and back_suction [ suc['color'] - 2 ] == 0:
                back_suction [ suc['color'] - 2 ] = 1
    # calculate distance and see front or back which is closer
    f = 100 #the distance between origin of robot and the front of the robot
    delta_x = f * math.cos( current.location[2])
    delta_y = f * math.sin( current.location[2])
    front_location = [ (delta_x + current.location[0]), (delta_y + current.location[1]), current.location[2]]
    back_location = [ (-delta_x + current.location[0]), (-delta_y + current.location[1]), (current.location[2] + math.pi)]
    for cup in current.cup_state:
		#determine front or back
		if (front_suction[ cup['color'] - 2 ] ==1 or front_claw[ cup['color'] - 2 ]  == 1) and (back_suction[ cup['color'] - 2 ] == 1 or back_claw[ cup['color'] - 2 ] == 1):
            case = front_back_determination( current.location, cup['location'])
        elif back_suction[ cup['color'] - 2 ] == 1 or back_claw[ cup['color'] - 2 ] == 1:
            case = 'back'
		elif front_suction[ cup['color'] - 2 ] ==1 or front_claw[ cup['color'] - 2 ]  == 1:
			case = 'front'
		
		#determine the closest distance between each cup
		if case == 'front':
			turn = 0
		elif case == 'back':
			turn = -math.pi
		d = distance( cup['robot_pos'][0], current.location)
		for pos in cup['robot_pos']:
			pos[2] += turn
			dd = distance( pos, current.location)
			if dd > d:
				cup['robot_pos'].remove(pos)
			else:
				d = dd
		cup['distance'] = d
        
	#find closest cup
    def myFunc(e):
        return e['distance']
    current.cup_state.sort(key=myFunc)
    i = 1
    c = 0
    #check if cup is still there and determine use which hand
    case = 'none'
    while i == 1 :
        if current.cup_state[c]['state'] == 1:
            if req.friend_action[0] == 12: #check it is not the same cup as friend's action
                if req.friend_action[1] != current.cup_state[c]['no']:
                    mission = current.cup_state[c]
                    #both front and back hand is availalbe
                    if (front_claw[ (current.cup_state[c]['color'] - 2)] == 1 or front_suction[ (current.cup_state[c]['color'] - 2)] == 1) and (back_claw[ (current.cup_state[c]['color'] - 2)] == 1 or back_suction[ (current.cup_state[c]['color'] - 2)] == 1): #determine use front or back
                        case = front_back_determination( current.location, current.cup_state[c]['robot_pos'][0])
                    elif front_claw[ (current.cup_state[c]['color'] - 2)] == 1 or front_suction[ (current.cup_state[c]['color'] - 2)] == 1: #only front is available
                        case = 'front'
                    elif back_claw[ (current.cup_state[c]['color'] - 2)] == 1 or back_suction[ (current.cup_state[c]['color'] - 2)] == 1: #only back is available
                        case = 'back'
                    i = 0
                else: 
                    c += 1
            else:
                mission = current.cup_state[c]
				mission.location = current.cup_state[c]['robot_pos'][0]
                #both front and back hand is availalbe
                if (front_claw[ (current.cup_state[c]['color'] - 2)] == 1 or front_suction[ (current.cup_state[c]['color'] - 2)] == 1) and (back_claw[ (current.cup_state[c]['color'] - 2)] == 1 or back_suction[ (current.cup_state[c]['color'] - 2)] == 1): #determine use front or back
                        case = front_back_determination( current.location, current.cup_state[c]['robot_pos'][0])
				elif front_claw[ (current.cup_state[c]['color'] - 2)] == 1 or front_suction[ (current.cup_state[c]['color'] - 2)] == 1: #only front is available
					case = 'front'
				elif back_claw[ (current.cup_state[c]['color'] - 2)] == 1 or back_suction[ (current.cup_state[c]['color'] - 2)] == 1: #only back is available
					case = 'back'
                i = 0
            # print( 'cup debug', current.cup_state[c])
        elif current.cup_state[c]['state'] == 0:
            c += 1 
        if c >= len(current.cup_state) - 1:
            mission = None
            i = 0
			
    if case == 'front':
        print("check if there is bug")
        if mission['color'] == 2:
            if front_claw[0] == 1:
                mission['location'][0] -= robot.claw[0]['location'][0] * math.cos(robot.claw[0]['location'][2])
                mission['location'][1] -= robot.claw[0]['location'][1] * math.sin(robot.claw[0]['location'][2])
                mission['location'][2] += robot.claw[0]['location'][2]
                mission['hand'] = 0
            elif front_suction[0] == 1:
                mission['location'][0] -= robot.suction[0]['location'][0] * math.cos(robot.suction[0]['location'][2])
                mission['location'][1] -= robot.suction[0]['location'][1] * math.sin(robot.suction[0]['location'][2])
                mission['location'][2] += robot.suction[0]['location'][2]
                mission['hand' ] = 4
        else:#red
            if front_claw[1] == 1:
                mission['location'][0] -= robot.claw[1]['location'][0] * math.cos(robot.claw[1]['location'][2])
                mission['location'][1] -= robot.claw[1]['location'][1] * math.sin(robot.claw[1]['location'][2])
                mission['location'][2] += robot.claw[1]['location'][2]
                # tmp = mission['location'][2] + robot.claw[1]['location'][2]
                # mission['location'][2] = tmp
                mission['hand'] = 1
            elif front_suction[1] == 1:
                mission['location'][0] -= robot.suction[2]['location'][0] * math.cos(robot.suction[2]['location'][2])
                mission['location'][1] -= robot.suction[2]['location'][1] * math.sin(robot.suction[2]['location'][2])
                mission['location'][2] += robot.suction[2]['location'][2]
                mission['hand' ] = 5
    elif case == 'back':
        if mission['color'] == 2:
            if back_claw[0] == 1:
                mission['location'][0] -= robot.claw[3]['location'][0] * math.cos(robot.claw[3]['location'][2])
                mission['location'][1] -= robot.claw[3]['location'][1] * math.sin(robot.claw[3]['location'][2])
                mission['location'][2] += robot.claw[3]['location'][2]
                mission['hand'] = 3
            elif back_suction[0] == 1:
                mission['location'][0] -= robot.suction[7]['location'][0] * math.cos(robot.suction[7]['location'][2])
                mission['location'][1] -= robot.suction[7]['location'][1] * math.sin(robot.suction[7]['location'][2])
                mission['location'][2] += robot.suction[7]['location'][2]
                mission['hand' ] = 7
        else:#red
            if back_claw[1] == 1:
                mission['location'][0] -= robot.claw[2]['location'][0] * math.cos(robot.claw[2]['location'][2])
                mission['location'][1] -= robot.claw[2]['location'][1] * math.sin(robot.claw[2]['location'][2])
                mission['location'][2] += robot.claw[2]['location'][2]
                mission['hand'] = 2
            elif back_suction[1] == 1:
                mission['location'][0] -= robot.suction[6]['location'][0] * math.cos(robot.suction[6]['location'][2])
                mission['location'][1] -= robot.suction[6]['location'][1] * math.sin(robot.suction[6]['location'][2])
                mission['location'][2] += robot.suction[6]['location'][2]
                mission['hand' ] = 6   
    elif case == 'none':
        mission = None
    if mission != None:
        print("cup", mission['no'], mission['location'], case) #,  mission['hand']
    del front_claw[:]
    del back_claw[:]
    del front_suction[:]
    del back_suction[:]
    return mission