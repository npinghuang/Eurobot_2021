#!/usr/bin/env python
#coding=utf-8
from setting_mission import *
from action_mission import *
#for future convience
current = current_setting( 0, [0,0,0], 0, [0,0,0], 0 )
#information i will get from main
current.mission = int(input("mission name:"))
# current.mission_pos[0] = input("mission pos x:")
# current.mission_pos[1] = input("mission pos y:")
# current.mission_pos[2] = input("mission pos theta:")
# current.cup_no = input("mission cup no:")
# current.planner = input("planner state 1 for at pos 0 for failed 2 for going:")
# current.pos[0] = input("pos x:")
# current.pos[1] = input("pos y:")
# current.pos[2] = input("pos theta:") 

current.myfunc()

current.mission_name = getmissionname(current.mission)
print("mission name", current.mission_name)

if current.mission_name == 'getcup':
    getcup()