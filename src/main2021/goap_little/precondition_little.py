"""
check mission precondition and refresh current state
=======================================================
"""
#!/usr/bin/env python
#coding=utf-8
import math
from setting_little_goap import *
# from cup_cost import*

def checkpreconditions( req, current, mis, robot):
    for m in mis:
        # print("debug mis name ", m.name)
        boom1 = 1
        boom2 = 1
        boomf = 1
        if m.location != None and current.enemy_1  != None and current.enemy_2 != None  and current.friend_pos != None:
            boom1 = check_boom( m.location, current.enemy_1)
            boom2 = check_boom( m.location, current.enemy_2)
            boomf = check_boom( m.location, current.friend_pos )
        if m.name == 'windsock':
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
            # print(" current ", current.reef_p, "placecup", current.placecup_reef,  "boom *  3", boom1, boom2, boomf)
            if robot.reef == 1 and current.placecup_reef == 0 and current.reef_p == 1 and boom1 ==  1 and boom2 == 1 and boomf == 1:
                # print("debug reef p")
                m.cost = distance( current.location, m.location ) - m.reward + m.time
                current.candidate.append(m)
        elif m.name == 'reef_left':
            if robot.reef == 1 and current.placecup_reef == 0 and current.reef_l == 1 and boom1 ==  1 and boom2 == 1 and boomf == 1:
                m.cost = distance( current.location, m.location ) - m.reward + m.time
                current.candidate.append(m)
        elif m.name == 'reef_right':
            if robot.reef == 1 and current.placecup_reef == 0 and current.reef_l == 1 and boom1 ==  1 and boom2 == 1 and boomf == 1:
                m.cost = distance( current.location, m.location ) - m.reward + m.time
                current.candidate.append(m)
        elif m.name == 'placecup_reef':
            # print(" current ", robot.reef, "placecup", current.placecup_reef,  "boom *  3", boom1, boom2, boomf)
            if robot.reef == 1 and current.placecup_reef == 1 and boom1 ==  1 and boom2 == 1 and boomf == 1:
                m.cost = distance( current.location, m.location ) - m.reward + m.time
                current.candidate.append(m)
        # print("cand", len(current.candidate))

def refreshstate(current, mission, robot, state):
    
    
    if state == 0:
        print("debug")
        current.placecup_reef = robot.hand_little
    if state == 2:
        if m.no == 6:
            current.reef_l = 0
        elif m.no == 7:
            current.reef_r = 0
        elif m.no == 8:
            current.reef_p = 0
        
    if state == 1:
        if mission.name != 'flag':
            d = distance( current.location, mission.location )
            rotate = rotate_time( current.location, mission.location )
            current.time += mission.time + d / velocity  + rotate
        if mission.location != None:
            current.location = mission.location
        #state =  1 -> this mission is done by self robotl; state = 0 -> this mission is done by other 
        if mission.effect[0] != None:
            # print("debug refresh state")
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
        if state == 1 and mission.name == 'placecup_reef':
            current.placecup_reef = 0    
        elif state == 1 and( mission.name == 'reef_private' or mission.name == 'reef_right' or mission.name == 'reef_left'):
            current.placecup_reef = 1 
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
