class robotsetting:
    def __init__(self, a):
        self.cupstorage = a
        self.freestorage = a
        # print("debug", self.cupstorage , self.freestorage)
    def cup(self, num):
        # print("debug", self.cupstorage , num)
        self.freestorage = self.cupstorage - num
        # print("free storage = ", self.freestorage)

class current_state:
    def __init__(self, name, cup_num, NS, windsock, flag, lhouse, time, cost):
        self.name = name
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
    def myfunc(self, name):
        print(name, self.cup_num, self.NS, self.windsock, self.flag, self.lhouse, self.time, self.candidate)

class Mission_precondition:
    def __init__(self, name, cup_num, NS, windsock, flag, lhouse, time, cost, effect):
        self.name = name
        self.cup_num = cup_num
        self.NS = NS
        self.windsock = windsock
        self.flag = flag
        self.lhouse = lhouse
        self.time = time
        self.cost = cost
        self.check = 0
        self.effect = effect
    def myfunc(self, name):
        print("mission " + name, self.cup_num, self.NS, self.windsock, self.flag, self.lhouse, self.time)

def checkpreconditions( current, mis, robot):
    for m in mis:
        print("name", m.name)
        ok = 1
        #check if there are spce for cup
        if m.cup_num != None:
            if m.name == 'placecup':
                # print("name", m.name, robot.freestorage , robot.cupstorage)
                if robot.freestorage == robot.cupstorage :
                    ok = -1
                    print("gg")
            if m.cup_num > (robot.cupstorage - robot.freestorage) and robot.cupstorage != robot.freestorage:
                print("1",robot.cupstorage ,robot.freestorage)
                ok = -1
            
        if current.NS != m.NS and m.NS != None :
            ok = -1
            print("2",current.NS, m.NS)
        if current.windsock != m.windsock and m.windsock != None  and current.windsock != None :
        # if current.windsock != m.windsock :
            ok = -1
            print("3",current.windsock, m.windsock)
        if current.flag != m.flag and m.flag != None  and current.flag != None :
            ok = -1
            print("4")
        if current.lhouse != m.lhouse and m.lhouse != None  and current.lhouse != None :
            ok = -1
            print("5",current.lhouse, m.lhouse)
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
            current.candidate.append(m)
            # print("candidate", m.name)

def refreshstate(current, mission, robot):
    # for i in mission.effect:
        # print("refresh", i)
    if current.cup_num != None and mission.effect[0] != None:
        robot.cup(mission.effect[0])
        current.cup_num += mission.effect[0]
    # if current.NS != None:
    #     current.NS = mission.effect[1]
    if current.windsock != None:
        current.windsock = mission.effect[2]
    if current.flag != None:
        current.flag = mission.effect[3]
    if current.lhouse != None and mission.effect[4] != None:
        current.lhouse = mission.effect[4]
    if current.time != None:
        current.time += mission.effect[5]
    # print("refresh", current.cup_num, current.windsock)

#compare cost of missions
def compare_cost( array ):
    def myFunc(e):
        #print(e.cost)
        return e.cost

    array.sort(key=myFunc)
    for c in array:
        print("can_sort", c.name, c.cost)

mission = 7

#setting of robot1
current_cup = 0
robot1 = robotsetting(6)
robot1.cup(current_cup)
#print("func", robot1.freestorage)

#setting of current state
#name, cup_num, NS, windsock, flag, lhouse, time, cost
cur = current_state( "cur", 0, 1, 0, 0, 0, 0, 0)
cur.myfunc("current")

#setting of mission precondition 
#name, cup_num, NS, windsock, flag, lhouse, time, cost, effect
windsock = Mission_precondition( "windsock", None, None, 0, None, None, 2, 30, [None, None, 1, None, None, 2])
windsock.myfunc("windsock")

lhouse = Mission_precondition( "lhouse", None, None, None, None, 0, 2, 100,[None, None, None, None, 1, 2])
lhouse.myfunc("lhouse")

#temporay set that it has to be done last
anchorN = Mission_precondition( "anchorN", None, 1, 1, None, 1, 2, 10,[None, None, None, None, None, 2])
anchorN.myfunc("anchorN")
anchorS = Mission_precondition( "anchorS", None, 0, 1, None, 1, 2, 10,[None, None, None, None, None, 2])
anchorS.myfunc("anchorS")

#temporay set that it has to be done after lhouse and windsock
flag = Mission_precondition( "flag", None, None, 1, 0, 1, 1, 100,[None, None, None, 1, None, 1])
flag.myfunc("flag")

getcup = Mission_precondition( "getcup", 1, None, None, None, None, 5, 20,[1, None, None, None, None, 5])
getcup.myfunc("getcup")

placecup = Mission_precondition( "placecup", -1, None, None, None, None, 1, 10,[-1, None, None, None, None, 1])
placecup.myfunc("placecup")

leaf = [windsock, lhouse, anchorN, anchorS, flag, getcup, placecup]
for i in range (mission):
    if i  == 0:
    #check if current states meet preconditions
        checkpreconditions(cur, leaf, robot1)
        compare_cost(cur.candidate)
        cur.achieved.append(cur.candidate[0])
        refreshstate(cur, cur.candidate[0], robot1)
    else:
        for i in cur.achieved:
            # print("e", i.name)
            if i in leaf:
                leaf.remove(i)
        # for y in leaf:
            # print("leaf", y.name)
          
        checkpreconditions(cur, leaf, robot1)
               
        if len(cur.candidate) != 0:
            compare_cost(cur.candidate)
            print("aa", cur.candidate[0].name)
            cur.achieved.append(cur.candidate[0])
            refreshstate(cur, cur.candidate[0], robot1)

    #cur.candidate.clear()
    del cur.candidate[:]
   
        

for a in cur.achieved:
    print("achieved", a.name)