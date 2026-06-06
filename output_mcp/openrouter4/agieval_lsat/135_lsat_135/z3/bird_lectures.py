from z3 import *

O, P, R, S, T = 0, 1, 2, 3, 4  # bird types

solver = Solver()

# location_at_position[p] = True for Gladwyn Hall, False for Howard Auditorium
loc = [Bool(f'loc_{p}') for p in range(5)]  # positions 0-4

# bird_at_position[p] = which bird is at position p
bird = [Int(f'bird_{p}') for p in range(5)]

# Domain constraints: each position gets a bird type 0..4
for p in range(5):
    solver.add(bird[p] >= 0, bird[p] <= 4)

# Each bird appears exactly once
solver.add(Distinct(bird))

# Constraint 1: First lecture (position 0) is in Gladwyn Hall
solver.add(loc[0] == True)

# Constraint 2: Fourth lecture (position 3) is in Howard Auditorium
solver.add(loc[3] == False)

# Constraint 3: Exactly three lectures are in Gladwyn Hall
solver.add(Sum([If(loc[p], 1, 0) for p in range(5)]) == 3)

# Constraint 4: Sandpipers in Howard, and earlier than oystercatchers
# Sandpipers (S=3) in Howard: for position p where bird[p] == S, loc[p] == False
for p in range(5):
    solver.add(Implies(bird[p] == S, loc[p] == False))

# Sandpipers earlier than oystercatchers: position_of_S < position_of_O
for pS in range(5):
    for pO in range(5):
        solver.add(Implies(And(bird[pS] == S, bird[pO] == O), pS < pO))

# Constraint 5: Terns earlier than petrels, petrels in Gladwyn
# position_of_T < position_of_P
for pT in range(5):
    for pP in range(5):
        solver.add(Implies(And(bird[pT] == T, bird[pP] == P), pT < pP))

# Petrels in Gladwyn
for p in range(5):
    solver.add(Implies(bird[p] == P, loc[p] == True))

# Now evaluate each option
# The question asks "Which must be false?" = the option that is UNSAT when added
# Option A: first and second lectures both in Gladwyn Hall
opt_a = And(loc[0] == True, loc[1] == True)

# Option B: second and third both in Howard Auditorium
opt_b = And(loc[1] == False, loc[2] == False)

# Option C: second and fifth both in Gladwyn Hall
opt_c = And(loc[1] == True, loc[4] == True)

# Option D: third and fourth both in Howard Auditorium
opt_d = And(loc[2] == False, loc[3] == False)

# Option E: third and fifth both in Gladwyn Hall
opt_e = And(loc[2] == True, loc[4] == True)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        found_options.append(letter)
        print(f"Option {letter}: SAT")
        m = solver.model()
        for p in range(5):
            print(f"  Position {p+1}: bird={m[bird[p]]}, loc={'G' if is_true(m[loc[p]]) else 'H' if not is_true(m[loc[p]]) else '?'}")
    else:
        print(f"Option {letter}: UNSAT")
    solver.pop()

print()
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")