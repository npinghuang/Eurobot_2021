#!/usr/bin/env python
#coding=utf-8
import math
import rospy
from goap_2021.srv import *
from precondition import *
from setting_goap import *

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
    (current, robot1) = mission_precondition(req)
    tmp = 0
    action = []
    action_pos = []
    mission = len(current.mission_list)
    state = 1
    if current.emergency == 1:
        #return location (x, y, theta), try to get out
        location = emergency(current)
        action.append(0)
        action_pos.append(location[0])
        action_pos.append(location[1])
        action_pos.append(location[2] )
        print("emergency", location)    

    elif current.emergency == 0:
        while current.time < 95:
            # print("time", current.time)
            del current.mission_list[:]
            friend = 0
            for a in range(0, len(req.action_list)):
                if req.action_list[a] == 0:
                    for m in current.leaf:
                        if m.no == a :
                            if m.no == req.friend_action and (req.friend_action == 1 or req.friend_action == 2 or req.friend_action == 6 or req.friend_action == 7 or req.friend_action == 8 or req.friend_action == 9 or req.friend_action == 10 or req.friend_action == 11):
                                friend = 1
                            else:
                                friend = 0
                                current.mission_list.append(m)
                if req.action_list[a] == 1:
                    for m in current.leaf:
                        if m.no == a:
                            refreshstate(current, m, robot1)
            # print("time", current.time)
            if tmp  == 0:
            #check if current states meet preconditions
                checkpreconditions(req, current, current.mission_list, robot1)
                compare_cost(current.candidate)
                current.achieved.append(current.candidate[0])
                refreshstate(current, current.candidate[0], robot1)
                tmp = tmp + 1
            else:
                checkpreconditions(req, current, current.mission_list, robot1)           
                if len(current.candidate) != 0:
                    compare_cost(current.candidate)
                    # print("aa", current.candidate[0].name)
                    current.achieved.append(current.candidate[0])
                    refreshstate(current, current.candidate[0], robot1)
                else:
                    current.time += 1
            del current.candidate[:]
	flag = current.leaf[11]
	anchorN = current.leaf[9]
	anchorS = current.leaf[10]
        if current.NS == anchorN.NS:
            current.achieved.append(anchorN)
        else:
            current.achieved.append(anchorS)
        current.achieved.append(flag)

        temp = 0
        i = 0

	ff = 0
        for a in current.achieved: 
            if a.name == 'getcup':
                print("action",current.cup_order[temp]['no'] , a.name, current.cup_order[temp]['location'][0], current.cup_order[temp]['location'][1], current.cup_order[temp]['location'][2])
                action_pos.append(current.cup_order[temp]['location'][0])
                action_pos.append( current.cup_order[temp]['location'][1])
                action_pos.append( current.cup_order[temp]['location'][2])
                action_pos.append( current.cup_order[temp]['no'])
		action.append(a.no)
                
                temp = temp + 1
                i += 1
            else:
                if a.location != None:
                    print("action", a.no, a.name, a.location[0], a.location[1], a.location[2], 0)
                    action.append(a.no)
                    action_pos.append(a.location[0])
                    action_pos.append( a.location[1])
                    action_pos.append(a.location[2] )
                    action_pos.append(0)

                    i += 1
                else:#flag has no location so i need to give last mission's location
                    print("action", a.no, a.name,action_pos[-1])
                    action.append(a.no)
                    action_pos.append(action_pos[-4])
                    action_pos.append( action_pos[-4])
                    action_pos.append(action_pos[-4] )
                    action_pos.append(0)
                    i += 1
        
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

    return action, action_pos

def goap_server():
    rospy.init_node('goap_server')
    s = rospy.Service('goap', goap_, GOAP)
    rospy.spin()         

if __name__ == "__main__":
    goap_server()
