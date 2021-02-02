"""
check mission precondition and refresh current state
=======================================================
"""
#!/usr/bin/env python
#coding=utf-8
import math
from setting_big_goap import *
def checkpreconditions( req, current, mis, robot):
    for m in mis:
        if m.location != None:
            boom1 = check_boom( m.location, current.enemy_1)
            boom2 = check_boom( m.location, current.enemy_2)
            boomf = check_boom( m.location, current.friend_pos )
        if m.name == 'getcup':
            if robot.freestorage > 0 and current.time < 90:
                cupp = cup_cost( req, current, m, robot )
                if cupp != None:
                    # print("debug cup no", cupp['no'])
                    m.cost = distance( current.location, cupp[ 'location' ] )- m.reward + m.time
                    m.location = cupp[ 'location' ]
                    m.cup = cupp
                    boom1 = check_boom( cupp['location'], current.enemy_1)
                    boom2 = check_boom( cupp['location'], current.enemy_2)
                    boomf = check_boom( cupp['location'], current.friend_pos)
                    if boom1 ==  1 and boom2 == 1 and boomf == 1:
                    # if abs(cupp['location'][0] - current.enemy_1[0] ) > margin and abs(cupp['location'][1] - current.enemy_1[1] ) > margin and abs(cupp['location'][0] - current.enemy_2[0] ) > margin and abs(cupp['location'][1] - current.enemy_2[1] ) > margin:
                        current.candidate.append(m)
        elif m.name == 'placecupP' or m.name == 'placecupH':
            if robot.freestorage < robot.cupstorage and boom1 ==  1 and boom2 == 1 and boomf == 1:
                if current.time < 70:
                    m.cost = distance( current.location, m.location ) - m.reward * ( robot.cupstorage - robot.freestorage - 12 )*1000 + m.time
                else:
                    m.cost = distance( current.location, m.location ) - m.reward * (100 * ( robot.cupstorage - robot.freestorage ))**5 + m.time
                current.candidate.append(m)
        elif m.name == 'windsock':
            if current.windsock != 1 and boom1 ==  1 and boom2 == 1 and boomf == 1:
                m.cost = distance( current.location, m.location ) - m.reward + m.time
                current.candidate.append(m)
        elif m.name == 'lhouse':
            # print("lhouse", current.lhouse,boom1, boom2, boomf)
            if current.lhouse != 1 and boom1 == 1 and boom2 == 1 and boomf == 1:
                m.cost = distance( current.location, m.location ) - m.reward + m.time 
                current.candidate.append(m)
                # print("debug", m.cost)
        elif m.name == 'flag':
            if current.time >= 95 :
                m.cost =  - m.reward + m.time
                current.candidate.append(m)
        elif m.name == 'anchorN' or m.name == 'anchorS':
            if current.NS == m.NS and current.time > 97 and boom1 ==  1 and boom2 == 1 and boomf == 1:
                m.cost = distance( current.location, m.location ) - m.reward + m.time
                current.candidate.append(m)
        elif m.name == 'reef_private':
            if robot.reef == 1 and current.reef_p == 1 and boom1 ==  1 and boom2 == 1 and boomf == 1:
                m.cost = distance( current.location, m.location ) - m.reward + m.time
                current.candidate.append(m)
        elif m.name == 'reef_left':
            if robot.reef == 1 and current.reef_l == 1 and boom1 ==  1 and boom2 == 1 and boomf == 1:
                m.cost = distance( current.location, m.location ) - m.reward + m.time
                current.candidate.append(m)
        elif m.name == 'reef_right':
            if robot.reef == 1 and current.reef_r == 1 and boom1 ==  1 and boom2 == 1 and boomf == 1:
                m.cost = distance( current.location, m.location ) - m.reward + m.time
                current.candidate.append(m)
        elif m.name == 'placecup_reef':
            if current.placecup_reef == 1 and boom1 ==  1 and boom2 == 1 and boomf == 1:
                m.cost = distance( current.location, m.location ) - m.reward + m.time
                current.candidate.append(m)
        # print("cand", len(current.candidate))

def cup_cost(req, current, mission, robot):
    cup_location_transfrom(current.cup_state)
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
        # if len(cup['robot_pos']) > 0:
        #     print("debug robot_pos", cup['no'],  cup['robot_pos'])
        #     d = distance( cup['robot_pos'][0], current.location)
        # else:
        #     mission = None
        #     return mission
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
        if current.cup_state[c]['state'] == 1:
            if req.friend_action[0] == 12: #check it is not the same cup as friend's action
                if req.friend_action[1] != current.cup_state[c]['no']:
                    mission = current.cup_state[c]
                    mission.location = current.cup_state[c]['robot_pos'][0]
                    #both front and back hand is availalbe
                    if (front_claw[ (current.cup_state[c]['color'] - 2)] == 1 or front_suction[ (current.cup_state[c]['color'] - 2)] == 1) and (back_claw[ (current.cup_state[c]['color'] - 2)] == 1 or back_suction[ (current.cup_state[c]['color'] - 2)] == 1): #determine use front or back
                        case = front_back_determination( current.location, current.cup_state[c]['robot_pos'][0])
                    elif front_claw[ (current.cup_state[c]['color'] - 2)] == 1 or front_suction[ (current.cup_state[c]['color'] - 2)] == 1: #only front is available
                        case = 'front'
                    elif back_claw[ (current.cup_state[c]['color'] - 2)] == 1 or back_suction[ (current.cup_state[c]['color'] - 2)] == 1: #only back is available
                        case = 'back'
                    else:
                        case = 'none'
                    i = 0
                else: 
                    c += 1
            else:
                mission = current.cup_state[c]
                mission['location'] = current.cup_state[c]['robot_pos'][0]
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
        # print("cup", mission['no'], mission['location'], case) #,  mission['hand']
    del front_claw[:]
    del back_claw[:]
    del front_suction[:]
    del back_suction[:]
    return mission
def refreshstate(current, mission, robot, state):
    #state =  1 -> this mission is done by self robotl; state = 0 -> this mission is done by other 
    if mission.name == "getcup":
        robot.cup(1)
        current.cup_order.append(mission.cup)
        if mission.cup['hand'] < 4:#claw
            robot.claw[mission.cup['hand']]['state'] = 1
        elif mission.cup['hand'] >= 4:#suction
            i = 2 * (mission.cup['hand'] - 4)
            if robot.suction[ i ]['state'] == 0:
                robot.suction[ i ]['state'] = 1
            elif robot.suction[ i ]['state'] == 1 and robot.suction[ i + 1 ]['state'] == 0:
                robot.suction[ i + 1 ]['state'] = 1
        for c in current.cup_state:
            if mission.location == c['location']:
                c['state'] = 0
    elif mission.name == 'placecupH' or mission.name == 'placecupP':
        n = robot.cupstorage - robot.freestorage
        robot.cup(-n)
        for claw in robot.claw:
            claw['state'] = 0
        for suc in robot.suction:
            suc['state'] = 0
        

    if mission.effect[0] != None:
        current.reef_p = mission.effect[0]
        current.placecup_reef = 1
    if mission.effect[1] != None:
        current.reef_r = mission.effect[1]
        current.placecup_reef = 1
    if mission.effect[2] != None:
        current.reef_l = mission.effect[2]
        current.placecup_reef = 1
    if mission.effect[3] != None:
        current.windsock = mission.effect[3]
    if mission.effect[4] != None:
        current.flag = mission.effect[4]
    if mission.effect[5] != None:
        current.lhouse = mission.effect[5]
    if mission.name == 'placecup_reef':
        current.placecup_reef = 0        

    if state == 1:
        if mission.name == 'flag':
            current.time += mission.effect[5]
        else:
            d = distance( current.location, mission.location )
            rotate = rotate_time( current.location, mission.location )
            current.time += mission.time + d / velocity  + rotate
        if mission.location != None:
            current.location = mission.location
    def myFunc(e):
        return e['no']
    current.cup_state.sort(key=myFunc)
#compare cost of missions
def compare_cost( array ):
    def myFunc(e):
        return e.cost
    array.sort(key=myFunc)

def rotate_time(a, b):
    r = abs( a[2] - b[2])
    time = r / angular_velocity
    return time

#calculate the distance betwwen two robot and determine if it will bump into each other
#just to clarify, this stupid name is named by susan hahaha
def check_boom( a, b ):
    margin = 50
    distance_boom = distance(a,b)
    if distance_boom < margin:
        return False #don't go to that mission
    else:
        return True

def front_back_determination( current, pos):
    x = current[0]
    y = current[1]
    theta = current[2]
    if (theta == math.pi  / 2):
        # print("tan90", math.tan(math.pi/2))
        tangent = 1
    elif  theta ==( -math.pi / 2):
        tangent = -1
    else:
        tangent = math.tan(theta)
    if tangent == 0:
        line = ( y) * pos[0] + ( x + y * (tangent)) * pos[1]
        tmp = ( y ) * ( x + y * (tangent))
    else:
        line = ( y + x / tangent) * pos[0] + ( x + y * (tangent)) * pos[1]
        tmp = ( y + x / tangent) * ( x + y * (tangent))
    # 1 for back 0 for front
    if line < tmp:
        return 'back'
    else:
		return 'front'
