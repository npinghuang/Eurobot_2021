#!/usr/bin/env python
#coding=utf-8
import math
import rospy
from main2021.srv import *
from precondition_little import *
from setting_little_goap import *
from scripts_little import *

print("start goap")
# global penalty_mission
penalty_mission = None
def emergency(current):
    location = current.location
    #back away distance
    d = 50
    theta = current.location[2]
    rad = theta * math.pi / 180
    (x, y) = ( location[0], location[1])
    count = 0
    state = 0
    while state == 0:
        #back off in the opposite direction
        x -= math.cos(rad) * d
        y -= math.sin(rad) * d
        #check if ( x, y ) will hit the border
        if x < 50:
            print("debug1",math.cos(rad) * d,  math.sin(rad) * d)
            x = 50
            rad += math.pi / 4
        elif x > 1950:
            x = 1950
            rad += math.pi / 4
        elif y < 50:
            y = 50
            rad += math.pi / 4
        elif y > 2950:
            y = 2950
            rad += math.pi / 4
        #check if ( x, y ) will hit cup or not
        else:
            for c in current.cup_state:
                if (x, y) == c['location']:
                    print("debug")
                    rad += math.pi / 4
                    break
                else:
                    count += 1
            if count == len(current.cup_state):
                state = 1
    location = ( int(x), int(y), theta)
    current.location = location
    return location

def evaluate(current, robot):
    score = 0
    red = 0
    green = 0
    cup = 0
    #number of times place cup when there is no freestorage
    num = int(len(current.cup_order) / robot.cupstorage)
    mm = 0
    for m in current.achieved:
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
    #cup score
    score += 2 * len(current.cup_order)
    for i in range(0, len(current.cup_order)):
        if current.cup_order[i]['color'] == 2:
            green += 1
        else:
            red += 1
    #calculate how many paired cup
    if red > green:
        score += 2 * green
    else:
        score += 2 * red
    return score

#     return action, position, cup
# service .res
action = []
position = []
cup = []
counter = 0 # for little mission
counter_scripts = 0 #for script

def GOAP_normal(req):
    print("-------------------------------------------------")
    global penalty_mission
    global counter
    global action
    global position
    global cup
    global previous_team
    time_main = req.time
    tmp = 0
    
    # print("previous current emergency", cur.emergency)
    if (cur.mission)!= None:
        print("previous action ", cur.mission.name)
        cur.previous_mission = cur.mission
    if cur.emergency == True: # document the action right before entering emergency state
        for mission in cur.mission_list:
            if cur.mission.name == mission.name:
                # global penalty_mission
                penalty_mission = mission
                # print("penalty", mission.name)
    else:
        # global penalty_mission
        penalty_mission = None
    (current, robot1) = mission_precondition(req)
    # print("cur.time", current.time)
    print("refresh reef status")
    current.reef_l = 1
    current.reef_r = 1
    current.reef_p = 1
    if req.hand[0] == 1:
        current.placecup_reef = 1
    #current.mission_list => a list of action available
    mission = len(current.mission_list)
    state = 1
    del current.achieved[:]
    del current.cup_order[:]
    
    if req.emergency == 1:
        #return location (x, y, theta), try to get out andont delete previous goap res data
        # print("current", current)
        location = emergency(current)
        action.insert(0,0)
        position.insert(0, location[2])
        position.insert(0, location[1])
        position.insert(0, location[0])
        cup.insert( 0, 0 )
        cup.insert( 0, 0 )
        cup.insert( 0, 0 )
        print("emergency", location)    
    elif req.time >= 100:
        action.append(0)
        position.append(current.location[0])
        position.append(current.location[1])
        position.append(current.location[2] )
        print("emergency", current.location)    
    elif req.emergency == 0:
        
        if cur.previous_mission != None and len(cur.previous_mission.little_mission_no) != 0 and action[0] != cur.previous_mission.little_mission_no[-1] and req.team == previous_team:
            # if little mission are done we will have to generate new goap data
            # if action[0] != cur.previous_mission.little_mission_no[-1]: 
                if action [0] != 0:#if previous action is not emergency
                    #remove previous action data
                    action.pop(0)
                    position.pop(0)
                    position.pop(0)
                    position.pop(0)
                    cup.pop(0)
                    cup.pop(0)
                    cup.pop(0)
                else:
                    # c = 0
                    while action[0] == 0:#therer may be more than one emergency action data in previous data
                        action.pop(0)
                        position.pop(0)
                        position.pop(0)
                        position.pop(0)
                        cup.pop(0)
                        cup.pop(0)
                        cup.pop(0)
                    action.pop(0)
                    position.pop(0)
                    position.pop(0)
                    position.pop(0)
                    cup.pop(0)
                    cup.pop(0)
                    cup.pop(0)
                print("action", action[0], position[0], position[1], position[2], 0)
                return action, position, cup
        else:
            del action[:]
            del position[:]
            del cup[:]
        (current, robot1) = mission_precondition(req)
        # current.placecup_reef = robot1.hand_little
        print("hand", current.placecup_reef)
        tt = 0
        while current.time < 90:
            # print("time", current.time)
            del current.mission_list[:] 
            friend = 0
            # print('debug', len(req.action_list), len(current.leaf))
            for a in range(0, len(req.action_list) ):
                if req.action_list[a] == 0:
                    for m in current.leaf:
                        if m.no == a:
                            if m.no == req.friend_action[0] and (req.friend_action[0] == 1 or req.friend_action[0] == 2 or req.friend_action[0] == 6 or req.friend_action[0] == 7 or req.friend_action == 8 or req.friend_action[0] == 9 or req.friend_action == 10 or req.friend_action[0] == 11):
                                friend = 1
                            else:
                                friend = 0
                                current.mission_list.append(m)
                elif req.action_list[a] == 1:
                    for m in current.leaf:
                        if m.no == a:
                            # print("debug", m.name)
                            if m.name == 'getcup':
                                current.mission_list.append(m)
                            else:
                                refreshstate(current, m, robot1, 0)
                            # print("current windsock", current.windsock, current.lhouse)
                elif req.action_list[a] == 3: #if mission failed 
                    for m in current.leaf:
                        if m.no == a and a < 13: # some mission we don't won't to retry  bugg!!!! cup no and m.name != 'getcup'
                            current.mission_list.append(m)
            if penalty_mission != None and tt == 0: #penalty on mission which had led to emergency
                tt = 1 #parameter to let penalty only be done once
                for m in current.mission_list:
                    if m.name == penalty_mission.name:
                        m.reward -= 50
                        print("penalty ", m.name, m.reward)

            # print("time", current.time)
            if tmp  == 0:
            #check if current states meet preconditions
                checkpreconditions(req, current, current.mission_list, robot1)
                if len(current.candidate) != 0:
                    compare_cost(current.candidate)
                    current.achieved.append(current.candidate[0])
                    # print("aa", current.candidate[0].name)
                    refreshstate(current, current.candidate[0], robot1, 1)
                    tmp = tmp + 1
                else:
                    current.time += 1
                    # print("no mission")
            else:
                checkpreconditions(req, current, current.mission_list, robot1)           
                if len(current.candidate) != 0:
                    compare_cost(current.candidate)
                    # print("aa", current.candidate[0].name)
                    current.achieved.append(current.candidate[0])
                    refreshstate(current, current.candidate[0], robot1, 1)
                else:
                    current.time += 1
                    # print("no mission")
            del current.candidate[:]
        # add anchor and flag as last two mission
        if current.time <  100 :
            for m in current.leaf:
                if m.name == "flag":
                    flag = m
                elif m.name == "anchorN":
                    anchorN = m
                elif m.name == "anchorS":
                    anchorS = m
            if current.NS == anchorN.NS and req.action_list[4] == 0:
                current.achieved.append(anchorN)
            elif current.NS == anchorS.NS and req.action_list[5] == 0:
                current.achieved.append(anchorS)
            if len(current.achieved) > 1:
                current.achieved.append(flag)
            elif req.time >= 95:
                current.achieved.append(flag)
        
        temp = 0
        i = 0 #little bug i forgot what this is for

	ff = 0
    # if current.time >= 90:
        for a in current.achieved: 
            if a.name == 'flag':
                print("action", a.no, a.name,current.location)
                action.append(a.no)
                position.append(current.location[0])
                position.append( current.location[1])
                position.append(current.location[2])
                cup.append( 0)
                cup.append(0)
                cup.append(0)
                # position.append(0)
                i += 1
            elif len( a.little_mission_no ) != 0:#add little mission pos
                for i in range( 0, len(a.little_mission_no)): # if a.no == 1 or a.no == 2 or  a.no == 9 or  a.no == 10: 
                    if i == 0:
                        print("action", a.no, a.name, a.location[0], a.location[1], a.location[2], 0)
                        action.append(a.no)
                        position.append(a.location[0])
                        position.append( a.location[1])
                        position.append(a.location[2] )
                        cup.append(0)
                        cup.append(0)
                        cup.append(0)
                    else:
                        print("action", a.little_mission_no[i], a.little_mission_pos[i][0], a.little_mission_pos[i][1], a.little_mission_pos[i][2], 0)
                        action.append(a.little_mission_no[i])
                        position.append(a.little_mission_pos[i][0])
                        position.append(a.little_mission_pos[i][1])
                        position.append(a.little_mission_pos[i][2] )
                        cup.append(0)
                        cup.append(0)
                        cup.append(0)
                i += 1
            else:
                if a.location != None:
                    print("action", a.no, a.name, a.location[0], a.location[1], a.location[2], 0)
                    action.append(a.no)
                    position.append(a.location[0])
                    position.append( a.location[1])
                    position.append(a.location[2] )
                    cup.append( 0)
                    cup.append(0)
                    cup.append(0)
                    i += 1
        if len ( current.achieved) != 0:
            current.mission = current.achieved[0]
        else:
            current.mission = None
        mission_list = []
        temp = 0
        for a in current.achieved:
            if a.name == 'getcup':
                c = (a.name, (current.cup_order[temp]['location']))
                mission_list.append(c)
                temp = temp + 1
            else:
                # print("achieved", a.name, a.location)
                c = (a.name, a.location)
                mission_list.append(c)

        score = evaluate(current, robot1)
        print("score", score)
        # for p in mission_list:
        #     print("mission_list", p)
        state = 0
    previous_team = req.team
    return action, position, cup
previous_team = None
# def GOAP_script(req):
#     global penalty_mission
#     global counter
#     global action
#     global position
#     global cup
#     global counter_scripts
#     global previous_team
#     # del action[:]
#     # del position[:]
#     # del cup[:]
#     # reset
#     print("len action", len(action))
#     # if len(action) == 0 + 1 or (req.team != 2 and req.team != previous_team):
#     #     counter_scripts = 0
#     #     del action[:]
#     #     del position[:]
#     #     del cup[:]

#     if req.emergency == True:
#         # print("debug action [0]", action[0])#delete this !!!
#         action.insert( 0,0)
#         position.insert( 0,req.my_pos[0])
#         position.insert( 0, req.my_pos[1])
#         position.insert( 0,req.my_pos[2] )
#         cup.insert( 0, 0)
#         cup.insert( 0,0)
#         cup.insert( 0,0)
#         return action, position, cup
#     if len(action) == 0 + 1 or (req.team != 2 and req.team != previous_team):
#         # counter_scripts = 0
#         action.append(0)
#         position.append(req.my_pos[0])
#         position.append(req.my_pos[1])
#         position.append(req.my_pos[2])
#         cup.append(0)
#         cup.append(0)
#         cup.append(0)
    
#     if req.emergency == False and counter_scripts == 0: #blue team script
        
#         (current, robot1) = mission_precondition(req)     
#         if req.team == 0:
#             if req.ns == False:
#                 scrpit_mission =[404]
#             elif req.ns == True:
#                 scrpit_mission = [404]
#             position_script = [404,404,404]
#             # cup_script = [0, 21, 0, 34, 0, 0, 0, 0, 0, 0, 5, 5, 6, 9, 9, 6, 10, 7, 15, 11, 16, 10, 19, 12, 20, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#         #('action', 13, 'getcup_12', 1085, 400, 0, 2, 4, 'hand', 2, 1)
#             # position_script = [1085.0, 400.0, 0.0, 500.0, 400.0, 0.0, 150.0, 275.0, 3.1415927410125732, 
#             # 100.0, 275.0, 3.1415927410125732, 150.0, 275.0, 3.1415927410125732, 
#             # 52.191062927246094, 636.3331909179688, 1.9634953737258911, 293.43145751953125, 906.5025024414062, -0.7853981852531433, 
#             # 693.4314575195312, 1050.5025634765625, -0.7853981852531433, 1093.431396484375, 1220.5025634765625, -2.356194496154785, 
#             # 1093.431396484375, 1680.5025634765625, -0.7853981852531433, 693.4314575195312, 1850.5025634765625, -0.7853981852531433, 
#             # 293.43145751953125, 1994.5025634765625, -0.7853981852531433, 62.56562805175781, 2326.696533203125, -0.39269909262657166, 
#             # 1900.0, 1800.0, 0.0, 1870.0, 1800.0, 0.0, 1650.0, 1800.0, 0.0, 1900.0, 1800.0, 3.1415927410125732, 1800.0, 1800.0, 3.1415927410125732, 
#             # 1770.0, 1800.0, 3.1415927410125732, 1650.0, 1800.0, 3.1415927410125732, 300.0, 200.0, 0.0, 300.0, 200.0, 0.0]
#         elif req.team == 1:
#             # cup_script = [0, 21, 0, 34, 0, 0, 0, 0, 0, 0, 20, 7, 19, 5, 16, 8, 15, 6, 10, 9, 9, 11, 6, 10, 5, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#             # position_script = [ 800.0, 2700.0, 0.0, 300.0, 2775.0, 0.0, ]
#             if req.ns == False:
#                 scrpit_mission =[7,26,27,11,30,4]
#                 position_script = [ 80, 2150, math.pi, 50, 2150, math.pi,  80, 2150, math.pi, 950,2500,0.0, 450,2500,0.0,300.0, 2500.0, 0.0]
#             elif req.ns == True:
#                 scrpit_mission =[7,26,27,11,30,5]
#                 position_script = [ 80, 2150, math.pi, 50, 2150, math.pi,  80, 2150, math.pi, 450,2500,math.pi, 950,2500,math.pi,1300.0, 2500.0, math.pi ]
# # action: [13, 14, 2, 16, 17, 12, 12, 12, 12, 12, 12, 12, 12, 9, 18, 19, 20, 21, 22, 23, 1, 15]
# # position: [1085.0, 2600.0, 0.0, 500.0, 2600.0, 0.0, 100.0, 2725.0, 3.1415927410125732, 50.0, 2725.0, 3.1415927410125732, 100.0, 2725.0, 3.1415927410125732, 95.84193420410156, 2394.103759765625, 0.0, 243.43145751953125, 1994.5025634765625, -0.7853981852531433, 643.4314575195312, 1850.5025634765625, -2.356194496154785, 1043.431396484375, 1680.5025634765625, -0.7853981852531433, 1043.431396484375, 1220.5025634765625, -0.7853981852531433, 643.4314575195312, 1050.5025634765625, -0.7853981852531433, 243.43145751953125, 906.5025024414062, -0.7853981852531433, 81.69979858398438, 712.8905029296875, 1.1780972480773926, 1850.0, 1200.0, 0.0, 1870.0, 1200.0, 0.0, 1650.0, 1200.0, 0.0, 1900.0, 1200.0, 3.1415927410125732, 1800.0, 1200.0, 3.1415927410125732, 1770.0, 1200.0, 3.1415927410125732, 1650.0, 1200.0, 3.1415927410125732, 1850.0, 2800.0, 1.5707963705062866, 1850.0, 2300.0, 1.5707963705062866]
# # cup: [0, 21, 0, 34, 0, 0, 0, 0, 0, 0, 20, 7, 19, 5, 16, 8, 15, 6, 10, 9, 9, 11, 6, 10, 5, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] 
#         count_script = 0
#         count_cup = 0
#         while count_script < len( scrpit_mission):
#             # if scrpit_mission[count_script] > 14:
#             action.append(scrpit_mission[count_script])
#             position.append(position_script[ 3* count_script])
#             position.append(position_script[ 3* count_script + 1])
#             position.append(position_script[ 3* count_script + 2])
#             cup.append(0)
#             cup.append(0)
#             cup.append(0)
#             # else:
#             #     for m in current.leaf:
#             #         if m.name == scrpit_mission[ count_script ] or m.no == scrpit_mission[ count_script ]:
#             #             action.append(m.no)
#             #             position.append(m.location[0])
#             #             position.append(m.location[1])
#             #             position.append(m.location[2])
#             #             cup.append(cup_script[ 2* count_script])
#             #             cup.append(cup_script[ 2* count_script + 1])
#             count_script += 1 #for appending next action
#     #pop old action
#     if counter_scripts > 0 and req.emergency == False:
#         action.pop(0)
#         position.pop(0)
#         position.pop(0)
#         position.pop(0)
#         cup.pop(0)
#         cup.pop(0)
#         cup.pop(0)
    
#     counter_scripts += 1
#     previous_team = req.team
#     for a in range(0, len(action)):
#         print( a, "mission", action[a], "position", position[3*a], position[3*a + 1], position[3*a + 2], "cup", cup[ 3* a], cup[ 3* a + 1],  cup[ 3* a + 2])
#     return action, position, cup
def GOAP(req):
    print("-------------------------------------------------")
    if req.strategy == 0:
        (action, position, cup) = GOAP_normal(req)
    elif req.strategy == 1:
        (action, position, cup) = GOAP_script(req)
    return action, position, cup
def goap_server():
    rospy.init_node('goap_server')
    s = rospy.Service('goap', goap_srv, GOAP)
    rospy.spin()         

if __name__ == "__main__":
    goap_server()
