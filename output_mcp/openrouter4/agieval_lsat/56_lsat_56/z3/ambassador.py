from z3 import *

solver = Solver()

# Candidates: 0=Jaramillo, 1=Kayne, 2=Landon, 3=Novetzke, 4=Ong
# Countries: ven=Venezuela, yem=Yemen, zam=Zambia
ven, yem, zam = Ints('ven yem zam')

# Domain: each is a candidate
solver.add(ven >= 0, ven <= 4)
solver.add(yem >= 0, yem <= 4)
solver.add(zam >= 0, zam <= 4)

# All different (one ambassador per country, no ambassador to more than one country)
solver.add(Distinct(ven, yem, zam))

# Constraint 1: Either Kayne(1) or Novetzke(3), but not both, is assigned.
# Exactly one of {1, 3} appears among the three positions.
solver.add(Sum([If(ven == 1, 1, 0), If(yem == 1, 1, 0), If(zam == 1, 1, 0),
                If(ven == 3, 1, 0), If(yem == 3, 1, 0), If(zam == 3, 1, 0)]) == 1)

# Constraint 2: If Jaramillo(0) is assigned, then Kayne(1) is assigned.
solver.add(Implies(Or(ven == 0, yem == 0, zam == 0),
                   Or(ven == 1, yem == 1, zam == 1)))

# Constraint 3: If Ong(4) is assigned as ambassador to Venezuela, Kayne(1) is not assigned as ambassador to Yemen.
solver.add(Implies(ven == 4, yem != 1))

# Constraint 4: If Landon(2) is assigned to an ambassadorship, it is to Zambia.
# Landon cannot be assigned to Venezuela or Yemen.
solver.add(ven != 2)
solver.add(yem != 2)

# Premise for the question: Ong is assigned as ambassador to Venezuela.
solver.add(ven == 4)

# Now test each option.
# Each option gives the two people assigned to Yemen and Zambia.
# We check if there exists a model where yem and zam are those two people (in some order).

options = {
    "A": (0, 2),  # Jaramillo and Landon
    "B": (0, 3),  # Jaramillo and Novetzke
    "C": (1, 2),  # Kayne and Landon
    "D": (1, 3),  # Kayne and Novetzke
    "E": (2, 3),  # Landon and Novetzke
}

found_options = []
for letter, (p1, p2) in options.items():
    solver.push()
    # The two remaining ambassadors are p1 and p2 (in some order at Yemen and Zambia)
    solver.add(Or(And(yem == p1, zam == p2), And(yem == p2, zam == p1)))
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