#!/usr/bin/env python
#coding=utf-8
import math
import rospy
from main2021.srv import *
from precondition import *
from setting_big_goap import *
from scripts_big import *
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
            score += 15 
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
# service .res
action = []
position = []
cup = []
counter = 0 # for little mission
counter_scripts = 0 #for script

def GOAP_nornal(req):
    global penalty_mission
    global counter
    global action
    global position
    global cup
    global previous_team
    time_main = req.time
    tmp = 0
    # strategy 0 is not script 1 for script
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

    #current.mission_list => a list of action available
    mission = len(current.mission_list)
    state = 1
    del current.achieved[:]
    del current.cup_order[:]

    if req.emergency == 1:
        #return location (x, y, theta), try to get out andont delete previous goap res data
        # print("current", current)
        location = emergency(current)
        # action = list(action)
        # position = list(position)
        # cup = list(cup)
        action.insert(0,0)
        position.insert(0, location[2])
        position.insert(0, location[1])
        position.insert(0, location[0])
        cup.insert( 0, 0 )
        cup.insert( 0, 0 )
        print("emergency", location)    
    elif req.time >= 100:
        action.append(0)
        position.append(current.location[0])
        position.append(current.location[1])
        position.append(current.location[2] )
        cup.append( 0)
        cup.append(0)
        print("over 100 second", current.location)    
        return action, position, cup
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
                else:
                    # c = 0
                    while action[0] == 0:#therer may be more than one emergency action data in previous data
                        action.pop(0)
                        position.pop(0)
                        position.pop(0)
                        position.pop(0)
                        cup.pop(0)
                        cup.pop(0)

                    action.pop(0)
                    position.pop(0)
                    position.pop(0)
                    position.pop(0)
                    cup.pop(0)
                    cup.pop(0)
                print("action", action[0], position[0], position[1], position[2], 0)
                return action, position, cup
        else:
            del action[:]
            del position[:]
            del cup[:]
        (current, robot1) = mission_precondition(req)
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
            #check if mission had been done
            # for m in current.mission_list:
            #     if m in current.achieved:
            #         print("same action",  m.name)
            #         current.mission_list.remove(m)
            # print("time", current.time)
            if tmp  == 0:
            #check if current states meet preconditions
                checkpreconditions(req, current, current.mission_list, robot1)
                if len(current.candidate) != 0:
                    # compare_cost(current.candidate)
                    # current.achieved.append(current.candidate[0])
                    current.achieved.append(compare_cost(current.candidate))
                    # print("aa", compare_cost(current.candidate).name, current.achieved[-1].name)
                    refreshstate(current, current.candidate[0], robot1, 1)
                    tmp = tmp + 1
                else:
                    current.time += 1
                    # print("no mission")
            else:
                checkpreconditions(req, current, current.mission_list, robot1)           
                if len(current.candidate) != 0:
                    # compare_cost(current.candidate)
                    # for d in current.candidate:
                        # print("debug candidate", d.name)
                    # current.achieved.append(current.candidate[0])
                    current.achieved.append(compare_cost(current.candidate))
                    # print("aa", compare_cost(current.candidate).name, current.achieved[-1].name)
                    refreshstate(current, current.candidate[0], robot1, 1)
                else:
                    current.time += 1
                    # print("no mission")
            del current.candidate[:]
        if current.time <  100 :
            #cur.leaf = [ windsock, lhouse, getcup, getcup_12, getcup_34, reef_private, reef_right, reef_left, placecup_reef, placecupP, placecupH, anchorN, anchorS, flag]
            # flag = current.leaf[13]
            # anchorN = current.leaf[11]
            # anchorS = current.leaf[12]
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
            if a.name == 'getcup':
                print("action",current.cup_order[temp]['no'] , a.name, current.cup_order[temp]['location'][0], current.cup_order[temp]['location'][1], current.cup_order[temp]['location'][2],"hand: ",current.cup_order[temp]['hand_ST'], "color : ",current.cup_order[temp]['color'])
                position.append(current.cup_order[temp]['location'][0])
                position.append( current.cup_order[temp]['location'][1])
                position.append( current.cup_order[temp]['location'][2])
                # position.append( current.cup_order[temp]['no'])
                action.append(a.no)
                cup.append(current.cup_order[temp]['no'])
                # cup.append(current.cup_order[temp]['hand'] + 1) #change hand number to start from 1
                cup.append(current.cup_order[temp]['hand_ST']) #same with ST2
                cup.append(current.cup_order[temp]['color'] ) 
                temp = temp + 1
                i += 1
            elif a.name == 'getcup_12' or a.name == 'getcup_34':
                print("action", a.no, a.name, a.location[0], a.location[1], a.location[2], a.cup[0]['no'], a.cup[1]['no'],"hand", current.cup_state[a.cup[0]['no']-1]['hand']  + 1, current.cup_state[a.cup[1]['no']-1]['hand'] + 1, 5)
                action.append(a.no)
                position.append(a.location[0])
                position.append( a.location[1])
                position.append(a.location[2] )
                # position.append(0)current.cup_state[a]['hand'] 
                handd = (current.cup_state[a.cup[0]['no']-1]['hand']  + 1) * 10 + current.cup_state[a.cup[1]['no']-1]['hand'] + 1#change hand number to start from 1
                cup.append( 0)
                cup.append(handd)
                cup.append(5)
                temp += 2
            elif a.name == 'flag':
                print("action", a.no, a.name,a.location)
                action.append(a.no)
                for a in current.achieved:
                    if a.no == 4 or a.no == 5:
                        position.append(a.location[0])
                        position.append( a.location[1])
                        position.append(a.location[2])
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

    #if no action
    if len( position ) == 0:
        action.append(0)
        position.append(current.location[0])
        position.append( current.location[1])
        position.append(current.location[2] )
        cup.append( 0)
        cup.append(0)
        cup.append(0)
    previous_team = req.team
    return action, position, cup
previous_team = None

def GOAP(req):
    print("-------------------------------------------------")
    if req.strategy == 0:
        (action, position, cup) = GOAP_nornal(req)
    elif req.strategy == 1:
        (action, position, cup) = GOAP_script(req)
    return action, position, cup
    

def goap_server():
    rospy.init_node('goap_server')
    s = rospy.Service('goap', goap_srv, GOAP)
    rospy.spin()         

if __name__ == "__main__":
    goap_server()
