# ( ( x, y ), 1 for cup still there 0 for cup gone,  2  for green 3 for red, type : private 0 or public 1 )
cup_state = [ { 'location' : ( 510, 450 ), 'state' : 1, 'color' : 2, 'type' : 0 } , { 'location' : ( 1200, 300 ), 'state' : 1, 'color' : 2, 'type' : 0 },
                { 'location' : ( 400, 300 ), 'state' : 1, 'color' : 3, 'type' : 0 }, { 'location' : ( 1080, 450 ), 'state' : 1, 'color' : 3, 'type' : 0 } ,
                { 'location' : ( 1650, 1665 ), 'state' : 1, 'color' : 2, 'type' : 0 }, { 'location' : ( 1955, 1995 ), 'state' : 1, 'color' : 2, 'type' : 0 },
                { 'location' : ( 1955, 1605 ), 'state' : 1, 'color' : 3, 'type' : 0 }, { 'location' : ( 1650, 1935 ), 'state' : 1, 'color' : 3, 'type' : 0 },
                { 'location' : ( 100, 670 ), 'state' : 1, 'color' : 2, 'type' : 1 }, { 'location' : ( 800, 1100 ), 'state' : 1, 'color' : 2, 'type' : 1 },
                { 'location' : ( 1200, 1730 ), 'state' : 1, 'color' : 2, 'type' : 1 } , { 'location' : ( 400, 2050 ), 'state' : 1, 'color' : 2, 'type' : 1 },
                { 'location' : ( 400, 950 ), 'state' : 1, 'color' : 3, 'type' : 1 }, { 'location' : ( 1200, 1270 ), 'state' : 1, 'color' : 3, 'type' : 1 },
                { 'location' : ( 800, 1900 ), 'state' : 1, 'color' : 3, 'type' : 1 }, { 'location' : ( 100, 2330 ), 'state' : 1, 'color' : 3, 'type' : 1 } ]  

#  change get cup place cup to soecific location
class robotsetting:
    def __init__(self, a):
        self.cupstorage = a
        self.freestorage = a
        # print("debug", self.cupstorage , self.freestorage)
    def cup(self, num):
        # print("debug", self.cupstorage , num)
        self.freestorage = self.freestorage - num
        # print("free storage = ", self.freestorage)

class current_state:
    def __init__(self, name, location, cup_num, NS, windsock, flag, lhouse, time, cost):
        self.name = name
        self.location = location 
        self.cup_num = cup_num
        self.NS = NS
        self.windsock = windsock
        self.flag = flag
        self.lhouse = lhouse
        self.time = time
        self.cost = cost
        self.check = 0
        self.candidate = []
        self.achieved = []
        self.cup_order = []
    def myfunc(self, name):
        print(name, self.cup_num, self.NS, self.windsock, self.flag, self.lhouse, self.time, self.candidate)

class Mission_precondition:
    def __init__(self, name, location, cup_num, NS, windsock, flag, lhouse, time, reward, effect):
        self.name = name
        self.location = location
        self.cup_num = cup_num
        self.NS = NS
        self.windsock = windsock
        self.flag = flag
        self.lhouse = lhouse
        self.time = time
        self.reward = reward
        self.cost = 0
        self.check = 0
        self.effect = effect
    def myfunc(self, name):
        print("mission " + name, self.cup_num, self.NS, self.windsock, self.flag, self.lhouse, self.time)

def checkpreconditions( current, mission, robot):
    for m in mission:
        # print("name", m.name)
        ok = 1
        #check if there are space for cup
        if m.name == 'placecupH' or m.name == 'placecupP':
                # print("name", m.name, robot.freestorage , robot.cupstorage)
            if robot.freestorage >= robot.cupstorage :
                ok = -1
            if current.time < 85:
                if robot.freestorage > 0:
                    ok = -1
    
        if m.name == 'getcup':
            if m.cup_num > (robot.freestorage) and robot.cupstorage != robot.freestorage:
                # print("1",robot.cupstorage ,robot.freestorage)
                ok = -1
        #go home only after time = 98
        if m.name == 'anchorN' or  m.name == 'anchorS':
            if current.NS != m.NS and m.NS != None :
                ok = -1
            else:
                if current.time < 90:
                    ok = -1
            # print("2",current.NS, m.NS)
        #check if anchored -> NS + 10
        if current.NS >= 10:
            if m.name != 'flag':
                ok = -1
            else:
                if current.time < 95:
                    current.time += 1
                # elif current.time >= 100:
                #     current.candidate.append(m)
        if current.windsock != m.windsock and m.windsock != None  and current.windsock != None :
        # if current.windsock != m.windsock :
            ok = -1
            # print("3",current.windsock, m.windsock)
        if m.name == 'flag':
            #raise flag only after time = 95
            if current.time <= 95:
                ok = -1
        if current.flag != m.flag and m.flag != None  and current.flag != None :
            ok = -1
            # print("4")
        if current.lhouse != m.lhouse and m.lhouse != None  and current.lhouse != None :
            ok = -1
            # print("5",current.lhouse, m.lhouse)
        if current.time >= 100:
            ok = -1
            print("time up!")
        
        if ok == 1:
        # print("ok")
            m.check = 1
        elif ok == -1:
            #print("not okay")
            m.check = 0
        
        if m.check == 1:
            # print("mmmm")
            # calculate cost
            if m.name == 'getcup':
                # print("nnn")
                cup = cup_cost(current, m, robot)
                # print("debuggg", cup)
                m.cost = cup['distance']  - m.reward + m.time
                m.location = cup['location']
                # print("cup cost", m.cost)
            
            elif m.name == 'flag':
                # print("debug flag", m.location, m.reward, m.time)
                m.cost = -m.reward + m.time
            elif (m.name == 'palcecupP' or m.name == 'placecupH') and current.time >= 85:
                d = int((abs( current.location[0] - m.location[0] )**2 + abs( current.location[1] - m.location[1])**2)**0.5)
                m.cost = d - m.reward * 100 + m.time
            else:
                # print("debug",m.name, m.location, m.reward, m.time)
                # d = abs( current.location[0] - m.location[0] ) + abs( current.location[1] -  m.location[1])
                d = int((abs( current.location[0] - m.location[0] )**2 + abs( current.location[1] - m.location[1])**2)**0.5)
                m.cost = d - m.reward + m.time
            current.candidate.append(m)
            # print("candidate", m.name)

def cup_cost(current, mission, robot):
    global cup_state 
    # calculate Manhattan distance
    for cup in cup_state:
        # d = abs( current.location[0] - cup['location'][0] ) + abs( current.location[1] - cup['location'][1])
        d = int((abs( current.location[0] - cup['location'][0] )**2 + abs( current.location[1] - cup['location'][1])**2)**0.5)
        global cup_state
        cup['distance'] = d

    def myFunc(e):
        return e['distance']
    cup_state.sort(key=myFunc)

    i = 1
    c = 0
    while i == 1 :
        if cup_state[c]['state'] == 1:
            mission = cup_state[c]
            # print( 'cup debug', cup_state[c])
            i = 0
        else:
            c += 1
    return mission


def refreshstate(current, mission, robot):
    # for i in mission.effect:
        # print("refresh", i)
    if mission.name == "anchorN" or mission.name == "anchorS":
        current.NS += 10
        # print('debugNS', current.NS)
    if mission.name == "getcup":
        global cup_state
        for c in cup_state:
            if mission.location == c['location']:
                c['state'] = 0
                # print("refresh cup state", c)
    if current.cup_num != None and mission.effect[0] != None:
    # if current.cup_num != None and mission.effect[0] != None:
        # print("debug", mission.effect[0], robot.freestorage, robot.cupstorage)
        robot.cup(mission.effect[0])
        current.cup_num += mission.effect[0]
        # print("debug2", mission.effect[0], robot.freestorage, robot.cupstorage)
    # if current.NS != None:
    #     current.NS = mission.effect[1]
    if current.windsock != None:
        current.windsock = mission.effect[2]
    if current.flag != None:
        current.flag = mission.effect[3]
    if current.lhouse != None and mission.effect[4] != None:
        current.lhouse = mission.effect[4]
    if current.time != None:
        if mission.name == 'flag':
            current.time += mission.effect[5]
        else:
            d = abs( current.location[0] - mission.location[0] ) + abs( current.location[1] -  mission.location[1])
            current.time += mission.effect[5] + d / 500 
            print("debuggg", current.time)
        # current.time += mission.cost + mission.reward
    if mission.location != None:
        current.location = mission.location
    # print("refresh", current.cup_num, current.windsock)

#compare cost of missions
def compare_cost( array ):
    def myFunc(e):
        #print(e.cost)
        return e.cost

    array.sort(key=myFunc)
    for c in array:
        print("can_sort", c.name, c.cost)


def evaluate(current, robot):
    score = 0
    red = 0
    green = 0
    cup = 0
    num = int(len(current.cup_order) / 6)
    m = 0
    for m in current.achieved:
        print("name", m.name, score)
        if m.name == 'windsock1' or m.name == 'windsock2':
            score += 15
        elif m.name == 'lhouse':
            score += 10
        elif m.name == 'anchorN' or  m.name == 'anchorS':
            score += 10
        elif  m.name == 'flag':
            score += 10
        elif m.name == 'placecupH' or  m.name == 'placecupP':
            score += 2 * robot.cupstorage
            i = 0
            if m <= num:
                for i in range(0, robot.cupstorage):
                    for c in cup_state:
                        if current.cup_order[ cup ] == c['location']:
                            if c['color'] == 2:
                                green += 1
                            else:
                                red += 1
                            break
                    cup += 1
                m += 1
            else:
                tmp = len(current.cup_order) - num * robot.cupstorage
                for i in range(0, tmp + 1):
                    for c in cup_state:
                        if current.cup_order[ cup ] == c['location']:
                            if c['color'] == 2:
                                green += 1
                            else:
                                red += 1
                            break
                    cup += 1
    
    #calculate how many paired cup
    if red > green:
        score += 2 * green
    else:
        score += 2 * red
    return score


#setting of robot1
current_cup = 0
robot1 = robotsetting(9)
robot1.cup(current_cup)
#print("func", robot1.freestorage)

#setting of current state
#name, location, cup_num, NS, windsock, flag, lhouse, time, cost
cur = current_state( "cur", ( 200, 750 ), 0, 1, 0, 0, 0, 0, 0)
cur.myfunc("current")

#setting of mission precondition 
#name, location, cup_num, NS, windsock, flag, lhouse, time, reward, effect
windsock1 = Mission_precondition( "windsock1", ( 2000, 230 ), None, None, 0, None, None, 2, 15, [None, None, 1, None, None, 2])
windsock1.myfunc("windsock1")

windsock2 = Mission_precondition( "windsock2", ( 2000, 635 ), None, None, 0, None, None, 2, 15, [None, None, 1, None, None, 2])
windsock2.myfunc("windsock2")

lhouse = Mission_precondition( "lhouse", ( 0, 300 ), None, None, None, None, 0, 2, 50,[None, None, None, None, 1, 2])
lhouse.myfunc("lhouse")

#temporay set that it has to be done last
anchorN = Mission_precondition( "anchorN", (300, 200 ), None, 1, 1, None, 1, 2, 10000,[None, None, None, None, None, 2])
anchorN.myfunc("anchorN")
anchorS = Mission_precondition( "anchorS", ( 1300, 200 ), None, 0, 1, None, 1, 2, 10000,[None, None, None, None, None, 2])
anchorS.myfunc("anchorS")

#temporay set that it has to be done after lhouse and windsock
flag = Mission_precondition( "flag", None, None, None, 1, 0, 1, 0, 20000,[None, None, None, 1, None, 1])
flag.myfunc("flag")

getcup = Mission_precondition( "getcup", ( 0, 0 ), 1, None, None, None, None, 2, 60,[1, None, None, None, None, 5])
getcup.myfunc("getcup")

placecupP = Mission_precondition( "placecupP", ( 515, 200 ), -6, None, None, None, None, 5, 40,[-6, None, None, None, None, 1])
placecupP.myfunc("placecupP")

placecupH = Mission_precondition( "placecupH", ( 1850, 1800 ), -6, None, None, None, None, 5, 40,[-6, None, None, None, None, 1])
placecupH.myfunc("placecupH")

leaf = [ windsock1, windsock2, lhouse, anchorN, anchorS, flag, getcup, placecupP, placecupH ]
tmp = 0


while cur.time < 100:
    print ( 'time', cur.time )
    # for i in range (len(leaf)):
    if tmp  == 0:
    #check if current states meet preconditions
        checkpreconditions(cur, leaf, robot1)
        compare_cost(cur.candidate)
        cur.achieved.append(cur.candidate[0])
        if cur.candidate[0].name == 'getcup':
                # print("mmmm")
                cur.cup_order.append(cur.candidate[0].location)
        refreshstate(cur, cur.candidate[0], robot1)
        tmp = tmp + 1
    else:
        for i in cur.achieved:
            if i in leaf:
                if i.name != "getcup" and i.name != "placecupP" and i.name != "placecupH":
                    # print("e", i.name)
                    leaf.remove(i)
        # for y in leaf:
            # print("leaf", y.name)
        
        checkpreconditions(cur, leaf, robot1)
            
        if len(cur.candidate) > 0:
            compare_cost(cur.candidate)
            # print("aa", cur.candidate[0].name)
            cur.achieved.append(cur.candidate[0])
            if cur.candidate[0].name == 'getcup':
                # print("mmmm")qewewqww2e
                cur.cup_order.append(cur.candidate[0].location)
            refreshstate(cur, cur.candidate[0], robot1)
        else:
            cur.time += 1
            print("no candidate")
            # break

    del cur.candidate[:]
cur.achieved.append(flag)
temp = 0
for a in cur.achieved:
    if a.name == 'getcup':
        # print("debug",len(cur.cup_order))
        print("achieved", a.name, cur.cup_order[temp])
        # print("achieved", a.name)
        temp = temp + 1
    else:
        print("achieved", a.name, a.location)

score = evaluate(cur, robot1)
print("score", score)

