"""
check mission precondition and refresh current state
=======================================================
"""
from setting_bigchicken import *
def checkpreconditions( current, mis, robot):
    margin = 30
    for m in mis:
        if m.name == 'getcup':
            if robot.freestorage > 0 and current.time < 90:
                cup = cup_cost( current, m, robot )
                if cup != None:
                    m.cost = distance( current.location, cup[ 'location' ] )- m.reward + m.time
                    m.location = cup[ 'location' ]
                    m.cup = cup
                    if abs(cup['location'][0] - current.enemy_1[0] ) > margin and abs(cup['location'][1] - current.enemy_1[1] ) > margin and abs(cup['location'][0] - current.enemy_2[0] ) > margin and abs(cup['location'][1] - current.enemy_2[1] ) > margin:
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
            if robot1.reef == 1 and current.reef_p == 1 and (abs(m.location[0] - current.enemy_1[0] ) > margin and abs(m.location[1] - current.enemy_1[1] ) > margin and abs(m.location[0] - current.enemy_2[0] ) > margin and abs(m.location[1] - current.enemy_2[1] ) > margin):
                m.cost = distance( current.location, m.location ) - m.reward + m.time
                current.candidate.append(m)
        elif m.name == 'reef_left':
            if robot1.reef == 1 and current.reef_l == 1 and (abs(m.location[0] - current.enemy_1[0] ) > margin and abs(m.location[1] - current.enemy_1[1] ) > margin and abs(m.location[0] - current.enemy_2[0] ) > margin and abs(m.location[1] - current.enemy_2[1] ) > margin):
                m.cost = distance( current.location, m.location ) - m.reward + m.time
                current.candidate.append(m)
        elif m.name == 'reef_right':
            if robot1.reef == 1 and current.reef_r == 1 and (abs(m.location[0] - current.enemy_1[0] ) > margin and abs(m.location[1] - current.enemy_1[1] ) > margin and abs(m.location[0] - current.enemy_2[0] ) > margin and abs(m.location[1] - current.enemy_2[1] ) > margin):
                m.cost = distance( current.location, m.location ) - m.reward + m.time
                current.candidate.append(m)
        elif m.name == 'placecup_reef':
            if current.placecup_reef == 1 and (abs(m.location[0] - current.enemy_1[0] ) > margin and abs(m.location[1] - current.enemy_1[1] ) > margin and abs(m.location[0] - current.enemy_2[0] ) > margin and abs(m.location[1] - current.enemy_2[1] ) > margin):
                m.cost = distance( current.location, m.location ) - m.reward + m.time
                current.candidate.append(m)
def cup_cost(current, mission, robot):
    global cup_state 
    # calculate distance
    for cup in cup_state:
        d = distance( current.location, cup[ 'location' ])
        global cup_state
        cup['distance'] = d

    def myFunc(e):
        return e['distance']
    cup_state.sort(key=myFunc)

    i = 1
    c = 0
    #check if cup is still there
    while i == 1 :
        if cup_state[c]['state'] == 1:
            mission = cup_state[c]
            # print( 'cup debug', cup_state[c])
            i = 0
        elif c >= len(cup_state) - 1:
            mission = None
            i = 0
        else:
            c += 1
    return mission

def refreshstate(current, mission, robot):
    if mission.name == "getcup":
        global cup_state
        robot.cup(1)
        current.cup_order.append(mission.cup)
        for c in cup_state:
            if mission.location == c['location']:
                c['state'] = 0

    elif mission.name == 'placecupH' or mission.name == 'placecupP':
        n = robot1.cupstorage - robot1.freestorage
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
    # print("refresh", current.cup_num, current.windsock)
    if mission.location != None:
        current.location = mission.location
    
#compare cost of missions
def compare_cost( array ):
    def myFunc(e):
        return e.cost

    array.sort(key=myFunc)
    # for c in array:
        # print("can_sort", c.name, c.cost)

def distance(a, b):
    d = int((abs( a[0] - b[0] )**2 + abs( a[1] - b[1])**2)**0.5)
    return d
