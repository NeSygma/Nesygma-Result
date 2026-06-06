from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare symbolic variables for photographers in each section
# 0: Fuentes, 1: Gagnon, 2: Hue
L0, L1 = Ints('L0 L1')  # Lifestyle section
M0, M1 = Ints('M0 M1')  # Metro section
S0, S1 = Ints('S0 S1')  # Sports section

# Photographer totals
Fuentes_total = Sum([If(L0 == 0, 1, 0), If(L1 == 0, 1, 0), 
                     If(M0 == 0, 1, 0), If(M1 == 0, 1, 0), 
                     If(S0 == 0, 1, 0), If(S1 == 0, 1, 0)])
Gagnon_total = Sum([If(L0 == 1, 1, 0), If(L1 == 1, 1, 0), 
                    If(M0 == 1, 1, 0), If(M1 == 1, 1, 0), 
                    If(S0 == 1, 1, 0), If(S1 == 1, 1, 0)])
Hue_total = Sum([If(L0 == 2, 1, 0), If(L1 == 2, 1, 0), 
                 If(M0 == 2, 1, 0), If(M1 == 2, 1, 0), 
                 If(S0 == 2, 1, 0), If(S1 == 2, 1, 0)])

# Hue in Lifestyle
Hue_in_Lifestyle = Sum([If(L0 == 2, 1, 0), If(L1 == 2, 1, 0)])

# Fuentes in Sports
Fuentes_in_Sports = Sum([If(S0 == 0, 1, 0), If(S1 == 0, 1, 0)])

# Base constraints
solver = Solver()

# Each photographer must have at least 1 and at most 3 photographs
solver.add(Fuentes_total >= 1, Fuentes_total <= 3)
solver.add(Gagnon_total >= 1, Gagnon_total <= 3)
solver.add(Hue_total >= 1, Hue_total <= 3)

# At least one photograph in Lifestyle must be by a photographer who has at least one photograph in Metro
# This means: there exists a photographer p such that p is in Lifestyle and p is in Metro
solver.add(Or(
    And(L0 == 0, Or(M0 == 0, M1 == 0)),
    And(L1 == 0, Or(M0 == 0, M1 == 0)),
    And(L0 == 1, Or(M0 == 1, M1 == 1)),
    And(L1 == 1, Or(M0 == 1, M1 == 1)),
    And(L0 == 2, Or(M0 == 2, M1 == 2)),
    And(L1 == 2, Or(M0 == 2, M1 == 2))
))

# Number of Hue's photographs in Lifestyle must equal number of Fuentes' photographs in Sports
solver.add(Hue_in_Lifestyle == Fuentes_in_Sports)

# None of Gagnon's photographs can be in the Sports section
solver.add(S0 != 1)
solver.add(S1 != 1)

# Define the answer choice constraints

def opt_a_constr():
    # (A) Both photographs in the Lifestyle section are by Hue
    return And(L0 == 2, L1 == 2)

def opt_b_constr():
    # (B) One photograph in the Lifestyle section is by Fuentes and one is by Hue
    return Or(
        And(L0 == 0, L1 == 2),
        And(L0 == 2, L1 == 0)
    )

def opt_c_constr():
    # (C) Both photographs in the Metro section are by Fuentes
    return And(M0 == 0, M1 == 0)

def opt_d_constr():
    # (D) One photograph in the Metro section is by Gagnon and one is by Hue
    return Or(
        And(M0 == 1, M1 == 2),
        And(M0 == 2, M1 == 1)
    )

def opt_e_constr():
    # (E) Both photographs in the Sports section are by Hue
    return And(S0 == 2, S1 == 2)

# Evaluate each option under the condition that one section has both photographs by Gagnon
found_options = []

# Test each option with the additional constraint that one section has both photographs by Gagnon
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    # Possibility 1: Both Lifestyle photographs are by Gagnon
    solver.push()
    solver.add(And(L0 == 1, L1 == 1))
    solver.add(constr())
    if solver.check() == sat:
        found_options.append(letter)
        solver.pop()
        break
    solver.pop()
    
    # Possibility 2: Both Metro photographs are by Gagnon
    solver.push()
    solver.add(And(M0 == 1, M1 == 1))
    solver.add(constr())
    if solver.check() == sat:
        found_options.append(letter)
        solver.pop()
        break
    solver.pop()
    
    # Possibility 3: Both Sports photographs are by Gagnon
    solver.push()
    solver.add(And(S0 == 1, S1 == 1))
    solver.add(constr())
    if solver.check() == sat:
        found_options.append(letter)
        solver.pop()
        break
    solver.pop()
    
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