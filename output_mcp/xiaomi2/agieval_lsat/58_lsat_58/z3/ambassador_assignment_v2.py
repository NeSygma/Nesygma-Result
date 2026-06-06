from z3 import *

solver = Solver()

# Countries: Venezuela(0), Yemen(1), Zambia(2)
# Candidates: Jaramillo(0), Kayne(1), Landon(2), Novetzke(3), Ong(4)
ven = Int('ven')
yem = Int('yem')
zam = Int('zam')

solver.add(ven >= 0, ven <= 4)
solver.add(yem >= 0, yem <= 4)
solver.add(zam >= 0, zam <= 4)
solver.add(Distinct(ven, yem, zam))

# Constraint 1: Exactly one of Kayne(1) or Novetzke(3) is assigned
kayne_assigned = Or(ven == 1, yem == 1, zam == 1)
novetzke_assigned = Or(ven == 3, yem == 3, zam == 3)
solver.add(Or(And(kayne_assigned, Not(novetzke_assigned)),
              And(Not(kayne_assigned), novetzke_assigned)))

# Constraint 2: If Jaramillo(0) assigned, then Kayne(1) assigned
jaramillo_assigned = Or(ven == 0, yem == 0, zam == 0)
solver.add(Implies(jaramillo_assigned, kayne_assigned))

# Constraint 3: If Ong(4) to Venezuela, Kayne(1) not to Yemen
solver.add(Implies(ven == 4, yem != 1))

# Constraint 4: If Landon(2) assigned, it is to Zambia
landon_assigned = Or(ven == 2, yem == 2, zam == 2)
solver.add(Implies(landon_assigned, zam == 2))

# Answer options - which CANNOT be true (i.e., which is UNSAT?)
ong_assigned = Or(ven == 4, yem == 4, zam == 4)

options = [
    ("A", zam == 0),                    # Jaramillo to Zambia
    ("B", zam == 1),                    # Kayne to Zambia
    ("C", zam == 3),                    # Novetzke to Zambia
    ("D", Not(landon_assigned)),        # Landon not assigned
    ("E", Not(ong_assigned)),           # Ong not assigned
]

impossible_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == unsat:
        impossible_options.append(letter)
        print(f"Option {letter}: UNSAT - CANNOT be true")
    elif result == sat:
        m = solver.model()
        print(f"Option {letter}: SAT - CAN be true (ven={m[ven]}, yem={m[yem]}, zam={m[zam]})")
    else:
        print(f"Option {letter}: UNKNOWN")
    solver.pop()

print()
if len(impossible_options) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible_options[0]}")
elif len(impossible_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options {impossible_options}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible options found")