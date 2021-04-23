"""
determine which cup to get
=======================================================
"""
#!/usr/bin/env python
#coding=utf-8
import math
from setting_big_goap import *
from precondition import*

def cup_cost(req, current, mission, robot):
    cup_location_transfrom(current.cup_state)
    #see claw suction state ( whether they have room to take cup )]
    front_claw = [ 0, 0 ]
    back_claw = [ 0, 0 ]
    front_suction = [ 0, 0 ] #[0] for green [1] for red value 1 stand for can take cup
    back_suction = [ 0, 0 ] #[0] for green [1] for red
    check_hand = 0
    red_hand = 0
    green_hand = 0
    case = ''
    for claw in robot.claw:
        if claw['state'] == 0:
            check_hand += 1
            if claw['color'] == 2:
                green_hand += 1
            else:
                red_hand += 1
            if claw['no'] <= 1:
                front_claw[ claw['color'] - 2 ] = 1 # 1 stand for can take cup
            elif claw['no'] > 1:
                back_claw[ claw['color'] - 2 ] = 1
    for suc in robot.suction:
        if suc['state'] == 0: 
            check_hand += 1
            if suc['color'] == 2:
                green_hand += 1
            else:
                red_hand += 1
            if suc['no'] <= 3 and front_suction [ suc['color'] - 2 ] == 0:
                front_suction [ suc['color'] - 2 ] = 1 
            elif suc['no'] > 3 and back_suction [ suc['color'] - 2 ] == 0:
                back_suction [ suc['color'] - 2 ] = 1
    if check_hand == 0: #no free hand so can not get cup
        mission = None
        return mission

    available_cup = []
    for cup in current.cup_state:
        state = 1
        
        if req.friend_action[0] == 12 and  req.friend_action[1] == current.cup_state[c]['no']:#check it is not the same cup as friend's action
            state = 0
        elif cup['state'] == 1:
            if (cup['color'] == 2 and green_hand )> 0 or (cup['color'] == 3 and red_hand ): # check if robot can take cup
                #determine which way to face
                if (front_suction[ cup['color'] - 2 ] ==1 or front_claw[ cup['color'] - 2 ]  == 1) and (back_suction[ cup['color'] - 2 ] == 1 or back_claw[ cup['color'] - 2 ] == 1):
                    case = front_back_determination( current.location, cup['location'])
                elif back_suction[ cup['color'] - 2 ] == 1 or back_claw[ cup['color'] - 2 ] == 1:
                    case = 'back'
                elif front_suction[ cup['color'] - 2 ] ==1 or front_claw[ cup['color'] - 2 ]  == 1:
                    case = 'front'
                #determine the closest distance between each cup
                if case == 'front':
                    turn = 0
                elif case == 'back':
                    turn = -math.pi
                
                if len(cup['robot_pos']) > 0:
                    # print("cup debug", cup['no'], cup['robot_pos'][0])
                    d = distance( cup['robot_pos'][0], current.location)
                    for pos in cup['robot_pos']:
                        pos[2] += turn
                        dd = distance( pos, current.location)
                        if dd > d:
                            cup['robot_pos'].remove(pos)
                        else:
                            d = dd
                    cup['distance'] = d
                else:
                    state = 0
                    cup['distance'] = 9999999999

                #determine which hand to use
                if case == 'front' and state != 0:
                    # print("check if there is bug")
                    if cup['color'] == 2:
                        if front_claw[0] == 1:
                            cup['robot_pos'][0][0] -= robot.claw[0]['location'][0] * math.cos(robot.claw[0]['location'][2])
                            cup['robot_pos'][0][1] -= robot.claw[0]['location'][1] * math.sin(robot.claw[0]['location'][2])
                            cup['robot_pos'][0][2] += robot.claw[0]['location'][2]
                            cup['hand'] = 0
                            cup['hand_ST'] = 1
                        elif front_suction[0] == 1:
                            cup['robot_pos'][0][0] -= robot.suction[0]['location'][0] * math.cos(robot.suction[0]['location'][2])
                            cup['robot_pos'][0][1] -= robot.suction[0]['location'][1] * math.sin(robot.suction[0]['location'][2])
                            cup['robot_pos'][0][2] += robot.suction[0]['location'][2]
                            if robot.suction[1]['state'] == 0:
                                cup['hand' ] = 5
                                cup['hand_ST'] = 3
                            else:
                                cup['hand' ] = 4
                                cup['hand_ST'] = 5
                        else:
                            case = 'back'
                    else:#red
                        if front_claw[1] == 1:
                            cup['robot_pos'][0][0] -= robot.claw[1]['location'][0] * math.cos(robot.claw[1]['location'][2])
                            cup['robot_pos'][0][1] -= robot.claw[1]['location'][1] * math.sin(robot.claw[1]['location'][2])
                            cup['robot_pos'][0][2] += robot.claw[1]['location'][2]
                            cup['hand'] = 1
                            cup['hand_ST'] = 0
                        elif front_suction[1] == 1:
                            cup['robot_pos'][0][0] -= robot.suction[2]['location'][0] * math.cos(robot.suction[2]['location'][2])
                            cup['robot_pos'][0][1] -= robot.suction[2]['location'][1] * math.sin(robot.suction[2]['location'][2])
                            cup['robot_pos'][0][2] += robot.suction[2]['location'][2]
                            if robot.suction[3]['state'] == 0:
                                cup['hand' ] = 7
                                cup['hand_ST'] = 2
                            else:
                                cup['hand' ] = 6
                                cup['hand_ST'] = 4
                elif case == 'back' and state != 0:
                    if cup['color'] == 2:
                        if back_claw[0] == 1:
                            cup['robot_pos'][0][0] -= robot.claw[3]['location'][0] * math.cos(robot.claw[3]['location'][2])
                            cup['robot_pos'][0][1] -= robot.claw[3]['location'][1] * math.sin(robot.claw[3]['location'][2])
                            cup['robot_pos'][0][2] += robot.claw[3]['location'][2]
                            cup['hand' ] = 3
                            cup['hand_ST'] = 6
                        elif back_suction[0] == 1:
                            cup['robot_pos'][0][0] -= robot.suction[7]['location'][0] * math.cos(robot.suction[7]['location'][2])
                            cup['robot_pos'][0][1] -= robot.suction[7]['location'][1] * math.sin(robot.suction[7]['location'][2])
                            cup['robot_pos'][0][2] += robot.suction[7]['location'][2]
                            if robot.suction[7]['state'] == 0:
                                cup['hand' ] = 11
                                cup['hand_ST'] = 8
                            else:
                                cup['hand' ] = 10
                                cup['hand_ST'] = 10
                        else:
                            mission = None
                    else:#red
                        if back_claw[1] == 1:
                            cup['robot_pos'][0][0] -= robot.claw[2]['location'][0] * math.cos(robot.claw[2]['location'][2])
                            cup['robot_pos'][0][1] -= robot.claw[2]['location'][1] * math.sin(robot.claw[2]['location'][2])
                            cup['robot_pos'][0][2] += robot.claw[2]['location'][2]
                            cup['hand' ] = 2
                            cup['hand_ST'] = 7
                        elif back_suction[1] == 1:
                            cup['robot_pos'][0][0] -= robot.suction[6]['location'][0] * math.cos(robot.suction[6]['location'][2])
                            cup['robot_pos'][0][1] -= robot.suction[6]['location'][1] * math.sin(robot.suction[6]['location'][2])
                            cup['robot_pos'][0][2] += robot.suction[6]['location'][2]
                            if robot.suction[5]['state'] == 0:
                                cup['hand' ] = 9
                                cup['hand_ST'] = 9
                            else:
                                cup['hand' ] = 8
                                cup['hand_ST'] = 11
                elif case == 'none':
                    mission = None
        
                if state != 0:
                    available_cup.append(cup)
    # print("debug", len(available_cup))
    # for cup in available_cup:
    #     print("cup", cup['no'], type(cup['distance']))
    

    if len( available_cup ) > 0:
        # def myFunc(e):
        #     return e['distance']
        # available_cup.sort(key=myFunc)
        # mission = available_cup[0]
        # mission['location'] = available_cup[0]['robot_pos'][0]
        # i am soo dumb dumb
        distance_min = available_cup[0]['distance']
        min_no = 0
        ii = 0
        for d in available_cup:
            if d['distance'] < distance_min:
                distance_min = d['distance']
                min_no = ii
            ii += 1
        # print("cup min", available_cup[min_no]['no'], available_cup[min_no]['robot_pos'][0])
        if min_no != None:
            mission = available_cup[min_no]
            mission['location'] = available_cup[min_no]['robot_pos'][0]
    else :
        mission = None

    return mission

def front_back_determination( current, pos):
    x = current[0]
    y = current[1]
    theta = current[2]
    if (theta == math.pi  / 2):
        # print("tan90", math.tan(math.pi/2))
        tangent = 1
    elif  theta ==( -math.pi / 2):
        tangent = -1
    else:
        tangent = math.tan(theta)
    if tangent == 0:
        line = ( y) * pos[0] + ( x + y * (tangent)) * pos[1]
        tmp = ( y ) * ( x + y * (tangent))
    else:
        line = ( y + x / tangent) * pos[0] + ( x + y * (tangent)) * pos[1]
        tmp = ( y + x / tangent) * ( x + y * (tangent))
    # 1 for back 0 for front
    if line < tmp:
        return 'back'
    else:
		return 'front'
