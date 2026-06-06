from z3 import *

solver = Solver()

# Slots: 0=(screen1, 7PM), 1=(screen1, 9PM), 2=(screen2, 7PM), 3=(screen2, 9PM), 4=(screen3, 8PM)
# Movies: H=horror, M=mystery, R=romance, S=sci-fi, W=western

H, M, R, S, W = Ints('H M R S W')

# Each movie in one of the 5 slots
movies = [H, M, R, S, W]
for m in movies:
    solver.add(m >= 0, m <= 4)

# All different - each slot gets exactly one movie
solver.add(Distinct(movies))

# Helper: time value (0=7PM, 1=8PM, 2=9PM)
time_of = lambda s: If(s == 4, 1, If(Or(s == 1, s == 3), 2, 0))
# Helper: screen number (1, 2, or 3)
screen_of = lambda s: If(Or(s == 0, s == 1), 1, If(Or(s == 2, s == 3), 2, 3))

# Constraint 1: Western begins before horror (time(W) < time(H))
solver.add(time_of(W) < time_of(H))

# Constraint 2: Sci-fi not on screen 3
solver.add(S != 4)

# Constraint 3: Romance not on screen 2 (slots 2 and 3)
solver.add(R != 2)
solver.add(R != 3)

# Constraint 4: Horror and mystery on different screens
solver.add(screen_of(H) != screen_of(M))

# Now test each option for screen 2 (slot 2 = 7PM, slot 3 = 9PM)
found_options = []

# Option A: sci-fi at 7PM, horror at 9PM
solver.push()
solver.add(And(S == 2, H == 3))
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: sci-fi at 7PM, mystery at 9PM
solver.push()
solver.add(And(S == 2, M == 3))
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: sci-fi at 7PM, western at 9PM
solver.push()
solver.add(And(S == 2, W == 3))
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: western at 7PM, horror at 9PM
solver.push()
solver.add(And(W == 2, H == 3))
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: western at 7PM, mystery at 9PM
solver.push()
solver.add(And(W == 2, M == 3))
if solver.check() == sat:
    found_options.append("E")
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