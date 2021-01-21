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
    def __init__(self, a, b):
        self.cupstorage = a
        self.freestorage = a
        self.reef = b
        # print("debug", self.cupstorage , self.freestorage)
    def cup(self, num):
        # print("debug", self.cupstorage , num)
        self.freestorage = self.freestorage - num
        # print("free storage = ", self.freestorage)

class current_state:
    def __init__(self, name, location, NS, reef_p, reef_l, reef_r, windsock, flag, lhouse, time):
        self.name = name
        self.location = location 
        self.NS = NS
        self.reef_p = reef_p
        self.reef_l = reef_l
        self.reef_r = reef_r
        self.windsock = windsock
        self.flag = flag
        self.lhouse = lhouse
        self.time = time
        self.placecup_reef = 0
        self.check = 0
        self.candidate = []
        self.achieved = []
        self.cup_order = []
    def myfunc(self, name):
        print(name, self.NS, self.windsock, self.flag, self.lhouse, self.time, self.candidate)

class Mission_precondition:
    def __init__(self, name, location, NS, reef_p, reef_l, reef_r, windsock, flag, lhouse, time, reward, effect):
        self.name = name
        self.location = location
        self.NS = NS
        self.reef_p = reef_p
        self.reef_l = reef_l
        self.reef_r = reef_r
        self.windsock = windsock
        self.flag = flag
        self.lhouse = lhouse
        self.time = time
        self.reward = reward
        self.cost = 0
        self.check = 0
        self.cup = None
        self.effect = effect
    def myfunc(self, name):
        print("mission " + name, self.NS, self.windsock, self.flag, self.lhouse, self.time)

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
                if current.time < 70:
                    m.cost = distance( current.location, m.location ) - m.reward * ( robot.cupstorage - robot.freestorage - 12 ) + m.time
                else:
                    m.cost = distance( current.location, m.location ) - m.reward * (100 * ( robot.cupstorage - robot.freestorage ))**5 + m.time
                current.candidate.append(m)
        elif m.name == 'windsock':
            if current.windsock != 1:
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
        elif m.name == 'reef_rivate':
            if robot1.reef == 1 and current.reef_p == 1:
                m.cost = distance( current.location, m.location ) - m.reward + m.time
                current.candidate.append(m)
        elif m.name == 'reef_left':
            if robot1.reef == 1 and current.reef_l == 1:
                m.cost = distance( current.location, m.location ) - m.reward + m.time
                current.candidate.append(m)
        elif m.name == 'reef_right':
            if robot1.reef == 1 and current.reef_r == 1:
                m.cost = distance( current.location, m.location ) - m.reward + m.time
                current.candidate.append(m)
        elif m.name == 'placecup_reef':
            if current.placecup_reef == 1:
                m.cost = distance( current.location, m.location ) - m.reward + m.time
                current.candidate.append(m)
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
    # if current.cup_num != None and mission.effect[0] != None:
    #     robot.cup(mission.effect[0])
    #     current.cup_num += mission.effect[0]
    if mission.name == "getcup":
        global cup_state
        robot.cup(1)
        current.cup_order.append(mission.cup)
        for c in cup_state:
            if mission.location == c['location']:
                c['state'] = 0

    elif mission.name == 'placecupH' or mission.name == 'placecupP':
        robot.cup(-12)

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
        # d = abs( current.location[0] - mission.location[0] ) + abs( current.location[1] -  mission.location[1])
        # if mission.effect[5] == None:
        #      current.time += d / 500
        # else:
        current.time += mission.time + d / 500 
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
        elif m.name == 'placecupH' or  m.name == 'placecupP':
            score += 2 * robot1.cupstorage
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


#setting of robot1 cup capacity and if can pick cup from reef
current_cup = 0
robot1 = robotsetting(12, 0)
# robot1 = robotsetting(5, 1)
robot1.cup(current_cup)
#print("func", robot1.freestorage)

#setting of current state
#name, location, NS, reef_p, reef_l, reef_r, windsock, flag, lhouse, time):
cur = current_state( "cur", ( 800, 200 ), 0, 1, 1, 1, 0, 0, 0, 0)
cur.myfunc("current")
#setting of mission precondition 
#name, location, NS, reefp, reefr, reefl, windsock, flag, lhouse, time, reward, effect[reefp, reefr, reefl, windsock, flag, lhouse]
windsock = Mission_precondition( "windsock", ( 2000, 430 ), None, None, None, None, 0, None, None, 2, 80, [None, None, None, 1, None, None, None, 2])
windsock.myfunc("windsock")

lhouse = Mission_precondition( "lhouse", ( 0, 300 ), None, None, None, None, None, None, 0, 2, 50,[None, None, None, None, None, 1])
lhouse.myfunc("lhouse")

getcup = Mission_precondition( "getcup", ( 0, 0 ), None, None, None, None, None, None, None, 2, 20,[None, None, None, None, None, None])
getcup.myfunc("getcup")

#reef cup counts separately
reef_private = Mission_precondition( "reef_private", ( 1600, 0 ), None, None, 1, None, None, None, None, 9, 100,[0, None, None, None, None, None])
reef_private.myfunc("reef_private")

reef_left = Mission_precondition( "reef_left", ( 0, 850 ), None, None, None, 1, None, None, None, 9, 200,[None, None, 0, None, None, None])
reef_left.myfunc("reef_left")

reef_right = Mission_precondition( "reef_right", ( 0, 2150 ), None, None, None, 1, None, None, None, 9, 200,[None, 0, None, None, None, None])
reef_right.myfunc("reef_right")

placecup_reef = Mission_precondition( "placecup_reef", ( 800, 200 ), None, None, None, None, None, None, None, 5, 10000,[None, None, None, None, None, None])
placecup_reef.myfunc("placecup_reef")

placecupP = Mission_precondition( "placecupP", ( 515, 200 ), None, None, None, None, None, None, None, 5, 40,[None, None, None, None, None, None])
placecupP.myfunc("placecupP")

placecupH = Mission_precondition( "placecupH", ( 1850, 1800 ), None, None, None, None, None, None, None, 5, 40,[None, None, None, None, None, None])
placecupH.myfunc("placecupH")
#temporay set that it has to be done last
anchorN = Mission_precondition( "anchorN", (300, 200 ), None, None, None, None, None, None, None, 2, 10000,[None, None, None, None, None, None])
anchorN.myfunc("anchorN")
anchorS = Mission_precondition( "anchorS", ( 1300, 200 ), None, None, None, None, None, None, None, 2, 10000,[None, None, None, None, None, None])
anchorS.myfunc("anchorS")

#temporay set that it has to be done after lhouse and windsock
flag = Mission_precondition( "flag", None, None, None, None, 1, 1, 0, 1, 0, 20000,[None, None, None, 1, None, 1])
flag.myfunc("flag")  

leaf = [ anchorN, anchorS, flag, windsock, lhouse, getcup, reef_private, reef_left, reef_right, placecupP, placecupH, placecup_reef ]
tmp = 0
mission = len(leaf)
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
        # print("debug",len(cur.cup_order))
        print("achieved", a.name, cur.cup_order[temp])
        # print("achieved", a.name)
        c = (a.name, (cur.cup_order[temp]['location']))
        mission_list.append(c)
        temp = temp + 1
    else:
        print("achieved", a.name, a.location)
        c = (a.name, a.location)
        mission_list.append(c)

score = evaluate(cur, robot1)
print("score", score)
# for p in mission_list:
#     print("mission_list", p)
