from z3 import *

solver = Solver()

# Birds: oystercatchers(O), petrels(P), rails(R), sandpipers(S), terns(T)
# Positions: 1-5 (each bird assigned a unique position)
O, P, R, S, T = Ints('O P R S T')
birds = [O, P, R, S, T]

# Each bird at a distinct position 1-5
solver.add(Distinct(birds))
for b in birds:
    solver.add(b >= 1, b <= 5)

# Venue for each position: 0 = Gladwyn Hall, 1 = Howard Auditorium
# Use Z3 Array to allow symbolic indexing
venue = Array('venue', IntSort(), IntSort())

# Constraint 1: First lecture is in Gladwyn Hall
solver.add(Select(venue, 1) == 0)

# Constraint 2: Fourth lecture is in Howard Auditorium
solver.add(Select(venue, 4) == 1)

# Constraint 3: Exactly three lectures in Gladwyn Hall (positions 1-5)
solver.add(Sum([If(Select(venue, i) == 0, 1, 0) for i in range(1, 6)]) == 3)

# Constraint 4: Sandpipers in Howard Auditorium, earlier than oystercatchers
solver.add(Select(venue, S) == 1)
solver.add(S < O)

# Constraint 5: Terns earlier than petrels, petrels in Gladwyn Hall
solver.add(T < P)
solver.add(Select(venue, P) == 0)

# Define each answer choice as position assignments
# (A) oystercatchers, petrels, rails, sandpipers, terns => O=1,P=2,R=3,S=4,T=5
opt_a = And(O == 1, P == 2, R == 3, S == 4, T == 5)
# (B) petrels, sandpipers, oystercatchers, terns, rails => P=1,S=2,O=3,T=4,R=5
opt_b = And(P == 1, S == 2, O == 3, T == 4, R == 5)
# (C) rails, sandpipers, terns, petrels, oystercatchers => R=1,S=2,T=3,P=4,O=5
opt_c = And(R == 1, S == 2, T == 3, P == 4, O == 5)
# (D) sandpipers, terns, oystercatchers, rails, petrels => S=1,T=2,O=3,R=4,P=5
opt_d = And(S == 1, T == 2, O == 3, R == 4, P == 5)
# (E) terns, petrels, sandpipers, oystercatchers, rails => T=1,P=2,S=3,O=4,R=5
opt_e = And(T == 1, P == 2, S == 3, O == 4, R == 5)

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