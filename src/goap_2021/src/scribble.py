import math
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
		return 1
	else:
		return 0
def distance(a, b):
    d =int((abs( a[0] - b[0] )**2 + abs( a[1] - b[1])**2))**0.5
    return d	
# cup_location_transfrom(cup_state)
cc = front_back_determination( [800, 1500, math.pi  ], cup_state[0]['location'])

print("hungry", cc)
	
	
	