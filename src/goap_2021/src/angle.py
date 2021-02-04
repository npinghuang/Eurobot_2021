desired = 180

theta = 15 #angle difference between robot and suction hand

angle_1 = 50 #robot
angle_2 = 0 # suction hand
cost_h = 1
cost_r = 1.5
cost_list = []
for i in range ( 0 , 50):
    # angle_1 = desired - (angle_2 + theta)
    cost = abs(desired - (angle_2 + theta) - angle_1) * cost_r + abs(i - angle_2) * cost_h
    cost_list.append(cost)
    print("cost", cost)

tmp = 0

tt = cost_list[0]
for i in range(1, len(cost_list)):
    if tt > cost_list[i]:
        tt = cost_list[i]
        tmp = i

print("best cost angle2", tt, tmp)
