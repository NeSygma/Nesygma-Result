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

# Test each option: which ones are IMPOSSIBLE (UNSAT)?
# The question asks which CANNOT be an accurate list.
# So we test if the option is possible (SAT). The one that is UNSAT is the answer.

impossible_options = []
for letter, constr in [("A", And(S == 2, H == 3)),
                       ("B", And(S == 2, M == 3)),
                       ("C", And(S == 2, W == 3)),
                       ("D", And(W == 2, H == 3)),
                       ("E", And(W == 2, M == 3))]:
    solver.push()
    solver.add(constr)
    if solver.check() == unsat:
        impossible_options.append(letter)
    solver.pop()

if len(impossible_options) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible_options[0]}")
elif len(impossible_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options impossible {impossible_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options impossible")