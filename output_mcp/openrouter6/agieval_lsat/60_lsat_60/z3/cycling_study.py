from z3 import *

# Define bicycle codes
F, G, H, J = 0, 1, 2, 3

# Rider-day variables
R1, S1, T1, Y1 = Ints('R1 S1 T1 Y1')
R2, S2, T2, Y2 = Ints('R2 S2 T2 Y2')

solver = Solver()

# Base constraints: each rider tests a bicycle each day, within range
solver.add(R1 >= 0, R1 <= 3)
solver.add(S1 >= 0, S1 <= 3)
solver.add(T1 >= 0, T1 <= 3)
solver.add(Y1 >= 0, Y1 <= 3)
solver.add(R2 >= 0, R2 <= 3)
solver.add(S2 >= 0, S2 <= 3)
solver.add(T2 >= 0, T2 <= 3)
solver.add(Y2 >= 0, Y2 <= 3)

# Each day, all bicycles are tested exactly once (distinct riders)
solver.add(Distinct([R1, S1, T1, Y1]))
solver.add(Distinct([R2, S2, T2, Y2]))

# Each rider tests a different bicycle on day 2
solver.add(R1 != R2)
solver.add(S1 != S2)
solver.add(T1 != T2)
solver.add(Y1 != Y2)

# Condition 1: Reynaldo cannot test F
solver.add(R1 != F)
solver.add(R2 != F)

# Condition 2: Yuki cannot test J
solver.add(Y1 != J)
solver.add(Y2 != J)

# Condition 3: Theresa must be one of the testers for H
solver.add(Or(T1 == H, T2 == H))

# Condition 4: Yuki's first-day bicycle must be tested by Seamus on second day
solver.add(S2 == Y1)

# Now evaluate each answer choice
found_options = []

# Choice A
solver.push()
solver.add(S1 == F, R2 == F)   # F: Seamus, Reynaldo
solver.add(Y1 == G, S2 == G)   # G: Yuki, Seamus
solver.add(T1 == H, Y2 == H)   # H: Theresa, Yuki
solver.add(R1 == J, T2 == J)   # J: Reynaldo, Theresa
if solver.check() == sat:
    found_options.append('A')
solver.pop()

# Choice B
solver.push()
solver.add(S1 == F, Y2 == F)   # F: Seamus, Yuki
solver.add(R1 == G, T2 == G)   # G: Reynaldo, Theresa
solver.add(Y1 == H, S2 == H)   # H: Yuki, Seamus
solver.add(T1 == J, R2 == J)   # J: Theresa, Reynaldo
if solver.check() == sat:
    found_options.append('B')
solver.pop()

# Choice C
solver.push()
solver.add(Y1 == F, S2 == F)   # F: Yuki, Seamus
solver.add(S1 == G, R2 == G)   # G: Seamus, Reynaldo
solver.add(T1 == H, Y2 == H)   # H: Theresa, Yuki
solver.add(R1 == J, T2 == J)   # J: Reynaldo, Theresa
if solver.check() == sat:
    found_options.append('C')
solver.pop()

# Choice D
solver.push()
solver.add(Y1 == F, S2 == F)   # F: Yuki, Seamus
solver.add(T1 == G, R2 == G)   # G: Theresa, Reynaldo
solver.add(R1 == H, T2 == H)   # H: Reynaldo, Theresa
solver.add(S1 == J, Y2 == J)   # J: Seamus, Yuki
if solver.check() == sat:
    found_options.append('D')
solver.pop()

# Choice E
solver.push()
solver.add(Y1 == F, T2 == F)   # F: Yuki, Theresa
solver.add(S1 == G, Y2 == G)   # G: Seamus, Yuki
solver.add(T1 == H, R2 == H)   # H: Theresa, Reynaldo
solver.add(R1 == J, S2 == J)   # J: Reynaldo, Seamus
if solver.check() == sat:
    found_options.append('E')
solver.pop()

# Output result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")