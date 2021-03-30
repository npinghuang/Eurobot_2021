#!/usr/bin/env python
#coding=utf-8
import math
import rospy
from goap_2021.srv import *
from precondition_little import *
from setting_little_goap import *
from goap_little_server import *

def GOAP_script(req):
    global penalty_mission
    global counter
    global action
    global position
    global cup
    global counter_scripts
    global previous_team
    # del action[:]
    # del position[:]
    # del cup[:]
    # reset
    print("len action", len(action))
    # if len(action) == 0 + 1 or (req.team != 2 and req.team != previous_team):
    #     counter_scripts = 0
    #     del action[:]
    #     del position[:]
    #     del cup[:]

    if req.emergency == True:
        # print("debug action [0]", action[0])#delete this !!!
        action.insert( 0,0)
        position.insert( 0,req.my_pos[0])
        position.insert( 0, req.my_pos[1])
        position.insert( 0,req.my_pos[2] )
        cup.insert( 0, 0)
        cup.insert( 0,0)
        cup.insert( 0,0)
        return action, position, cup
    if len(action) == 0 + 1 or (req.team != 2 and req.team != previous_team):
        # counter_scripts = 0
        action.append(0)
        position.append(req.my_pos[0])
        position.append(req.my_pos[1])
        position.append(req.my_pos[2])
        cup.append(0)
        cup.append(0)
        cup.append(0)
    
    if req.emergency == False and counter_scripts == 0: #blue team script
        
        (current, robot1) = mission_precondition(req)     
        if req.team == 0:
            if req.ns == False:
                scrpit_mission =[404]
            elif req.ns == True:
                scrpit_mission = [404]
            position_script = [404,404,404]
            # cup_script = [0, 21, 0, 34, 0, 0, 0, 0, 0, 0, 5, 5, 6, 9, 9, 6, 10, 7, 15, 11, 16, 10, 19, 12, 20, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        #('action', 13, 'getcup_12', 1085, 400, 0, 2, 4, 'hand', 2, 1)
            # position_script = [1085.0, 400.0, 0.0, 500.0, 400.0, 0.0, 150.0, 275.0, 3.1415927410125732, 
            # 100.0, 275.0, 3.1415927410125732, 150.0, 275.0, 3.1415927410125732, 
            # 52.191062927246094, 636.3331909179688, 1.9634953737258911, 293.43145751953125, 906.5025024414062, -0.7853981852531433, 
            # 693.4314575195312, 1050.5025634765625, -0.7853981852531433, 1093.431396484375, 1220.5025634765625, -2.356194496154785, 
            # 1093.431396484375, 1680.5025634765625, -0.7853981852531433, 693.4314575195312, 1850.5025634765625, -0.7853981852531433, 
            # 293.43145751953125, 1994.5025634765625, -0.7853981852531433, 62.56562805175781, 2326.696533203125, -0.39269909262657166, 
            # 1900.0, 1800.0, 0.0, 1870.0, 1800.0, 0.0, 1650.0, 1800.0, 0.0, 1900.0, 1800.0, 3.1415927410125732, 1800.0, 1800.0, 3.1415927410125732, 
            # 1770.0, 1800.0, 3.1415927410125732, 1650.0, 1800.0, 3.1415927410125732, 300.0, 200.0, 0.0, 300.0, 200.0, 0.0]
        elif req.team == 1:
            # cup_script = [0, 21, 0, 34, 0, 0, 0, 0, 0, 0, 20, 7, 19, 5, 16, 8, 15, 6, 10, 9, 9, 11, 6, 10, 5, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            # position_script = [ 800.0, 2700.0, 0.0, 300.0, 2775.0, 0.0, ]
            if req.ns == False:
                scrpit_mission =[7,26,27,11,30,4]
                position_script = [ 80, 2150, math.pi, 50, 2150, math.pi,  80, 2150, math.pi, 950,2500,0.0, 450,2500,0.0,300.0, 2500.0, 0.0]
            elif req.ns == True:
                scrpit_mission =[7,26,27,11,30,5]
                position_script = [ 80, 2150, math.pi, 50, 2150, math.pi,  80, 2150, math.pi, 450,2500,math.pi, 950,2500,math.pi,1300.0, 2500.0, math.pi ]
# action: [13, 14, 2, 16, 17, 12, 12, 12, 12, 12, 12, 12, 12, 9, 18, 19, 20, 21, 22, 23, 1, 15]
# position: [1085.0, 2600.0, 0.0, 500.0, 2600.0, 0.0, 100.0, 2725.0, 3.1415927410125732, 50.0, 2725.0, 3.1415927410125732, 100.0, 2725.0, 3.1415927410125732, 95.84193420410156, 2394.103759765625, 0.0, 243.43145751953125, 1994.5025634765625, -0.7853981852531433, 643.4314575195312, 1850.5025634765625, -2.356194496154785, 1043.431396484375, 1680.5025634765625, -0.7853981852531433, 1043.431396484375, 1220.5025634765625, -0.7853981852531433, 643.4314575195312, 1050.5025634765625, -0.7853981852531433, 243.43145751953125, 906.5025024414062, -0.7853981852531433, 81.69979858398438, 712.8905029296875, 1.1780972480773926, 1850.0, 1200.0, 0.0, 1870.0, 1200.0, 0.0, 1650.0, 1200.0, 0.0, 1900.0, 1200.0, 3.1415927410125732, 1800.0, 1200.0, 3.1415927410125732, 1770.0, 1200.0, 3.1415927410125732, 1650.0, 1200.0, 3.1415927410125732, 1850.0, 2800.0, 1.5707963705062866, 1850.0, 2300.0, 1.5707963705062866]
# cup: [0, 21, 0, 34, 0, 0, 0, 0, 0, 0, 20, 7, 19, 5, 16, 8, 15, 6, 10, 9, 9, 11, 6, 10, 5, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] 
        count_script = 0
        count_cup = 0
        while count_script < len( scrpit_mission):
            # if scrpit_mission[count_script] > 14:
            action.append(scrpit_mission[count_script])
            position.append(position_script[ 3* count_script])
            position.append(position_script[ 3* count_script + 1])
            position.append(position_script[ 3* count_script + 2])
            cup.append(0)
            cup.append(0)
            cup.append(0)
            # else:
            #     for m in current.leaf:
            #         if m.name == scrpit_mission[ count_script ] or m.no == scrpit_mission[ count_script ]:
            #             action.append(m.no)
            #             position.append(m.location[0])
            #             position.append(m.location[1])
            #             position.append(m.location[2])
            #             cup.append(cup_script[ 2* count_script])
            #             cup.append(cup_script[ 2* count_script + 1])
            count_script += 1 #for appending next action
    #pop old action
    if counter_scripts > 0 and req.emergency == False:
        action.pop(0)
        position.pop(0)
        position.pop(0)
        position.pop(0)
        cup.pop(0)
        cup.pop(0)
        cup.pop(0)
    
    counter_scripts += 1
    previous_team = req.team
    for a in range(0, len(action)):
        print( a, "mission", action[a], "position", position[3*a], position[3*a + 1], position[3*a + 2], "cup", cup[ 3* a], cup[ 3* a + 1],  cup[ 3* a + 2])
    return action, position, cup