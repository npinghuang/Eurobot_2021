"""
check mission precondition and refresh current state
=======================================================
"""
#!/usr/bin/env python
#coding=utf-8
import math
from setting_big_goap import *
from cup_cost import*

def checkpreconditions( req, current, mis, robot):
    for m in mis:
        boom1 = 1
        boom2 = 1
        boomf = 1
        if m.location != None and current.enemy_1  != None and current.enemy_2 != None  and current.friend_pos != None:
            boom1 = check_boom( m.location, current.enemy_1)
            boom2 = check_boom( m.location, current.enemy_2)
            boomf = check_boom( m.location, current.friend_pos )
        if m.name == 'getcup':
            if robot.freestorage > 0 and current.time < 70:
                cupp = cup_cost( req, current, m, robot )
                if cupp != None:
                    # print("debug cup no", cupp['no'])
                    m.cost = distance( current.location, cupp[ 'location' ] )- m.reward + m.time
                    m.location = cupp[ 'location' ]
                    m.cup = cupp
                    # print("cup no  check pre", cupp['no'])
                    if cupp['location'] != None and current.enemy_1  != None and current.enemy_2 != None  and current.friend_pos != None:
                        boom1 = check_boom( cupp['location'], current.enemy_1)
                        boom2 = check_boom( cupp['location'], current.enemy_2)
                        boomf = check_boom( cupp['location'], current.friend_pos)
                    if boom1 ==  1 and boom2 == 1 and boomf == 1:
                    # if abs(cupp['location'][0] - current.enemy_1[0] ) > margin and abs(cupp['location'][1] - current.enemy_1[1] ) > margin and abs(cupp['location'][0] - current.enemy_2[0] ) > margin and abs(cupp['location'][1] - current.enemy_2[1] ) > margin:
                        current.candidate.append(m)
        elif (m.name == 'getcup_12' or m.name == 'getcup_34' ):#and m not in current.achieved
            # print("why!!", m.name)
            if m.name == 'getcup_12': #cup number
                if req.team == 0: #blue
                    a = 2-1
                    b = 4-1
                elif req.team == 1:#yellow
                    a = 22-1
                    b = 24-1
            elif m.name == 'getcup_34':
                if req.team == 0: #blue
                    a = 1-1
                    b = 3-1
                elif req.team == 1:#yellow
                    a = 21-1
                    b = 23-1
            if boom1 ==  1 and boom2 == 1 and boomf == 1:
                def myFunc(e):
                    return e['no']
                current.cup_state.sort(key=myFunc)
                # print( "debug cup no ",m.name,  robot.freestorage, current.cup_state[a]['no'], current.cup_state[a]['state'], current.cup_state[b]['no'],  current.cup_state[b]['state'])
                if robot.freestorage > 1 and current.cup_state[a]['state'] == 1 and current.cup_state[b]['state'] == 1:#check if there is room for two cup
                    state = 1
                    if (robot.claw[0]['state'] == 0 and robot.claw[1]['state'] == 0 ) and (robot.claw[2]['state'] ==0 and robot.claw[3]['state'] == 0):#check if hand 0 and 1 or 2 or 3 are free
                        face = front_back_determination( current.location, m.location)
                    elif robot.claw[0]['state'] == 0 and robot.claw[1]['state'] == 0:
                        face = 'front'
                    elif robot.claw[2]['state'] ==0 and robot.claw[3]['state'] == 0:
                        face = 'back'
                    else: #no free hand
                        state = 0
                    if state == 1:
                        if face == 'front':
                            current.cup_state[a]['hand'] = 1
                            current.cup_state[b]['hand'] = 0
                        elif face == 'back':
                            current.cup_state[a]['hand'] = 2
                            current.cup_state[b]['hand'] = 3
                        m.cup.append( current.cup_state[a] )
                        m.cup.append( current.cup_state[b] )
                        # print( "debug cup no ",m.name,  current.cup_state[a]['no'], current.cup_state[b]['no'], "hand", current.cup_state[a]['hand'] )
                        m.cost = distance( current.location, m.location ) - m.reward + m.time
                        # print("debug", m.name)
                        current.candidate.append(m)
                        # print("debug", m.name, current.cup_state[a]['hand'])
        elif m.name == 'placecupP' or m.name == 'placecupH':
            if robot.freestorage < robot.cupstorage and boom1 ==  1 and boom2 == 1 and boomf == 1:
                if current.time < 70:
                    m.cost = distance( current.location, m.location ) - m.reward * ( robot.cupstorage - robot.freestorage - 12 )*1000 + m.time
                else:
                    m.cost = distance( current.location, m.location ) - m.reward * (100 * ( robot.cupstorage - robot.freestorage ))**5 + m.time
                # print("preee place cup", robot.freestorage)
                current.candidate.append(m)
        elif m.name == 'windsock':
            # print("windsock", current.windsock,boom1, boom2, boomf)
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

def refreshstate(current, mission, robot, state):
    #state =  1 -> this mission is done by self robotl; state = 0 -> this mission is done by other 
    if mission.name == "getcup":
        robot.cup(1)
        current.cup_order.append(mission.cup)
        # print("lalal", mission.cup)
        if mission.cup['hand'] < 4:#claw
            robot.claw[mission.cup['hand']]['state'] = 1
        elif mission.cup['hand'] >= 4:#suction
            robot.suction[mission.cup['hand'] - 4]['state'] = 1
            i = 2 * (mission.cup['hand'] - 4)
            # if robot.suction[ i ]['state'] == 0:
            #     robot.suction[ i ]['state'] = 1
            # elif robot.suction[ i ]['state'] == 1 and robot.suction[ i + 1 ]['state'] == 0:
            #     robot.suction[ i + 1 ]['state'] = 1
        for c in current.cup_state:
            if mission.location == c['location']:
                c['state'] = 0
    elif mission.name == 'getcup_12' or mission.name == 'getcup_34' :
        if state == 1:
            robot.cup(2) #update robot cup storage status
            current.cup_order.append(mission.cup[0])
            current.cup_order.append(mission.cup[1])
            robot.claw[mission.cup[0]['hand']]['state'] = 1
            robot.claw[mission.cup[1]['hand']]['state'] = 1
            current.cup_state[mission.cup[0]['no'] - 1]['state'] = 0
            current.cup_state[mission.cup[1]['no'] - 1]['state'] = 0        
    elif mission.name == 'placecupH' or mission.name == 'placecupP':
        n = robot.cupstorage - robot.freestorage
        robot.cup(-n)
        # print("place cup", robot.freestorage)
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
            if mission.effect[5] != None:
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
    # print("sort", array[0].name, array[0].cost)
    cost_min = array[0].cost
    min_no = 0
    # ii = 0
    # for d in array:
    #     print("sort for", d.name, d.cost)
    #     if d.cost <= cost_min:
    #         cost_min = d.cost
    #         min_no = ii
    #     ii += 1
    # print("cost min", array[min_no].name, array[min_no].cost)
    
    return array[min_no]
    # key2 = min(array, key = lambda k: k.cost)
    # print("key2", key2.name)
    # return key2

def rotate_time(a, b):
    r = abs( a[2] - b[2])
    time = r / angular_velocity
    return time

#calculate the distance betwwen two robot and determine if it will bump into each other
#just to clarify, this stupid name is named by susan hahaha
def check_boom( a, b ):
    margin = 50
    distance_boom = distance(a,b)
    if distance_boom == None:
        return True
    elif distance_boom < margin:
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
