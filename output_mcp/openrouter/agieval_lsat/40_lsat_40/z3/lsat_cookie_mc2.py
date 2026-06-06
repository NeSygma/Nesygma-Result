from z3 import *

# Days: 0 Mon,1 Tue,2 Wed,3 Thu,4 Fri
O = [Int(f'O{i}') for i in range(1,4)]
P = [Int(f'P{i}') for i in range(1,4)]
S = [Int(f'S{i}') for i in range(1,4)]

solver = Solver()
# domain 0-4
for v in O+P+S:
    solver.add(v >= 0, v <= 4)
# No two batches of same kind same day
solver.add(Distinct(O))
solver.add(Distinct(P))
solver.add(Distinct(S))
# At least one batch on Monday (day 0)
solver.add(Or([v == 0 for v in O+P+S]))
# O2 same day as P1
solver.add(O[1] == P[0])
# S2 is Thursday (3)
solver.add(S[1] == 3)
# No batch on Wednesday (2) as per condition
for v in O+P+S:
    solver.add(v != 2)

# Option constraints
def opt_A():
    cnt = Sum([If(v == 1, 1, 0) for v in O+P+S])
    return cnt == 3

def opt_B():
    cnt = Sum([If(v == 4, 1, 0) for v in O+P+S])
    return cnt == 3

def opt_C():
    cnt = Sum([If(v == 0, 1, 0) for v in O+P+S])
    return cnt >= 2

def opt_D():
    cnt = Sum([If(v == 3, 1, 0) for v in O+P+S])
    return cnt >= 2

def opt_E():
    cnt0 = Sum([If(v == 0, 1, 0) for v in O+P+S])
    cnt1 = Sum([If(v == 1, 1, 0) for v in O+P+S])
    return cnt0 < cnt1

options = [
    ("A", opt_A()),
    ("B", opt_B()),
    ("C", opt_C()),
    ("D", opt_D()),
    ("E", opt_E()),
]

forced_options = []
for letter, constr in options:
    solver.push()
    # add negation of the option; if unsat, then option must hold
    solver.add(Not(constr))
    if solver.check() == unsat:
        forced_options.append(letter)
    solver.pop()

if len(forced_options) == 1:
    print("STATUS: sat")
    print(f"answer:{forced_options[0]}")
elif len(forced_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple forced options {forced_options}")
else:
    print("STATUS: unsat")
    print("Refine: No forced option found")