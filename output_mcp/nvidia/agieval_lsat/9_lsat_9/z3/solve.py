from z3 import *

solver = Solver()

# Declare Boolean variables
FN1, FN2, FN3 = Bools('FN1 FN2 FN3')
RN1, RN2, RN3 = Bools('RN1 RN2 RN3')
FP1, FP2 = Bools('FP1 FP2')
RP = Bool('RP')

# Base constraints: select all three French novels
solver.add(FN1)
solver.add(FN2)
solver.add(FN3)

# Total selected works between 5 and 6
total = FN1 + FN2 + FN3 + RN1 + RN2 + RN3 + FP1 + FP2 + RP
solver.add(total >= 5)
solver.add(total <= 6)

# French works <= 4
solver.add(FN1 + FN2 + FN3 + FP1 + FP2 <= 4)

# Novels count between 3 and 4
solver.add(FN1 + FN2 + FN3 + RN1 + RN2 + RN3 >= 3)
solver.add(FN1 + FN2 + FN3 + RN1 + RN2 + RN3 <= 4)

# French novels >= Russian novels
solver.add(FN1 + FN2 + FN3 >= RN1 + RN2 + RN3)

# If both French plays are selected then Russian play is not selected
solver.add(Not(And(FP1, FP2, RP)))

# Helper functions for exactly one and exactly two Russian novels
def exactly_one_RN():
    return Or(
        And(RN1, Not(RN2), Not(RN3)),
        And(RN2, Not(RN1), Not(RN3)),
        And(RN3, Not(RN1), Not(RN2))
    )

def exactly_two_RN():
    return Or(
        And(RN1, RN2, Not(RN3)),
        And(RN1, RN3, Not(RN2)),
        And(RN2, RN3, Not(RN1))
    )

# Define options and their constraints
found_options = []
options = [
    ("A", [
        exactly_one_RN(),
        Not(FP1),
        Not(FP2),
        Not(RP)
    ]),
    ("B", [
        FP1,
        FP2,
        Not(RN1),
        Not(RN2),
        Not(RN3),
        Not(RP)
    ]),
    ("C", [
        exactly_one_RN(),
        RP,
        Not(FP1),
        Not(FP2)
    ]),
    ("D", [
        exactly_one_RN(),
        FP1,
        FP2,
        Not(RP)
    ]),
    ("E", [
        exactly_two_RN(),
        FP1,
        Not(FP2),
        Not(RP)
    ])
]

# Evaluate each option
for letter, constr_list in options:
    solver.push()
    for c in constr_list:
        solver.add(c)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Output according to skeleton
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")