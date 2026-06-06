from z3 import *

solver = Solver()

# Define variables for each work
FN = [Bool(f'FN{i}') for i in range(1,4)]  # French novels
RN = [Bool(f'RN{i}') for i in range(1,4)]  # Russian novels
FP = [Bool(f'FP{i}') for i in range(1,3)]  # French plays
RP = Bool('RP')  # Russian play

# Helper to sum boolean selections as integers

def sum_bools(lst):
    return Sum([If(b,1,0) for b in lst])

# Base constraints

total = sum_bools(FN) + sum_bools(RN) + sum_bools(FP) + If(RP,1,0)
solver.add(total >= 5, total <= 6)
solver.add(sum_bools(FN) + sum_bools(FP) <= 4)  # No more than 4 French works
solver.add(sum_bools(FN) + sum_bools(RN) >= 3, sum_bools(FN) + sum_bools(RN) <= 4)  # Novels count
solver.add(sum_bools(FN) >= sum_bools(RN))  # French novels >= Russian novels
solver.add(Or(Not(FP[0]), Not(FP[1]), Not(RP)))  # If both French plays selected, Russian play not selected

# Option constraints
opt_a_constr = And(
    sum_bools(FN) == 1,
    sum_bools(RN) == 2,
    sum_bools(FP) == 1,
    RP == True
)
opt_b_constr = And(
    sum_bools(FN) == 2,
    sum_bools(RN) == 1,
    sum_bools(FP) == 2,
    RP == True
)
opt_c_constr = And(
    sum_bools(FN) == 2,
    sum_bools(RN) == 2,
    sum_bools(FP) == 2,
    RP == False
)
opt_d_constr = And(
    sum_bools(FN) == 3,
    sum_bools(RN) == 1,
    sum_bools(FP) == 2,
    RP == False
)
opt_e_constr = And(
    sum_bools(FN) == 3,
    sum_bools(RN) == 2,
    sum_bools(FP) == 0,
    RP == True
)

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