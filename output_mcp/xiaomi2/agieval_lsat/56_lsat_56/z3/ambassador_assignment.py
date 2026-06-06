from z3 import *

solver = Solver()

# Countries: Venezuela=0, Yemen=1, Zambia=2
# Candidates: Jaramillo=0, Kayne=1, Landon=2, Novetzke=3, Ong=4

# Assignment variables: which candidate goes to each country
ven = Int('ven')  # Venezuela
yem = Int('yem')  # Yemen
zam = Int('zam')  # Zambia

# Domain: each assignment is one of the 5 candidates
for v in [ven, yem, zam]:
    solver.add(And(v >= 0, v <= 4))

# No ambassador assigned to more than one country
solver.add(Distinct(ven, yem, zam))

# Constraint 1: Exactly one of Kayne(1) or Novetzke(3) is assigned
# "Either Kayne or Novetzke, but not both, is assigned to one of the ambassadorships"
kayne_assigned = Or(ven == 1, yem == 1, zam == 1)
novetzke_assigned = Or(ven == 3, yem == 3, zam == 3)
solver.add(Xor(kayne_assigned, novetzke_assigned))

# Constraint 2: If Jaramillo is assigned, then Kayne is assigned
jaramillo_assigned = Or(ven == 0, yem == 0, zam == 0)
solver.add(Implies(jaramillo_assigned, kayne_assigned))

# Constraint 3: If Ong is assigned to Venezuela, Kayne is not assigned to Yemen
solver.add(Implies(ven == 4, yem != 1))

# Constraint 4: If Landon is assigned to an ambassadorship, it is to Zambia
landon_assigned = Or(ven == 2, yem == 2, zam == 2)
solver.add(Implies(landon_assigned, zam == 2))

# Question premise: Ong is assigned to Venezuela
solver.add(ven == 4)

# Now check each answer option
# The "other two ambassadors" are for Yemen and Zambia
# We need to check if the pair could be assigned (in either order)

candidates = {0: "Jaramillo", 1: "Kayne", 2: "Landon", 3: "Novetzke", 4: "Ong"}

options = {
    "A": (0, 2),  # Jaramillo and Landon
    "B": (0, 3),  # Jaramillo and Novetzke
    "C": (1, 2),  # Kayne and Landon
    "D": (1, 3),  # Kayne and Novetzke
    "E": (2, 3),  # Landon and Novetzke
}

found_options = []
for letter, (c1, c2) in options.items():
    solver.push()
    # The pair must be assigned to Yemen and Zambia (in some order)
    solver.add(Or(
        And(yem == c1, zam == c2),
        And(yem == c2, zam == c1)
    ))
    if solver.check() == sat:
        m = solver.model()
        found_options.append(letter)
        print(f"Option {letter} is SAT: ven={candidates[m[ven].as_long()]}, yem={candidates[m[yem].as_long()]}, zam={candidates[m[zam].as_long()]}")
    else:
        print(f"Option {letter} is UNSAT")
    solver.pop()

print()
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")