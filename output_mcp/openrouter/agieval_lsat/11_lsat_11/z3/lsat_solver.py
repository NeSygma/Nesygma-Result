from z3 import *

# Decision variables: counts of each type
FN = Int('FN')  # French novels (0-3)
RN = Int('RN')  # Russian novels (0-3)
FP = Int('FP')  # French plays (0-2)
RP = Int('RP')  # Russian play (0-1)

solver = Solver()
# Domain constraints
solver.add(FN >= 0, FN <= 3)
solver.add(RN >= 0, RN <= 3)
solver.add(FP >= 0, FP <= 2)
solver.add(RP >= 0, RP <= 1)

# Base constraints
# total works between 5 and 6
total = FN + RN + FP + RP
solver.add(total >= 5, total <= 6)
# No more than four French works
solver.add(FN + FP <= 4)
# Novels between 3 and 4
solver.add(FN + RN >= 3, FN + RN <= 4)
# At least as many French novels as Russian novels
solver.add(FN >= RN)
# If both French plays selected then Russian play not selected
solver.add(Implies(FP == 2, RP == 0))

# Helper to test an option description
def option_sat(desc):
    s = Solver()
    s.add(solver.assertions())
    s.add(desc)
    return s.check() == sat

# Define each option description as a conjunction of equalities
opt_a = And(RN == 0, (FP + RP) == 1)  # exactly one play (either French or Russian)
opt_b = And(RN == 1, FP == 2, RP == 0)
opt_c = And(FN == 2, RP == 1)  # other counts unrestricted
opt_d = And(FN == 2, (FP + RP) == 2)
opt_e = And(RN == 2, (FP + RP) == 1)

options = [
    ("A", opt_a),
    ("B", opt_b),
    ("C", opt_c),
    ("D", opt_d),
    ("E", opt_e)
]

possible = []
for letter, constr in options:
    if option_sat(constr):
        possible.append(letter)

all_letters = {letter for letter, _ in options}
impossible = all_letters - set(possible)

if len(impossible) == 1:
    ans = impossible.pop()
    print("STATUS: sat")
    print(f"answer:{ans}")
else:
    print("STATUS: unsat")
    print(f"Refine: possible={possible}, impossible={list(impossible)}")