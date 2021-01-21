# ( ( x, y ), 1 for cup still there 0 for cup gone,  2  for green 3 for red) 
#blue
# cup_state = [ (( 510, 450 ), 1, 2), (( 1200, 300 ), 1, 2), (( 400, 300 ), 1, 3), (( 1080, 450 ), 1, 3), (( 1650, 1665 ), 1, 2), 
#                 (( 1955, 1995 ), 1, 2), (( 1955, 1605 ), 1, 3), (( 1650, 1935 ), 1, 3), (( 100, 670 ), 1, 2), ((800, 1100 ), 1, 2),
#                 (( 1200, 1730 ), 1, 2), (( 400, 2050 ), 1, 2), (( 400, 950 ), 1, 3), (( 1200, 1270 ), 1, 3), (( 800, 1900 ), 1, 3),
#                 (( 100, 2330 ), 1, 3) ]

cup_state = [ { 'location' : ( 510, 450 ), 'state' : 1, 'color' : 2} , { 'location' : ( 1200, 300 ), 'state' : 1, 'color' : 2},
                { 'location' : ( 400, 300 ), 'state' : 1, 'color' : 3}, { 'location' : ( 1080, 450 ), 'state' : 1, 'color' : 3} ,
                { 'location' : ( 1650, 1665 ), 'state' : 1, 'color' : 2}, { 'location' : ( 1955, 1995 ), 'state' : 1, 'color' : 2},
                { 'location' : ( 1955, 1605 ), 'state' : 1, 'color' : 3}, { 'location' : ( 1650, 1935 ), 'state' : 1, 'color' : 3},
                { 'location' : ( 100, 670 ), 'state' : 1, 'color' : 2}, { 'location' : ( 800, 1100 ), 'state' : 1, 'color' : 2},
                { 'location' : ( 1200, 1730 ), 'state' : 1, 'color' : 2} , { 'location' : ( 400, 2050 ), 'state' : 1, 'color' : 2},
                { 'location' : ( 400, 950 ), 'state' : 1, 'color' : 3}, { 'location' : ( 1200, 1270 ), 'state' : 1, 'color' : 3},
                { 'location' : ( 800, 1900 ), 'state' : 1, 'color' : 3}, { 'location' : ( 100, 2330 ), 'state' : 1, 'color' : 3} ]       


current = ( 200, 750 )

# calculate Manhattan distance
for cup in cup_state:
    d = abs( current[0] - cup['location'][0] ) + abs( current[1] - cup['location'][1])
    cup['distance'] = d

def myFunc(e):
  return e['distance']

cup_state.sort(key=myFunc)

i = 1
c = 0
while i == 1 :
    if cup_state[c]['state'] == 1:
        print( 'mission', cup_state[c]['location'])
        i = 0
    else:
        c += 1
for cup in cup_state:
    print(cup['distance'])

# def cup_cost(current, cup_state):
for c in cup_state:

    if ( 510, 450 ) == c['location']:
        print('?', c['location'],c['color'])

def distance(a, b):
    d = int((abs( a[0] - b[0] )**2 + abs( a[1] - b[1])**2)**0.5)
    return d

p = distance((0,0), (30, 40))
print(p)