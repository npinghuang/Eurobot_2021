#!/usr/bin/env python
#coding=utf-8
import math
import rospy
from goap_2021.srv import *
from setting_mission import *
from action_mission import *
#for future convience
global current
current = current_setting( 0, [0,0,0], 0, [0,0,0], 0 )
#information i will get from main
# current.mission = int(input("mission name:"))
# current.mission_pos[0] = input("mission pos x:")
# current.mission_pos[1] = input("mission pos y:")
# current.mission_pos[2] = input("mission pos theta:")
# current.cup_no = input("mission cup nob:")
# current.planner = input("planner state 1 for at pos 0 for failed 2 for going:")
# current.pos[0] = input("pos x:")
# current.pos[1] = input("pos y:")
# current.pos[2] = input("pos theta:") 

current.myfunc()
current.mission = 12
current.mission_name = getmissionname(current.mission)
# print("mission name", current.mission_name)

global time
time = 0
global getcup 
getcup = refreshmission()
global placecup
placecup = placecup_setting()
def trytry(current):
    if current.mission != 0:
        print("yeah~")
trytry(current)
print("---------------------------------------------")


def mission(req):
    print("req", req.action[0])
    state = 111
    global time
    # time += 1
    print("check mission", time)
    if time == 0:
        global getcup 
        getcup = refreshmission()
        time += 1
        print("class getcup", getcup.action_list [0])
    current.mission = req.action[0]
    current.mission_name = getmissionname(current.mission)
    print("current mission", current.mission_name)
    if getcup.cup_state == 1:
        getcup = refreshmission()
    if current.mission_name == 'getcup':
        print("class getcup2", getcup.cup_state)
        getcup.cup_state = getcup_action(getcup)
    elif current.mission_name == 'placecupH':
        global placecup
        placecup_action(placecup)
    print("---------------------------------------------")
    return state

def mission_big_server():
    rospy.init_node('mission_big_server')
    s = rospy.Service('mission_big', mission_srv, mission)
    rospy.spin()         

if __name__ == "__main__":
    mission_big_server()