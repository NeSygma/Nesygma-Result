from z3 import *

# Define positions 1..6 for each member
members = ['guitarist','keyboard','percussion','sax','trumpet','violin']
pos = {m: Int(m) for m in members}
solver = Solver()
# domain constraints
for m in members:
    solver.add(pos[m] >= 1, pos[m] <= 6)
# all distinct
solver.add(Distinct([pos[m] for m in members]))
# given constraints
solver.add(pos['guitarist'] != 4)
solver.add(pos['percussion'] < pos['keyboard'])
solver.add(pos['violin'] < pos['keyboard'])
solver.add(pos['keyboard'] < pos['guitarist'])
# sax after exactly one of percussion or trumpet (xor)
cond1 = And(pos['percussion'] < pos['sax'], pos['sax'] < pos['trumpet'])
cond2 = And(pos['trumpet'] < pos['sax'], pos['sax'] < pos['percussion'])
solver.add(Xor(cond1, cond2))

# Test each option: can this member be third?
found_options = []
option_constraints = []
for letter, person in zip(['A','B','C','D','E'], members):
    # constraint that this person is third
    opt_constr = pos[person] == 3
    option_constraints.append((letter, opt_constr))

for letter, constr in option_constraints:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Determine answer: the member that CANNOT be third is the one NOT in found_options
all_letters = ['A','B','C','D','E']
cannot = [l for l in all_letters if l not in found_options]
if len(cannot) == 1:
    print("STATUS: sat")
    print(f"answer:{cannot[0]}")
elif len(found_options) == 1:
    # fallback if exactly one can be third (unlikely for this problem)
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
else:
    print("STATUS: unsat")
    print(f"Refine: ambiguous options, can:{found_options}, cannot:{cannot}")