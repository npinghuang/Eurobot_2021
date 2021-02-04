#set mission state here
class current_setting:
    def __init__(self, mission, mission_pos, planner_state, pos, cup_no):
        self.mission = mission_pos
        self.mission_name = 'initialize'
        self.mission_pos = mission_pos
        self.planner = planner_state
        self.pos = pos
        self.cup_no = cup_no
    def myfunc(self):
        print("current", self.mission, self.planner, self.cup_no)
class robot1:
    def __init__(self):
        self.claw = [0, 0, 0, 0] # 0 1 for red 2 3 for green
        self.suction = [0, 0, 0, 0, 0, 0, 0, 0] # 0 ~ 3 for red 4 ~ 7 for green
        self.flag = 0
        self.storage_red = 0
        self.storage_red = 0
robot1 = robot1()
print("robot", robot1.claw[0])
class getcup_setting:
    def __init__(self):
        self.action_list = [ 1, 2, 3, 4, 5, 6]
        self.cup_state =1 
        self.count = 0 #record how many action had been done

class placecup_setting:
    def __init__(self):
        self.action_list = [ 1, 2, 3, 4, 5, 6]
        self.count = 0 #record how many action had been done

def refreshmission():
    getcupp = getcup_setting()
    print("refresh")
    return getcupp

def getmissionname( no ):
    name = ''
    print("no", no)
    if no == 0:
        name = 'emergency'
        print("check", name)
    elif no == 1:
        name = 'windsock'
    elif no == 2:
        name = 'lhouse'
    elif no == 3:
        name = 'flag'
    elif no == 4:
        name = 'anchorN'
    elif no == 5:
        name = 'anchorS'
    elif no == 6:
        name = 'reef_left'
    elif no == 7:
        name = 'reef_right'
    elif no == 8:
        name = 'reef_private'
    elif no == 9:
        name = 'placecupH'
    elif no == 10:
        name = 'placecupP'
    elif no == 11:
        name = 'placecupR'
    elif no == 12:
        name = 'getcup'
    elif no == 13:
        name = 'getcup_12'
    elif no == 14:
        name = 'getcup_34'
    return name