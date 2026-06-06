from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare symbolic variables for each witness's testimony day
# 0: Monday, 1: Tuesday, 2: Wednesday
franco = Int('franco')
garcia = Int('garcia')
hong = Int('hong')
iturbe = Int('iturbe')
jackson = Int('jackson')

# Base constraints
solver = Solver()

# Each witness testifies on exactly one day
solver.add(franco >= 0, franco <= 2)
solver.add(garcia >= 0, garcia <= 2)
solver.add(hong >= 0, hong <= 2)
solver.add(iturbe >= 0, iturbe <= 2)
solver.add(jackson >= 0, jackson <= 2)

# Iturbe testifies on Wednesday (2)
solver.add(iturbe == 2)

# Exactly two witnesses testify on Tuesday (1)
solver.add(Sum([If(franco == 1, 1, 0),
                If(garcia == 1, 1, 0),
                If(hong == 1, 1, 0),
                If(iturbe == 1, 1, 0),
                If(jackson == 1, 1, 0)]) == 2)

# Hong does not testify on Monday (0)
solver.add(hong != 0)

# At least one witness testifies on Monday (0)
solver.add(Sum([If(franco == 0, 1, 0),
                If(garcia == 0, 1, 0),
                If(hong == 0, 1, 0),
                If(iturbe == 0, 1, 0),
                If(jackson == 0, 1, 0)]) >= 1)

# Franco does not testify on the same day as Garcia
solver.add(franco != garcia)

# Option constraints
# (A) Franco is the only witness scheduled to testify on Monday.
opt_a = And(
    franco == 0,
    garcia != 0,
    hong != 0,
    jackson != 0,
    Sum([If(franco == 0, 1, 0),
        If(garcia == 0, 1, 0),
        If(hong == 0, 1, 0),
        If(iturbe == 0, 1, 0),
        If(jackson == 0, 1, 0)]) == 1
)

# (B) Franco is scheduled to testify on the same day as Iturbe.
opt_b = (franco == iturbe)

# (C) Garcia and Hong are both scheduled to testify on Tuesday.
opt_c = And(garcia == 1, hong == 1)

# (D) Garcia is the only witness scheduled to testify on Monday and Hong is one of two witnesses scheduled to testify on Wednesday.
opt_d = And(
    garcia == 0,
    Sum([If(franco == 0, 1, 0),
        If(garcia == 0, 1, 0),
        If(hong == 0, 1, 0),
        If(iturbe == 0, 1, 0),
        If(jackson == 0, 1, 0)]) == 1,
    Sum([If(franco == 2, 1, 0),
        If(garcia == 2, 1, 0),
        If(hong == 2, 1, 0),
        If(iturbe == 2, 1, 0),
        If(jackson == 2, 1, 0)]) == 2,
    hong == 2
)

# (E) Jackson is scheduled to testify on Tuesday and two witnesses are scheduled to testify on Monday.
opt_e = And(
    jackson == 1,
    Sum([If(franco == 0, 1, 0),
        If(garcia == 0, 1, 0),
        If(hong == 0, 1, 0),
        If(iturbe == 0, 1, 0),
        If(jackson == 0, 1, 0)]) == 2
)

# Evaluate each option
cannot_be_true = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == unsat:
        cannot_be_true.append(letter)
    solver.pop()

if len(cannot_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{cannot_be_true[0]}")
elif len(cannot_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options cannot be true {cannot_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No options cannot be true (all options are satisfiable)")