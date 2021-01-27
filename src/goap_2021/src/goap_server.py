#!/usr/bin/env python
#coding=utf-8
import math
import rospy
from goap_2021.srv import *
from precondition import *
from setting_goap import *

def emergency(current):
    location = cur.location
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
            for c in cup_state:
                if (x, y) == c['location']:
                    rad += math.pi / 4
                    break
                else:
                    count += 1
            if count == len(cup_state):
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
    mission_precondition(req)
    tmp = 0
    mission = len(cur.mission_list)
    state = 1
    
    # while state == 1:
    if cur.emergency == 0:
        while cur.time < 95:
            # print("time", cur.time)
            leaf = [ anchorN, anchorS, flag, windsock, lhouse, getcup, reef_private, reef_left, reef_right, placecupP, placecupH, placecup_reef ]
            del cur.mission_list[:]
            friend = 0
            for a in range(0, len(action_list)):
                if action_list[a] == 0:
                    for m in leaf:
                        if m.no == a :
                            if m.no == friend_action and (friend_action == 1 or friend_action == 2 or friend_action == 6 or friend_action == 7 or friend_action == 8 or friend_action == 9 or friend_action == 10 or friend_action == 11):
                                friend = 1
                            else:
                                friend = 0
                                cur.mission_list.append(m)
                if action_list[a] == 1:
                    for m in leaf:
                        if m.no == a:
                            refreshstate(cur, m, robot1)
            # print("time", cur.time)
            if tmp  == 0:
            #check if current states meet preconditions
                checkpreconditions(cur, cur.mission_list, robot1)
                compare_cost(cur.candidate)
                cur.achieved.append(cur.candidate[0])
                refreshstate(cur, cur.candidate[0], robot1)
                tmp = tmp + 1
            else:
                checkpreconditions(cur, cur.mission_list, robot1)           
                if len(cur.candidate) != 0:
                    compare_cost(cur.candidate)
                    # print("aa", cur.candidate[0].name)
                    cur.achieved.append(cur.candidate[0])
                    refreshstate(cur, cur.candidate[0], robot1)
                else:
                    cur.time += 1
            #cur.candidate.clear()
            del cur.candidate[:]

        cur.achieved.append(flag)
        if cur.NS == anchorN.NS:
            cur.achieved.append(anchorN)
        else:
            cur.achieved.append(anchorS)

        temp = 0
        i = 0
        # action = []*len(cur.achieved)[]*5
        action = [[0 for x in range(len(cur.achieved))] for y in range(5)] 
        # action = array((len(cur.achieved), 5))
        ff = 0
        
        mission_list = []
        temp = 0
        for a in cur.achieved:
            if a.name == 'getcup':
                print("temp", temp)
                c = (a.name, (cur.cup_order[temp]['location']))
                mission_list.append(c)
                temp = temp + 1
            else:
                # print("achieved", a.name, a.location)
                c = (a.name, a.location)
                mission_list.append(c)

        score = evaluate(cur, robot1)
        print("score", score)
        for p in mission_list:
            print("mission_list", p)
        state = 0
    else:
        #return location (x, y, theta), try to get out
        location = emergency(cur)
        print("emergency", location) 

def goap_server():
    rospy.init_node('goap_server')
    s = rospy.Service('goap', goap_, GOAP)
    rospy.spin()         

if __name__ == "__main__":
    goap_server()
