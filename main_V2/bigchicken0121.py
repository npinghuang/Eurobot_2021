import math
from setting_bigchicken import *
from precondition_bigchicken import *

def emergency(current):
    location = cur.location
    #back away distance
    d = 50
    theta = cur.location[2]
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
    cur.location = location
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
        # print("name", m.name, score)
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

location_setting = input ("Enter starting location = 1 no = 0 :") 
if location_setting == 1:
    cur.location = ( 800, 200, 0 )
else:
    x = input ("Enter location x : ")
    y = input ("Enter location y : ")
    theta = input ("Enter location theta : ")
    cur.location = (x, y, theta) 

cur.emergency = input ("Enter emergency = 1 non-emergency = 0 :") 
print("emergency", cur.emergency) 


leaf = [ anchorN, anchorS, flag, windsock, lhouse, getcup, reef_private, reef_left, reef_right, placecupP, placecupH, placecup_reef ]
tmp = 0
mission = len(leaf)
state = 1

while state == 1:
    if cur.emergency == 0:
        while cur.time < 95:
            # print("time", cur.time)
            if tmp  == 0:
            #check if current states meet preconditions
                checkpreconditions(cur, leaf, robot1)
                compare_cost(cur.candidate)
                cur.achieved.append(cur.candidate[0])
                refreshstate(cur, cur.candidate[0], robot1)
                tmp = tmp + 1
            else:
                checkpreconditions(cur, leaf, robot1)           
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
                
        mission_list = []
        temp = 0
        for a in cur.achieved:
            if a.name == 'getcup':
                # print("achieved", a.name, cur.cup_order[temp])
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
        cur.emergency = input ("Enter emergency = 1 non-emergency = 0 :") 
        
