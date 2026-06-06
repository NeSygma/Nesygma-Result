from z3 import *

# Define variables for positions 1..6
members = ['guitarist','keyboard','percussion','sax','trumpet','violin']
pos = {m: Int(m) for m in members}
solver = Solver()
# domain
for m in members:
    solver.add(pos[m] >= 1, pos[m] <= 6)
# all distinct
solver.add(Distinct([pos[m] for m in members]))
# constraints
solver.add(pos['guitarist'] != 4)
solver.add(pos['percussion'] < pos['keyboard'])
solver.add(pos['violin'] < pos['keyboard'])
solver.add(pos['keyboard'] < pos['guitarist'])
# sax after exactly one of percussion or trumpet
cond1 = And(pos['percussion'] < pos['sax'], pos['sax'] < pos['trumpet'])
cond2 = And(pos['trumpet'] < pos['sax'], pos['sax'] < pos['percussion'])
solver.add(Xor(cond1, cond2))

# function to test option

def test_option(person):
    s = Solver()
    s.append(solver.assertions())
    s.add(pos[person] == 3)
    return s.check()

for p in members:
    print(p, test_option(p))