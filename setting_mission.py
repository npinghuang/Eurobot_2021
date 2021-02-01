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

def getmissionname( current ):
    if current.mission == 0:
        current.mission_name = 'emergency'
    elif current.mission == 1:
        current.mission_name = 'windsock'
    elif current.mission == 2:
        current.mission_name = 'lhouse'
    elif current.mission == 3:
        current.mission_name = 'flag'
    elif current.mission == 4:
        current.mission_name = 'anchorN'
    elif current.mission == 5:
        current.mission_name = 'anchorS'
    elif current.mission == 6:
        current.mission_name = 'reef_left'
    elif current.mission == 7:
        current.mission_name = 'reef_right'
    elif current.mission == 8:
        current.mission_name = 'reef_private'
    elif current.mission == 9:
        current.mission_name = 'placecupH'
    elif current.mission == 10:
        current.mission_name = 'placecupP'
    elif current.mission == 11:
        current.mission_name = 'placecupR'
    elif current.mission == 12:
        current.mission_name = 'getcup'