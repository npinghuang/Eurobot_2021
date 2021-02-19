from setting_mission import*
#define action for each mission here

def getcup_action(cup):
    if len(cup.action_list) > 0:
        pp = cup.action_list.pop(0)
        print("i want to go home", pp)
        return 0
    else:
        print("mission done")
        return 1

def placecupH_action(placecup ):
    if placecup.count < len(placecup.action_list):
        print("placecup action", placecup.action_list[ placecup.count ])
        placecup.count += 1
    if placecup.count == len(placecup.action_list) :
        placecup.count = 0
        print("place cup h mission done!")
    