#!/usr/bin/env python
#coding=utf-8
# for 0418 demo
import math
import rospy
from main2021.srv import *
from precondition import *
from setting_big_goap import *
from goap_big_server import *
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
    if len(action) == 0 + 1 or (req.team != 2 and req.team != previous_team) and req.time < 95:
        # counter_scripts = 0
        action.append(0)
        position.append(req.my_pos[0])
        position.append(req.my_pos[1])
        position.append(req.my_pos[2])
        cup.append(0)
        cup.append(0)
        cup.append(0)
    elif len(action) == 0 + 1 or (req.team != 2 and req.team != previous_team) and req.time >= 95:
        # counter_scripts = 0
        action.append(3)
        position.append(req.my_pos[0])
        position.append(req.my_pos[1])
        position.append(req.my_pos[2])
        cup.append(0)
        cup.append(0)
        cup.append(0)

    # if req.emergency == True:
    #     # print("debug action [0]", action[0])#delete this !!!
    #     action.insert( 0,0)
    #     position.insert( 0,req.my_pos[0])
    #     position.insert( 0, req.my_pos[1])
    #     position.insert( 0,req.my_pos[2] )
    #     cup.insert( 0, 0)
    #     cup.insert( 0,0)
        # return action, position, cup
    if req.emergency == False and counter_scripts == 0: #blue team script
        (current, robot1) = mission_precondition(req)    
        scrpit_mission =[38, 39, 14, 12,12,12,12,##getcup12,12,12,12,12,
        21,22,23] #placecup21,22,19,20,
        cup_script = [# 0,0,0,
        # 0, 21, 5, # cup_no, hand_no, cup_color
        0,0,0,
        0,0,0,
        # 21, 1, 3,
        0, 34, 5,
        #20, 8, 2,
        #19, 6, 3,
        16, 10, 2,
        15, 12, 3,
        10, 9, 2,
        11, 11, 3,
        #9, 5, 3,
        # 6, 10, 2,

        # 15, 12, 3,
        # 11,11,3,
        # 0,0,0,
        # 0,0,0,
        # 0,0,0,
        # 0,0,0,
        0,0,0,
        0,0,0,
        0,0,0,
        0,0,0
        ]
        position_script = [#690,2820, 3.14159,#wait for little chicken
        # 401.556,2555.301,-2.294488, #mission 13 hand 21(0,1) cup 21 + 23
        937.777, 2824.441, 3.119224,#route to get two cup !need to change!
        1040.704, 2738.816, 2.437762,#route to get two cup !need to change!
        #1295.188, 2486.641, 2.512554,#route to get two cup !need to change!
        1285.019, 2507.630, 2.380629,#mission 13 hand 34(7,8) cup 22 + 24
        #310.461, 2441.248, -2.101246, #mission 12 hand 8(2) cup 20
        #269.303, 2219.526, -1.479989,#294.599, 2228, -1.546460, #mission 12 hand 6(3) cup 19
        1007.367, 1988.211, 0.893965,#mission 12 hand 6(3) cup 16
        1040.052, 1893.872, 1.834180, #mission 12 hand 8(2) cup 15
        1214.234, 1489.902, 1.860943, #mission 12 hand 5(5) cup 10
        1446.855, 1184.716, -3.022684, #mission 12 hand 7(4) cup 11
        #1023.438, 1352.961, 0.284053, #mission 12 hand 5(5) cup 10
        #652.288, 1214.775, -1.085210, #mission 12 hand 7(4) cup 9
        #590.199, 1132.844, 0.513628, #mission 12 hand 10(9) cup 6

        # 1114.633, 1562.207, -1.667093, #mission 12 hand 12(8) cup 15
        # 1535.012, 1508.660, 2.999664, #mission 12 hand 11(10) cup 11
        # 1823.005, 1234.059, math.pi,#mission 21 place backside 4 cup
        # 1777.299, 1234.059, math.pi, #mission 22 place backside 2 cup
        # 1398.836, 1234.059, math.pi, #mission 19 back off
        # 1398.836, 1234.059, 0, #mission 20 turn around
        1685.365, 1187.031, 3.14, #mission 21 place front 4 cup
        1585.365, 1187.031, 3.14,
        #1644.174, 1280.637, 0, #mission 18 place front 2 cup
        1455.734, 1187.031, 3.14, #mission 23 back off
        ]
        #remember to change the N or S position below!!!!
        #1900.0, 1800.0, 3.1415927410125732, 
        #  1800.0, 1800.0, 3.1415927410125732, 
        # 1770.0, 1800.0, 3.1415927410125732,
        #  1650.0, 1800.0, 3.1415927410125732,
        #   300.0, 200.0, 0.0
        
        # if req.team == 0:
        if req.ns == False:
            # scrpit_mission =[13, 14, 2, 16, 17, 12, 12, 12, 12, 12, 12, 12, 12, 9, 18, 19, 20, 21, 22, 23, 4]
            scrpit_mission.append(4)
            position_script.append(319.157) #N x
            position_script.append(2515.582) #N y
            position_script.append(2.202977) #N theta
        elif req.ns == True:
            scrpit_mission.append(5)
            position_script.append(1352.316) #S x
            position_script.append(2619.162) #S y
            position_script.append(1.612796) #S theta
            # scrpit_mission = [13, 14, 2, 16, 17, 12, 12, 12, 12, 12, 12, 12, 12, 9, 18, 19, 20, 21, 22, 23, 5]
        # cup_script = [0, 21, 5, 0, 34, 5, 0, 0, 0,  0, 0, 0,  0, 0, 0, 5, 5, 3,  6, 9, 2,  9, 6, 3,  10, 7, 2,  15, 11, 3, 16, 10, 2, 19, 12, 3, 20, 8, 2, 0, 0, 0, 0, 0, 0,0, 0, 0,0, 0,0, 0, 0, 0,0, 0, 0,0, 0, 0,0, 0,0]
        
        # elif req.team == 1:
        #     cup_script = [0, 21,5, 0, 34,5, 0, 0,0, 0, 0,0, 0, 0,0, 20, 7,2, 19, 5,3, 16, 8,2, 15, 6,3, 10, 9,2, 9, 11,3, 6, 10,2, 5, 12,3, 0, 0,0, 0, 0,0, 0, 0,0, 0, 0,0, 0, 0, 0,0, 0,0, 0, 0,0, 0, 0,0, 0, 0,0, 0, 0,0, 0, 0,0]
        #     position_script = [1085.0, 2600.0, 0.0, 500.0, 2600.0, 0.0, 150.0, 2725.0, 3.1415927410125732, 100.0, 2725.0, 3.1415927410125732, 150.0, 2725.0, 3.1415927410125732, 115.84193420410156, 2394.103759765625, 0.0, 243.43145751953125, 1994.5025634765625, -0.7853981852531433, 643.4314575195312, 1850.5025634765625, -2.356194496154785, 1043.431396484375, 1680.5025634765625, -0.7853981852531433, 1043.431396484375, 1220.5025634765625, -0.7853981852531433, 643.4314575195312, 1050.5025634765625, -0.7853981852531433, 243.43145751953125, 906.5025024414062, -0.7853981852531433, 110.69979858398438, 712.8905029296875, 1.1780972480773926, 1850.0, 1200.0, 0.0, 1870.0, 1200.0, 0.0, 1650.0, 1200.0, 0.0, 1900.0, 1200.0, 3.1415927410125732, 1800.0, 1200.0, 3.1415927410125732, 1770.0, 1200.0, 3.1415927410125732, 1650.0, 1200.0, 3.1415927410125732, 1850.0, 2800.0, 1.5707963705062866, 1850.0, 2300.0, 1.5707963705062866, 300.0, 2775.0, 0.0, 300.0, 2775.0, 0.0, ]
        #     if req.ns == False:
        #         scrpit_mission =[13, 14, 2, 16, 17, 12, 12, 12, 12, 12, 12, 12, 12, 9, 18, 19, 20, 21, 22, 23, 1, 15,4, 3]
        #     elif req.ns == True:
        #         scrpit_mission =[13, 14, 2, 16, 17, 12, 12, 12, 12, 12, 12, 12, 12, 9, 18, 19, 20, 21, 22, 23, 1, 15,5, 3]
        
        count_script = 0
        count_cup = 0
        while count_script < len( scrpit_mission):
            action.append(scrpit_mission[count_script])
            position.append(position_script[ 3* count_script])
            position.append(position_script[ 3* count_script + 1])
            position.append(position_script[ 3* count_script + 2])
            cup.append(cup_script[ 3* count_script])
            cup.append(cup_script[ 3* count_script + 1])
            cup.append(cup_script[ 3* count_script + 2])
            # if scrpit_mission[count_script] > 14:
            #     action.append(scrpit_mission[count_script])
            #     position.append(position_script[ 3* count_script])
            #     position.append(position_script[ 3* count_script + 1])
            #     position.append(position_script[ 3* count_script + 2])
            #     cup.append(cup_script[ 3* count_script])
            #     cup.append(cup_script[ 3* count_script + 1])
            #     cup.append(cup_script[ 3* count_script + 2])
            # else:
            #     for m in current.leaf:
            #         if m.name == scrpit_mission[ count_script ] or m.no == scrpit_mission[ count_script ]:
            #             if m.name == 'getcup_12':
            #                 action.append(13)
            #                 position.append(m.location[0])
            #                 position.append(m.location[1])
            #                 position.append(m.location[2])
            #                 cup.append(cup_script[ 3* count_script])
            #                 cup.append(cup_script[ 3* count_script + 1])
            #                 cup.append(cup_script[ 3* count_script + 2])
            #             elif m.name == 'getcup_34':
            #                 # ('action', 14, 'getcup_34', 500, 400, 0, 1, 3, 'hand', 3, 4)
            #                 action.append(14)
            #                 position.append(m.location[0])
            #                 position.append(m.location[1])
            #                 position.append(m.location[2])
            #                 cup.append(cup_script[ 3* count_script])
            #                 cup.append(cup_script[ 3* count_script + 1])
            #                 cup.append(cup_script[ 3* count_script + 2])
            #             elif m.name == 'getcup':
            #                 action.append(12)
            #                 position.append(position_script[ 3* count_script])
            #                 position.append(position_script[ 3* count_script + 1])
            #                 position.append(position_script[ 3* count_script + 2])
            #                 cup.append(cup_script[ 3* count_script])
            #                 cup.append(cup_script[ 3* count_script + 1])
            #                 cup.append(cup_script[ 3* count_script + 2])
            #             elif m.name == 'flag':
            #                 action.append(m.no)
            #                 position.append(req.my_pos[0])
            #                 position.append(req.my_pos[1])
            #                 position.append(req.my_pos[2])
            #                 # position.append(position[ 3* ( count_script - 1)])
            #                 # position.append(position[ 3*( count_script - 1) + 1])
            #                 # position.append(position[ 3*( count_script - 1)  + 2])
            #                 cup.append(cup_script[ 3* count_script])
            #                 cup.append(cup_script[ 3* count_script + 1])
            #                 cup.append(cup_script[ 3* count_script + 2])
            #             else:
            #                 action.append(m.no)
            #                 position.append(m.location[0])
            #                 position.append(m.location[1])
            #                 position.append(m.location[2])
            #                 cup.append(cup_script[ 3* count_script])
            #                 cup.append(cup_script[ 3* count_script + 1])
            #                 cup.append(cup_script[ 3* count_script + 2])
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
        print( a, "mission", action[a], "position", position[3*a], position[3*a + 1], position[3*a + 2], "cup", cup[ 3* a], cup[ 3* a + 1], cup[3* a + 2])
    return action, position, cup