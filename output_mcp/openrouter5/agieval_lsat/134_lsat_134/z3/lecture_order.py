from z3 import *

# We have 5 positions (1 to 5) and 5 bird types.
# Let's encode positions as integers 0..4 (first=0, fifth=4)
# Bird types: 0=oystercatchers, 1=petrels, 2=rails, 3=sandpipers, 4=terns
# Locations: 0=Gladwyn Hall, 1=Howard Auditorium

solver = Solver()

# Variables: pos[i] = bird type at position i (0-indexed)
pos = [Int(f'pos_{i}') for i in range(5)]
# Variables: loc[i] = location at position i
loc = [Int(f'loc_{i}') for i in range(5)]

# Domain constraints
for i in range(5):
    solver.add(pos[i] >= 0, pos[i] <= 4)
    solver.add(loc[i] >= 0, loc[i] <= 1)

# Each bird type appears exactly once
solver.add(Distinct(pos))

# The first lecture (position 0) is in Gladwyn Hall (0)
solver.add(loc[0] == 0)

# The fourth lecture (position 3) is in Howard Auditorium (1)
solver.add(loc[3] == 1)

# Exactly three of the lectures are in Gladwyn Hall
solver.add(Sum([If(loc[i] == 0, 1, 0) for i in range(5)]) == 3)

# The lecture on sandpipers (3) is in Howard Auditorium (1) and is given earlier than the lecture on oystercatchers (0)
# sandpipers in Howard
solver.add(Or([And(pos[i] == 3, loc[i] == 1) for i in range(5)]))
# sandpipers earlier than oystercatchers
solver.add(Or([And(pos[i] == 3, pos[j] == 0, i < j) for i in range(5) for j in range(5)]))

# The lecture on terns (4) is given earlier than the lecture on petrels (1), which is in Gladwyn Hall (0)
# terns earlier than petrels
solver.add(Or([And(pos[i] == 4, pos[j] == 1, i < j) for i in range(5) for j in range(5)]))
# petrels in Gladwyn Hall
solver.add(Or([And(pos[i] == 1, loc[i] == 0) for i in range(5)]))

# Now evaluate each option
# Each option gives an order from first to fifth (positions 0..4)
# We'll encode each option as a constraint on pos

bird_names = ["oystercatchers", "petrels", "rails", "sandpipers", "terns"]

# Option A: oystercatchers, petrels, rails, sandpipers, terns
# pos[0]=0, pos[1]=1, pos[2]=2, pos[3]=3, pos[4]=4
opt_a = And([pos[i] == [0,1,2,3,4][i] for i in range(5)])

# Option B: petrels, sandpipers, oystercatchers, terns, rails
# pos[0]=1, pos[1]=3, pos[2]=0, pos[3]=4, pos[4]=2
opt_b = And([pos[i] == [1,3,0,4,2][i] for i in range(5)])

# Option C: rails, sandpipers, terns, petrels, oystercatchers
# pos[0]=2, pos[1]=3, pos[2]=4, pos[3]=1, pos[4]=0
opt_c = And([pos[i] == [2,3,4,1,0][i] for i in range(5)])

# Option D: sandpipers, terns, oystercatchers, rails, petrels
# pos[0]=3, pos[1]=4, pos[2]=0, pos[3]=2, pos[4]=1
opt_d = And([pos[i] == [3,4,0,2,1][i] for i in range(5)])

# Option E: terns, petrels, sandpipers, oystercatchers, rails
# pos[0]=4, pos[1]=1, pos[2]=3, pos[3]=0, pos[4]=2
opt_e = And([pos[i] == [4,1,3,0,2][i] for i in range(5)])

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")