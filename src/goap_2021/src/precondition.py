"""
check mission precondition and refresh current state
=======================================================
"""
#!/usr/bin/env python
#coding=utf-8

from setting_goap import *
def checkpreconditions( req, current, mis, robot):
    margin = 30
    for m in mis:
        if m.name == 'getcup':
            if robot.freestorage > 0 and current.time < 90:
                cupp = cup_cost( req, current, m, robot )
                if cupp != None:
                    m.cost = distance( current.location, cupp[ 'location' ] )- m.reward + m.time
                    m.location = cupp[ 'location' ]
                    m.cup = cupp
                    if abs(cupp['location'][0] - current.enemy_1[0] ) > margin and abs(cupp['location'][1] - current.enemy_1[1] ) > margin and abs(cupp['location'][0] - current.enemy_2[0] ) > margin and abs(cupp['location'][1] - current.enemy_2[1] ) > margin:
                        current.candidate.append(m)
        elif m.name == 'placecupP' or m.name == 'placecupH':
            if robot.freestorage < robot.cupstorage and abs(m.location[0] - current.enemy_1[0] ) > margin and abs(m.location[1] - current.enemy_1[1] ) > margin and abs(m.location[0] - current.enemy_2[0] ) > margin and abs(m.location[1] - current.enemy_2[1] ) > margin:
                if current.time < 70:
                    m.cost = distance( current.location, m.location ) - m.reward * ( robot.cupstorage - robot.freestorage - 12 ) + m.time
                else:
                    m.cost = distance( current.location, m.location ) - m.reward * (100 * ( robot.cupstorage - robot.freestorage ))**5 + m.time
                current.candidate.append(m)
        elif m.name == 'windsock':
            if current.windsock != 1 and (abs(m.location[0] - current.enemy_1[0] ) > margin and abs(m.location[1] - current.enemy_1[1] ) > margin and abs(m.location[0] - current.enemy_2[0] ) > margin and abs(m.location[1] - current.enemy_2[1] ) > margin):
                m.cost = distance( current.location, m.location ) - m.reward + m.time
                current.candidate.append(m)
        elif m.name == 'lhouse':
            if current.lhouse != 1 and (abs(m.location[0] - current.enemy_1[0] ) > margin and abs(m.location[1] - current.enemy_1[1] ) > margin and abs(m.location[0] - current.enemy_2[0] ) > margin and abs(m.location[1] - current.enemy_2[1] ) > margin):
                m.cost = distance( current.location, m.location ) - m.reward + m.time
                current.candidate.append(m)
        elif m.name == 'flag':
            if current.time >= 95 and (abs(m.location[0] - current.enemy_1[0] ) > margin and abs(m.location[1] - current.enemy_1[1] ) > margin and abs(m.location[0] - current.enemy_2[0] ) > margin and abs(m.location[1] - current.enemy_2[1] ) > margin):
                m.cost = distance( current.location, m.location ) - m.reward + m.time
                current.candidate.append(m)
        elif m.name == 'anchorN' or m.name == 'anchorS':
            if current.NS == m.NS and current.time > 97 and (abs(m.location[0] - current.enemy_1[0] ) > margin and abs(m.location[1] - current.enemy_1[1] ) > margin and abs(m.location[0] - current.enemy_2[0] ) > margin and abs(m.location[1] - current.enemy_2[1] ) > margin):
                m.cost = distance( current.location, m.location ) - m.reward + m.time
                current.candidate.append(m)
        elif m.name == 'reef_private':
            if robot.reef == 1 and current.reef_p == 1 and (abs(m.location[0] - current.enemy_1[0] ) > margin and abs(m.location[1] - current.enemy_1[1] ) > margin and abs(m.location[0] - current.enemy_2[0] ) > margin and abs(m.location[1] - current.enemy_2[1] ) > margin):
                m.cost = distance( current.location, m.location ) - m.reward + m.time
                current.candidate.append(m)
        elif m.name == 'reef_left':
            if robot.reef == 1 and current.reef_l == 1 and (abs(m.location[0] - current.enemy_1[0] ) > margin and abs(m.location[1] - current.enemy_1[1] ) > margin and abs(m.location[0] - current.enemy_2[0] ) > margin and abs(m.location[1] - current.enemy_2[1] ) > margin):
                m.cost = distance( current.location, m.location ) - m.reward + m.time
                current.candidate.append(m)
        elif m.name == 'reef_right':
            if robot.reef == 1 and current.reef_r == 1 and (abs(m.location[0] - current.enemy_1[0] ) > margin and abs(m.location[1] - current.enemy_1[1] ) > margin and abs(m.location[0] - current.enemy_2[0] ) > margin and abs(m.location[1] - current.enemy_2[1] ) > margin):
                m.cost = distance( current.location, m.location ) - m.reward + m.time
                current.candidate.append(m)
        elif m.name == 'placecup_reef':
            if current.placecup_reef == 1 and (abs(m.location[0] - current.enemy_1[0] ) > margin and abs(m.location[1] - current.enemy_1[1] ) > margin and abs(m.location[0] - current.enemy_2[0] ) > margin and abs(m.location[1] - current.enemy_2[1] ) > margin):
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
            
        elif c >= len(current.cup_state) - 1:
            mission = None
            i = 0
        else:
            c += 1
    return mission

def refreshstate(current, mission, robot):
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

    if mission.name == 'flag':
        current.time += mission.effect[5]
    else:
        d = distance( current.location, mission.location )
        current.time += mission.time + d / 500 
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
    d = int((abs( a[0] - b[0] )**2 + abs( a[1] - b[1])**2)**0.5)
    return d
