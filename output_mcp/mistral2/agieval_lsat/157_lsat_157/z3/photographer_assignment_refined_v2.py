from z3 import *

solver = Solver()

# Declare symbolic variables for photographers assigned to each ceremony
# Silva University ceremony
S_Frost = Bool('S_Frost')
S_Gonzalez = Bool('S_Gonzalez')
S_Heideck = Bool('S_Heideck')
S_Knutson = Bool('S_Knutson')
S_Lai = Bool('S_Lai')
S_Mays = Bool('S_Mays')

# Thorne University ceremony
T_Frost = Bool('T_Frost')
T_Gonzalez = Bool('T_Gonzalez')
T_Heideck = Bool('T_Heideck')
T_Knutson = Bool('T_Knutson')
T_Lai = Bool('T_Lai')
T_Mays = Bool('T_Mays')

# Helper function to ensure at least two photographers are assigned to a ceremony
def at_least_two(assignments):
    return Sum(assignments) >= 2

# Constraint: At least two photographers assigned to each ceremony
solver.add(at_least_two([S_Frost, S_Gonzalez, S_Heideck, S_Knutson, S_Lai, S_Mays]))
solver.add(at_least_two([T_Frost, T_Gonzalez, T_Heideck, T_Knutson, T_Lai, T_Mays]))

# Constraint: No photographer can be assigned to both ceremonies
solver.add(Not(And(S_Frost, T_Frost)))
solver.add(Not(And(S_Gonzalez, T_Gonzalez)))
solver.add(Not(And(S_Heideck, T_Heideck)))
solver.add(Not(And(S_Knutson, T_Knutson)))
solver.add(Not(And(S_Lai, T_Lai)))
solver.add(Not(And(S_Mays, T_Mays)))

# Constraint: Frost must be assigned together with Heideck to one of the ceremonies
solver.add(Or(And(S_Frost, S_Heideck), And(T_Frost, T_Heideck)))

# Constraint: If Lai and Mays are both assigned, they must be assigned to different ceremonies
solver.add(Not(And(S_Lai, S_Mays)))
solver.add(Not(And(T_Lai, T_Mays)))

# Constraint: If Gonzalez is assigned to Silva University, then Lai must be assigned to Thorne University
solver.add(Implies(S_Gonzalez, T_Lai))

# Constraint: If Knutson is not assigned to Thorne University, then both Heideck and Mays must be assigned to it
solver.add(Implies(Not(T_Knutson), And(T_Heideck, T_Mays)))

# Base constraints for the multiple choice options
# Option A: Frost, Gonzalez, Heideck, Knutson
opt_a_constr = And(
    S_Frost == True,
    S_Gonzalez == True,
    S_Heideck == True,
    S_Knutson == True,
    S_Lai == False,
    S_Mays == False,
    T_Frost == False,
    T_Gonzalez == False,
    T_Heideck == False,
    T_Knutson == False,
    T_Lai == False,
    T_Mays == False
)

# Option B: Frost, Gonzalez, Heideck
opt_b_constr = And(
    S_Frost == True,
    S_Gonzalez == True,
    S_Heideck == True,
    S_Knutson == False,
    S_Lai == False,
    S_Mays == False,
    T_Frost == False,
    T_Gonzalez == False,
    T_Heideck == False,
    T_Knutson == True,
    T_Lai == False,
    T_Mays == True
)

# Option C: Gonzalez, Knutson
opt_c_constr = And(
    S_Frost == False,
    S_Gonzalez == True,
    S_Heideck == False,
    S_Knutson == True,
    S_Lai == False,
    S_Mays == False,
    T_Frost == False,
    T_Gonzalez == False,
    T_Heideck == True,
    T_Knutson == False,
    T_Lai == True,
    T_Mays == True
)

# Option D: Heideck, Lai
opt_d_constr = And(
    S_Frost == False,
    S_Gonzalez == False,
    S_Heideck == True,
    S_Knutson == False,
    S_Lai == True,
    S_Mays == False,
    T_Frost == False,
    T_Gonzalez == False,
    T_Heideck == False,
    T_Knutson == True,
    T_Lai == False,
    T_Mays == True
)

# Option E: Knutson, Mays
opt_e_constr = And(
    S_Frost == False,
    S_Gonzalez == False,
    S_Heideck == False,
    S_Knutson == True,
    S_Lai == False,
    S_Mays == True,
    T_Frost == False,
    T_Gonzalez == False,
    T_Heideck == True,
    T_Knutson == False,
    T_Lai == True,
    T_Mays == False
)

# Evaluate each option
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