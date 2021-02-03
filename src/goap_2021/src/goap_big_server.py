#!/usr/bin/env python
#coding=utf-8
import math
import rospy
from goap_2021.srv import *
from precondition import *
from setting_big_goap import *

print("start goap")

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

def GOAP(req):
    print("-------------------------------------------------")
    # print("previous current emergency", cur.emergency)
    if (cur.mission)!= None:
        print("previous action ", cur.mission.name)
    if cur.emergency == True: # document the action right before entering emergency state
        for mission in cur.mission_list:
            if cur.mission.name == mission.name:
                penalty_mission = mission
                # print("penalty", mission.name)
    else:
        penalty_mission = None
    (current, robot1) = mission_precondition(req)
    # print("cur.time", current.time)
    tmp = 0
    action = []
    action_pos = []
    cup = []
    #current.mission_list => a list of action available
    mission = len(current.mission_list)
    state = 1
    del current.achieved[:]
    del current.cup_order[:]
    if req.emergency == 1:
        #return location (x, y, theta), try to get out
        # print("current", current)
        location = emergency(current)
        action.append(0)
        action_pos.append(location[0])
        action_pos.append(location[1])
        action_pos.append(location[2] )
        print("emergency", location)    

    elif req.emergency == 0:
        (current, robot1) = mission_precondition(req)
        tt = 0
        while current.time < 90:
            # print("time", current.time)
            del current.mission_list[:] 
            friend = 0
            # print('debug', len(req.action_list), len(current.leaf))
            for a in range(0, len(req.action_list)):
                if req.action_list[a] == 0:
                    for m in current.leaf:
                        if m.no == a + 1:
                            if m.no == req.friend_action[0] and (req.friend_action[0] == 1 or req.friend_action[0] == 2 or req.friend_action[0] == 6 or req.friend_action[0] == 7 or req.friend_action == 8 or req.friend_action[0] == 9 or req.friend_action == 10 or req.friend_action[0] == 11):
                                friend = 1
                            else:
                                friend = 0
                                current.mission_list.append(m)
                elif req.action_list[a] == 1:
                    for m in current.leaf:
                        if m.no == a + 1:
                            # print("debug", m.name)
                            if m.name == 'getcup':
                                current.mission_list.append(m)
                            else:
                                refreshstate(current, m, robot1, 0)
                            # print("current windsock", current.windsock, current.lhouse)
                elif req.action_list[a] == 3: #if mission failed 
                    for m in current.leaf:
                        if m.no == a : # some mission we don't won't to retry  bugg!!!! cup no and m.name != 'getcup'
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
        if current.time <  100:
            #cur.leaf = [ windsock, lhouse, getcup, getcup_12, getcup_34, reef_private, reef_right, reef_left, placecup_reef, placecupP, placecupH, anchorN, anchorS, flag]
            flag = current.leaf[13]
            anchorN = current.leaf[11]
            anchorS = current.leaf[12]
            if current.NS == anchorN.NS:
                current.achieved.append(anchorN)
            else:
                current.achieved.append(anchorS)
            current.achieved.append(flag)
        
        # print("debug len", len(current.mission_list))
        # for p in current.mission_list:
        #     print("name", p.name)
        temp = 0
        i = 0

	ff = 0
    # if current.time >= 90:
        for a in current.achieved: 
            if a.name == 'getcup':
                print("action",current.cup_order[temp]['no'] , a.name, current.cup_order[temp]['location'][0], current.cup_order[temp]['location'][1], current.cup_order[temp]['location'][2],"hand: ",current.cup_order[temp]['hand'])
                action_pos.append(current.cup_order[temp]['location'][0])
                action_pos.append( current.cup_order[temp]['location'][1])
                action_pos.append( current.cup_order[temp]['location'][2])
                action_pos.append( current.cup_order[temp]['no'])
                cup.append(current.cup_order[temp]['no'])
                cup.append(current.cup_order[temp]['hand'])
                temp = temp + 1
                i += 1
            elif a.name == 'getcup_12' or a.name == 'getcup_34':
                print("action", a.no, a.name, a.location[0], a.location[1], a.location[2], 0,"hand", a.cup[0]['hand'], a.cup[1]['hand'])
                action.append(a.no)
                action_pos.append(a.location[0])
                action_pos.append( a.location[1])
                action_pos.append(a.location[2] )
                # action_pos.append(0)
                handd = a.cup[0]['hand'] * 10 + a.cup[1]['hand']
                cup.append( a.no * 10)
                cup.append(handd)
                temp += 2
            else:
                if a.location != None:
                    print("action", a.no, a.name, a.location[0], a.location[1], a.location[2], 0)
                    action.append(a.no)
                    action_pos.append(a.location[0])
                    action_pos.append( a.location[1])
                    action_pos.append(a.location[2] )
                    # action_pos.append(0)
                    # action_pos.append(None)

                    i += 1
                else:#flag has no location so i need to give last mission's location
                    print("action", a.no, a.name,action_pos[-1])
                    action.append(a.no)
                    action_pos.append(action_pos[-4])
                    action_pos.append( action_pos[-4])
                    action_pos.append(action_pos[-4] )
                    # action_pos.append(0)
                    i += 1
        current.mission = current.achieved[0]
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
        #for p in mission_list:
            #print("mission_list", p)
        state = 0

    return action, action_pos, cup

def goap_server():
    rospy.init_node('goap_server')
    s = rospy.Service('goap', goap_srv, GOAP)
    rospy.spin()         

if __name__ == "__main__":
    goap_server()
