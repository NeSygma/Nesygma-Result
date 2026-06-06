from z3 import *

# Define zones as ints 1,2,3
people = ['Kim','Mahr','Parra','Quinn','Stuckey','Tiao','Udall']
zone = {p: Int(p) for p in people}
solver = Solver()
# each zone in 1..3
for p in people:
    solver.add(And(zone[p] >= 1, zone[p] <= 3))
# constraints
# 1. Exactly one of Parra or Tiao in Zone1
solver.add(Or(And(zone['Parra']==1, zone['Tiao']!=1), And(zone['Tiao']==1, zone['Parra']!=1)))
# 2. Exactly one of Tiao or Udall in Zone2
solver.add(Or(And(zone['Tiao']==2, zone['Udall']!=2), And(zone['Udall']==2, zone['Tiao']!=2)))
# 3. Parra and Quinn same zone
solver.add(zone['Parra'] == zone['Quinn'])
# 4. Stuckey and Udall same zone
solver.add(zone['Stuckey'] == zone['Udall'])
# 5. More reps in Zone3 than Zone2
cnt2 = Sum([If(zone[p]==2,1,0) for p in people])
cnt3 = Sum([If(zone[p]==3,1,0) for p in people])
solver.add(cnt3 > cnt2)

# function to test option
options = {
    'A': And(zone['Kim']==1, zone['Stuckey']==1),
    'B': And(zone['Kim']==3, zone['Stuckey']==3),
    'C': And(zone['Mahr']==3, zone['Stuckey']==3),
    'D': And(zone['Mahr']==3, zone['Udall']==3),
    'E': And(zone['Parra']==1, zone['Stuckey']==1),
}

sat_options = []
for letter, constr in options.items():
    s = Solver()
    s.add(solver.assertions())
    s.add(constr)
    if s.check() == sat:
        sat_options.append(letter)
print('SAT options:', sat_options)

# also list a model for each sat option
for letter in sat_options:
    s = Solver()
    s.add(solver.assertions())
    s.add(options[letter])
    if s.check() == sat:
        m = s.model()
        print(letter, {p: m[zone[p]] for p in people})