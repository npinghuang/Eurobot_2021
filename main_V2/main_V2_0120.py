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
    def __init__(self, name, location, cup_num, NS, windsock1, windsock2, flag, lhouse, time, cost):
        self.name = name
        self.location = location 
        self.cup_num = cup_num
        self.NS = NS
        self.windsock1 = windsock1
        self.windsock2 = windsock2
        self.flag = flag
        self.lhouse = lhouse
        self.time = time
        self.cost = cost
        self.check = 0
        self.candidate = []
        self.achieved = []
        self.cup_order = []
    def myfunc(self, name):
        print(name, self.cup_num, self.NS, self.windsock1, self.flag, self.lhouse, self.time, self.candidate)

class Mission_precondition:
    def __init__(self, name, location, cup_num, NS, windsock1, windsock2, flag, lhouse, time, reward, effect):
        self.name = name
        self.location = location
        self.cup_num = cup_num
        self.NS = NS
        self.windsock1 = windsock1
        self.windsock2 = windsock2
        self.flag = flag
        self.lhouse = lhouse
        self.time = time
        self.reward = reward
        self.cost = 0
        self.check = 0
        self.cup = None
        self.effect = effect
    def myfunc(self, name):
        print("mission " + name, self.cup_num, self.NS, self.windsock1, self.flag, self.lhouse, self.time)

def checkpreconditions( current, mis, robot):
    for m in mis:
        if m.name == 'getcup':
            if robot.freestorage > 0 and current.time < 90:
                cup = cup_cost( current, m, robot )
                if cup != None:
                # m.cost = cup[ 'distance' ] - m.reward + m.time
                    # print("dddcup", cup[ 'location' ])
                    m.cost = distance( current.location, cup[ 'location' ] )- m.reward + m.time
                    m.location = cup[ 'location' ]
                    m.cup = cup
                    # print("cupdebug", m.cup)
                    current.candidate.append(m)
        elif m.name == 'placecupP' or m.name == 'placecupH':
            if robot.freestorage < robot.cupstorage:
                if current.time < 92:
                    m.cost = distance( current.location, m.location ) - m.reward * ( robot.cupstorage - robot.freestorage - 12 ) + m.time
                else:
                    m.cost = distance( current.location, m.location ) - m.reward * (100 * ( robot.cupstorage - robot.freestorage ))**5 + m.time
                current.candidate.append(m)
        elif m.name == 'windsock1':
            if current.windsock1 != 1:
                m.cost = distance( current.location, m.location ) - m.reward + m.time
                current.candidate.append(m)
        elif m.name == 'windsock2':
            if current.windsock2 != 1:
                m.cost = distance( current.location, m.location ) - m.reward + m.time
                current.candidate.append(m)
        elif m.name == 'lhouse':
            if current.lhouse != 1:
                m.cost = distance( current.location, m.location ) - m.reward + m.time
                current.candidate.append(m)
        elif m.name == 'flag':
            if current.lhouse != 1 and current.time >= 95:
                m.cost = distance( current.location, m.location ) - m.reward + m.time
                current.candidate.append(m)
        elif m.name == 'anchorN' or m.name == 'anchorS':
            if current.NS == m.NS and current.time > 97:
                m.cost = distance( current.location, m.location ) - m.reward + m.time
                current.candidate.append(m)
            # print("candidate", m.name)
def cup_cost(current, mission, robot):
    global cup_state 
    # calculate Manhattan distance
    for cup in cup_state:
        # d = abs( current.location[0] - cup['location'][0] ) + abs( current.location[1] - cup['location'][1])
        d = distance( current.location, cup[ 'location' ])
        # d = int((abs( current.location[0] - cup['location'][0] )**2 + abs( current.location[1] - cup['location'][1])**2)**0.5)
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
        elif c >= len(cup_state) - 1:
            mission = None
            i = 0
        else:
            c += 1
    return mission
def refreshstate(current, mission, robot):
    # for i in mission.effect:
        # print("refresh", i)
    if current.cup_num != None and mission.effect[0] != None:
        robot.cup(mission.effect[0])
        current.cup_num += mission.effect[0]
    if mission.name == "getcup":
        global cup_state
        current.cup_order.append(mission.cup)
        for c in cup_state:
            if mission.location == c['location']:
                c['state'] = 0
    # if current.NS != None:
    #     current.NS = mission.effect[1]
    if mission.effect[2] != None:
        # print("de", current.windsock1, mission.effect[2])
        current.windsock1 = mission.effect[2]
    if mission.effect[3] != None:
        # print("bug", current.windsock2, mission.effect[3])
        current.windsock2 = mission.effect[3]
    if mission.effect[4] != None:
        current.flag = mission.effect[4]
    if mission.effect[5] != None:
        current.lhouse = mission.effect[5]
        
    # if mission.effect[5] != None:
    if mission.name == 'flag':
        current.time += mission.effect[5]
    else:
        d = distance( current.location, mission.location )
        # d = abs( current.location[0] - mission.location[0] ) + abs( current.location[1] -  mission.location[1])
        if mission.effect[5] == None:
             current.time += d / 500
        else:
            current.time += mission.effect[5] + d / 500 
        # print("debuggg", current.time)
    # print("refresh", current.cup_num, current.windsock)
    if mission.location != None:
        current.location = mission.location
    
#compare cost of missions
def compare_cost( array ):
    def myFunc(e):
        #print(e.cost)
        return e.cost

    array.sort(key=myFunc)
    # for c in array:
        # print("can_sort", c.name, c.cost)

def distance(a, b):
    d = int((abs( a[0] - b[0] )**2 + abs( a[1] - b[1])**2)**0.5)
    return d

def evaluate(current, robot):
    score = 0
    red = 0
    green = 0
    cup = 0
    num = int(len(current.cup_order) / 6)
    m = 0
    for m in current.achieved:
        # print("name", m.name, score)
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
            # for c in cup_state:
            #     if current.cup_order[ cup ] == c['location']:
            #         if c['color'] == 2:
            #             green += 1
            #         else:
            #             red += 1
            #         break
            # cup += 1
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
mission = 10 - 3

#setting of robot1
current_cup = 0
robot1 = robotsetting(12)
robot1.cup(current_cup)
#print("func", robot1.freestorage)

#setting of current state
#name, location, cup_num, NS, windsock1, windsock2, flag, lhouse, time, cost
cur = current_state( "cur", ( 200, 750 ), 0, 1, 0, 0, 0, 0, 0, 0)
cur.myfunc("current")
#setting of mission precondition 
#name, location, cup_num, NS, windsock1, windsock2, flag, lhouse, time, reward, effect
windsock1 = Mission_precondition( "windsock1", ( 2000, 230 ), None, None, 0, None, None, None, 2, 15, [None, None, 1, None, None, None, 2])
windsock1.myfunc("windsock1")

windsock2 = Mission_precondition( "windsock2", ( 2000, 635 ), None, None, None, 0, None, None, 2, 15, [None, None, None, 1, None, None, 2])
windsock2.myfunc("windsock2")

lhouse = Mission_precondition( "lhouse", ( 0, 300 ), None, None, None, None, None, 0, 2, 50,[None, None, None, None, None, 1, 2])
lhouse.myfunc("lhouse")



getcup = Mission_precondition( "getcup", ( 0, 0 ), 1, None, None, None, None, None, 90, 60,[1, None, None, None, None, None, 5])
getcup.myfunc("getcup")

placecupP = Mission_precondition( "placecupP", ( 515, 200 ), -12, None, None, None, None, None, 5, 40,[-12, None, None, None, None, None, 1])
placecupP.myfunc("placecupP")

placecupH = Mission_precondition( "placecupH", ( 1850, 1800 ), -12, None, None, None, None, None, 5, 40,[-12, None, None, None, None, None, 1])
placecupH.myfunc("placecupH")
#temporay set that it has to be done last
anchorN = Mission_precondition( "anchorN", (300, 200 ), None, 1, 1, 1, None, 1, 2, 10000,[None, None, None, None, None, 2])
anchorN.myfunc("anchorN")
anchorS = Mission_precondition( "anchorS", ( 1300, 200 ), None, 0, 1, 1, None, 1, 2, 10000,[None, None, None, None, None, 2])
anchorS.myfunc("anchorS")

#temporay set that it has to be done after lhouse and windsock
flag = Mission_precondition( "flag", None, None, None, 1, 1, 0, 1, 0, 20000,[None, None, None, 1, None, 1])
flag.myfunc("flag")  

leaf = [ anchorN, anchorS, flag, windsock1, windsock2, lhouse, getcup, placecupP, placecupH ]
tmp = 0
while cur.time < 95:
    if tmp  == 0:
    #check if current states meet preconditions
        checkpreconditions(cur, leaf, robot1)
        compare_cost(cur.candidate)
        cur.achieved.append(cur.candidate[0])
        refreshstate(cur, cur.candidate[0], robot1)
        tmp = tmp + 1
    else:
        # for i in cur.achieved:
        #     # print("e", i.name)
        #     if i in leaf and i != 'getcup':
        #         leaf.remove(i)
        # for y in leaf:
            # print("leaf", y.name)
          
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