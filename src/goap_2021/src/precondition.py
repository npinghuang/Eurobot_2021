"""
check mission precondition and refresh current state
=======================================================
"""
#!/usr/bin/env python
#coding=utf-8

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
                    m.cost = distance( current.location, m.location ) - m.reward * ( robot.cupstorage - robot.freestorage - 12 ) + m.time
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
    # calculate distance
    for cup in current.cup_state:
        d = distance( current.location, cup[ 'location' ])
        cup['distance'] = d

    def myFunc(e):
        return e['distance']
    current.cup_state.sort(key=myFunc)
    i = 1
    c = 0
    #check if cup is still there
    while i == 1 :
        if current.cup_state[c]['state'] == 1:
            if req.friend_action[0] == 12:
                if req.friend_action[1] != current.cup_state[c]['no']:
                    mission = current.cup_state[c]
                    i = 0
                else: 
                    c += 1
            else:
                mission = current.cup_state[c]
                i = 0
            # print( 'cup debug', current.cup_state[c])
        elif current.cup_state[c]['state'] == 0:
            c += 1 
        if c >= len(current.cup_state) - 1:
            mission = None
            i = 0
        
    return mission

def refreshstate(current, mission, robot, state):
    #state =  1 -> this mission is done by self robotl; state = 0 -> this mission is done by other 
    if mission.name == "getcup":
        robot.cup(1)
        current.cup_order.append(mission.cup)
        for c in current.cup_state:
            if mission.location == c['location']:
                c['state'] = 0

    elif mission.name == 'placecupH' or mission.name == 'placecupP':
        n = robot.cupstorage - robot.freestorage
        robot.cup(-n)

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

def distance(a, b):
    d =int((abs( a[0] - b[0] )**2 + abs( a[1] - b[1])**2))**0.5
    return d

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

