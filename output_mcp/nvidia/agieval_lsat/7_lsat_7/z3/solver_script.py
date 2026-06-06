from z3 import *

solver = Solver()

# Declare Boolean variables
fn = [Bool('fn0'), Bool('fn1'), Bool('fn2')]  # French novels
rn = [Bool('rn0'), Bool('rn1'), Bool('rn2')]  # Russian novels
fp = [Bool('fp0'), Bool('fp1')]              # French plays
rp = Bool('rp')                              # Russian play

# Global constraints
all_vars = fn + rn + fp + [rp]
solver.add(Sum(all_vars) >= 5)
solver.add(Sum(all_vars) <= 6)
solver.add(Sum(fn + fp) <= 4)               # No more than 4 French works
solver.add(Sum(fn + rn) >= 3)               # At least 3 novels
solver.add(Sum(fn + rn) <= 4)               # At most 4 novels
solver.add(Sum(fn) >= Sum(rn))              # At least as many French novels as Russian novels
solver.add(Implies(Sum(fp) == 2, rp == False))  # If both French plays selected, Russian play not selected

# Define answer-specific constraints
opt_a_constr = [
    Sum(fn) == 1,
    Sum(rn) == 2,
    Sum(fp) == 1,
    rp == True  # one Russian play selected
]
opt_b_constr = [
    Sum(fn) == 2,
    Sum(rn) == 1,
    Sum(fp) == 2,
    rp == True
]
opt_c_constr = [
    Sum(fn) == 2,
    Sum(rn) == 2,
    Sum(fp) == 2,
    rp == False  # no Russian play
]
opt_d_constr = [
    Sum(fn) == 3,
    Sum(rn) == 1,
    Sum(fp) == 2,
    rp == False
]
opt_e_constr = [
    Sum(fn) == 3,
    Sum(rn) == 2,
    Sum(fp) == 0,
    rp == True
]

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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