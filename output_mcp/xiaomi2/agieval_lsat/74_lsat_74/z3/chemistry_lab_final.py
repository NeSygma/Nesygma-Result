from z3 import *

solver = Solver()

# 6 slots: 0=WM, 1=WA, 2=TM, 3=TA, 4=FM, 5=FA
# Day = slot // 2 (0=Wed, 1=Thu, 2=Fri)
# AM/PM = slot % 2 (0=morning, 1=afternoon)

J = Int('J')  # Julio
K = Int('K')  # Kevin
L = Int('L')  # Lan
N = Int('N')  # Nessa
O = Int('O')  # Olivia
R = Int('R')  # Rebecca

assistants = [J, K, L, N, O, R]

# Each assistant assigned to a valid slot (0-5)
for a in assistants:
    solver.add(a >= 0, a <= 5)

# All different slots
solver.add(Distinct(assistants))

# Constraint 1: Kevin and Rebecca same day
solver.add(K / 2 == R / 2)

# Constraint 2: Lan and Olivia different day
solver.add(L / 2 != O / 2)

# Constraint 3: Nessa afternoon
solver.add(N % 2 == 1)

# Constraint 4: Julio earlier day than Olivia
solver.add(J / 2 < O / 2)

# Additional condition: Julio and Kevin both morning
solver.add(J % 2 == 0)
solver.add(K % 2 == 0)

# Define option constraints
options = {
    "A": L == 0,       # Lan: Wednesday morning
    "B": L == 3,       # Lan: Thursday afternoon
    "C": N == 5,       # Nessa: Friday afternoon
    "D": O == 2,       # Olivia: Thursday morning
    "E": O == 4,       # Olivia: Friday morning
}

# The question asks "could be true EXCEPT" = which one CANNOT be true
# Find options that are UNSAT (cannot be true)
impossible_options = []
possible_options = []
for letter, constr in options.items():
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        possible_options.append(letter)
    else:
        impossible_options.append(letter)
    solver.pop()

print(f"Possible options (SAT): {possible_options}")
print(f"Impossible options (UNSAT): {impossible_options}")

if len(impossible_options) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible_options[0]}")
elif len(impossible_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options found {impossible_options}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible options found")