import math
# import rospy
# from goap_.srv import *
from srv_vs import *
from setting_goap_vs import *

def checkpreconditions( current, mis, robot):
    margin = 30
    for m in mis:
        if m.name == 'getcup':
            if robot.freestorage > 0 and current.time < 90:
                cupp = cup_cost( current, m, robot )
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
        # print("cand", len(current.candidate))
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
            if friend_action[0] == 12:
                if friend_action[1] != cup_state[c]['no']:
                    mission = cup_state[c]
                    i = 0
                else: 
                    c += 1
            else:
                mission = cup_state[c]
                i = 0
            # print( 'cup debug', cup_state[c])
            
        elif c >= len(cup_state) - 1:
            mission = None
            i = 0
        else:
            c += 1
    return mission

def refreshstate(current, mission, robot):
    global cup_state 
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
    if mission.location != None:
        current.location = mission.location
    def myFunc(e):
        return e['no']
    cup_state.sort(key=myFunc)
#compare cost of missions
def compare_cost( array ):
    def myFunc(e):
        return e.cost
    array.sort(key=myFunc)

def distance(a, b):
    d = int((abs( a[0] - b[0] )**2 + abs( a[1] - b[1])**2)**0.5)
    return d

def emergency(current):
    location = cur.location
    #back away distance
    d = 50
    theta = current.location[2]
    rad = theta * math.pi / 180
    (x, y) = ( location[0], location[1])
    count = 0
    state = 0
    while state == 0:
        #back off in the opposite direction
        x -= math.cos(rad) * d
        y -= math.sin(rad) * d
        #check if ( x, y ) will hit the border
        if x < 50:
            x = 50
            rad += math.pi / 4
        elif x > 1950:
            x = 1950
            rad += math.pi / 4
        elif y < 50:
            y = 50
            rad += math.pi / 4
        elif y > 2950:
            y = 2950
            rad += math.pi / 4
        #check if ( x, y ) will hit cup or not
        else:
            for c in cup_state:
                if (x, y) == c['location']:
                    rad += math.pi / 4
                    break
                else:
                    count += 1
            if count == len(cup_state):
                state = 1
    location = ( int(x), int(y), theta)
    current.location = location
    return location

def evaluate(current, robot):
    score = 0
    red = 0
    green = 0
    cup = 0
    #number of times place cup when there is no freestorage
    num = int(len(current.cup_order) / robot.cupstorage)
    mm = 0
    for m in current.achieved:
        if m.name == 'windsock':
            score += 15 * 2
        elif m.name == 'lhouse':
            score += 10
        elif m.name == 'anchorN' or  m.name == 'anchorS':
            score += 10
        elif  m.name == 'flag':
            score += 10
        elif m.name == 'placecup_reef':
            score += 2*5 + 2*2
    #cup score
    score += 2 * len(current.cup_order)
    for i in range(0, len(current.cup_order)):
        if current.cup_order[i]['color'] == 2:
            green += 1
        else:
            red += 1
    #calculate how many paired cup
    if red > green:
        score += 2 * green
    else:
        score += 2 * red
    return score

# my_pos[0, 0, 0]
# NS = 0
# emergency = 0
# time = 0

def GOAP():
    tmp = 0
    mission = len(cur.mission_list)
    state = 1
    
    # while state == 1:
    if cur.emergency == 0:
        while cur.time < 95:
            # print("time", cur.time)
            leaf = [ anchorN, anchorS, flag, windsock, lhouse, getcup, reef_private, reef_left, reef_right, placecupP, placecupH, placecup_reef ]
            del cur.mission_list[:]
            friend = 0
            for a in range(0, len(action_list)):
                if action_list[a] == 0:
                    for m in leaf:
                        if m.no == a :
                            if m.no == friend_action and (friend_action == 1 or friend_action == 2 or friend_action == 6 or friend_action == 7 or friend_action == 8 or friend_action == 9 or friend_action == 10 or friend_action == 11):
                                friend = 1
                            else:
                                friend = 0
                                cur.mission_list.append(m)
                if action_list[a] == 1:
                    for m in leaf:
                        if m.no == a:
                            refreshstate(cur, m, robot1)
            # print("time", cur.time)
            if tmp  == 0:
            #check if current states meet preconditions
                checkpreconditions(cur, cur.mission_list, robot1)
                compare_cost(cur.candidate)
                cur.achieved.append(cur.candidate[0])
                refreshstate(cur, cur.candidate[0], robot1)
                tmp = tmp + 1
            else:
                checkpreconditions(cur, cur.mission_list, robot1)           
                if len(cur.candidate) != 0:
                    compare_cost(cur.candidate)
                    # print("aa", cur.candidate[0].name)
                    cur.achieved.append(cur.candidate[0])
                    refreshstate(cur, cur.candidate[0], robot1)
                else:
                    cur.time += 1
            #cur.candidate.clear()
            del cur.candidate[:]

        cur.achieved.append(flag)
        if cur.NS == anchorN.NS:
            cur.achieved.append(anchorN)
        else:
            cur.achieved.append(anchorS)

        temp = 0
        i = 0
        # action = []*len(cur.achieved)[]*5
        action = [[0 for x in range(len(cur.achieved))] for y in range(5)] 
        # action = array((len(cur.achieved), 5))
        ff = 0
        for a in cur.achieved: 
            if a.name == 'getcup':
                action.append([cur.cup_order[temp]['location'][0], cur.cup_order[temp]['location'][1], cur.cup_order[temp]['location'][2], 12, cur.cup_order[temp]['no']])
                temp = temp + 1
                i += 1
            else:
                if ff == 3:
                    action.append([a.location[0], a.location[1], a.location[2], 3, 0])
                    ff = 0
                if a.location != None:
                    action.append([a.location[0], a.location[1], a.location[2], a.no, 0])
                    i += 1
                else:#flag has no location so i need to give next mission's location
                    ff = 3
        mission_list = []
        temp = 0
        for a in cur.achieved:
            if a.name == 'getcup':
                print("temp", temp)
                c = (a.name, (cur.cup_order[temp]['location']))
                mission_list.append(c)
                temp = temp + 1
            else:
                # print("achieved", a.name, a.location)
                c = (a.name, a.location)
                mission_list.append(c)

        score = evaluate(cur, robot1)
        print("score", score)
        for p in mission_list:
            print("mission_list", p)
        state = 0
    else:
        #return location (x, y, theta), try to get out
        location = emergency(cur)
        print("emergency", location) 

# def GOAP_server():
#     rospy.init_node('GOAP_server')
#     s = rospy.Service('GOAP', goap, GOAP)
#     rospy.spin()         

# if __name__ == "__main__":
#     GOAP_server()
GOAP()