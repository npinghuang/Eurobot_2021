#!/usr/bin/env python
#coding=utf-8
import math
import rospy
from main2021.srv import *
from precondition_little import *
from setting_little_goap import *
from goap_little_server import *
count_script = 0

def GOAP_script(req):
  global penalty_mission
  global counter
  global action
  global position
  global cup
  global counter_scripts
  global previous_team
  global count_script
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
  # if len(action) == 0 + 1 or (req.team != 2 and req.team != previous_team): 
  #     # counter_scripts = 0
  #     action.append(0)
  #     position.append(req.my_pos[0])
  #     position.append(req.my_pos[1])
  #     position.append(req.my_pos[2])
  #     cup.append(0)
  #     cup.append(0)
  #     cup.append(0)
  
  if req.emergency == False and counter_scripts == 0: #blue team script
      
    (current, robot1) = mission_precondition(req)     

    # scrpit_mission =[31,16,17,16,
    # 7,51,26,27,
    # 11,30,
    # 50,1,32,51,
    # 8,28,29,
    # 45,46,47,48,49,30,
    # 4]
    scrpit_mission =[3]
    position_script = [ 1085, 2804,math.pi,#back away
      200, 2804,math.pi, #move forward a little bit before lighthouse
      100, 2804, math.pi, #hit lighthouse
      200, 2804,math.pi, #move backward a little bit after lighthouse

      200, 2200, math.pi,#in front of reef
      100, 2200, math.pi,#in front of reef  
      40, 2200,  math.pi, #get cup
      200, 2200, math.pi, #in front of reef
      # 650.87,2770.306,0.0253, # to/avoid the fucking bump

      655,2800,math.pi,#place red cup
      1185,2800,math.pi,#place green cup

      1850,2840,-math.pi/2, #first point of windsock
      1850,2955,-math.pi/2, # move backward prepare to accelerate for windsock
      1850,2240,-math.pi/2,#second point of windsock retrieve hand
      1850,2240,math.pi,#second point of windsock retrieve hand

      1600,2240,math.pi/2,#before reef private
      1600,2975,math.pi/2,#getcup
      1600,2820,math.pi,#after reef private
      
      1260,2820,math.pi,#place green cup
      1365,2820,-math.pi/2,#move backward
      1365,2420,math.pi,#move backward
      240,2420,math.pi/2,#move backward
      240,2880,0,#move backward
      330,2880,0,#place red cup
      100,2880,0,#go to N
      
          ] # back away
              # old script
              # 1078, 2804,math.pi,#back away
              # 700, 2804,math.pi, #move forward a little bit
              # 371.9, 2155.79, 3.12,#in front of reef 
              # 41.92, 2155.79,  3.12, #get cup
              # 416.851, 2155.79, 3.12, #in front of reef
              # 650.87,2780.306,0.0253, # to avoid the fucking bump
              # 965.402,2780.306,0.0253,#place green cup
              # 379.727,2780.306,0.0253,#place red cup
              # 272.188,2780.306,0.0253,#back away
              # 272.188,2780.306,-1.57,#spin
              # 272.188,2889.034,-1.57]# back away
          # elif req.ns == True:
          # scrpit_mission =[31,35,7,26,27,11,30,32,33,34]
          # position_script = [ 1078, 2804,math.pi,#back away
          #     700, 2804,math.pi,#move forward a little bit
          #     371.9, 2155.79, 3.12,#in front of reef 
          #     41.92, 2155.79,  3.12,#get cup
          #     416.851, 2155.79, 3.12,#in front of reef
          #     612.879,2767.269,math.pi, #place red cup
          #     1188.579,2767.269,math.pi,#place green cup
          #     1289.645,2767.269,math.pi,#back away
          #     1289.645,2767.269,-1.603495,#spin
          #     1289.645,2884.954,-1.603495]# back away
    # if req.ns == False:
    # scrpit_mission.append(4)
    # position_script.append(246.743) #N x
    # position_script.append(2485.069) #N y
    # position_script.append(2.307810) #N theta
    # elif req.ns == True:
    #   scrpit_mission.append(5)
    #   position_script.append(1352.316) #S x
    #   position_script.append(2619.162) #S y
    #   position_script.append(1.612796) #S theta

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
  if counter_scripts > 0 and req.emergency == False and counter_scripts < count_script :
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
