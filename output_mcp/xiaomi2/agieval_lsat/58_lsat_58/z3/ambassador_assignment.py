from z3 import *

solver = Solver()

# Countries: Venezuela(0), Yemen(1), Zambia(2)
# Candidates: Jaramillo(0), Kayne(1), Landon(2), Novetzke(3), Ong(4)
ven = Int('ven')  # ambassador to Venezuela
yem = Int('yem')  # ambassador to Yemen
zam = Int('zam')  # ambassador to Zambia

# Each ambassador assigned to exactly one country (range 0-4)
solver.add(ven >= 0, ven <= 4)
solver.add(yem >= 0, yem <= 4)
solver.add(zam >= 0, zam <= 4)

# No ambassador assigned to more than one country
solver.add(Distinct(ven, yem, zam))

# Constraint 1: Exactly one of Kayne(1) or Novetzke(3) is assigned (XOR)
kayne_assigned = Or(ven == 1, yem == 1, zam == 1)
novetzke_assigned = Or(ven == 3, yem == 3, zam == 3)
solver.add(Or(And(kayne_assigned, Not(novetzke_assigned)),
              And(Not(kayne_assigned), novetzke_assigned)))

# Constraint 2: If Jaramillo(0) is assigned, then Kayne(1) is assigned
jaramillo_assigned = Or(ven == 0, yem == 0, zam == 0)
solver.add(Implies(jaramillo_assigned, kayne_assigned))

# Constraint 3: If Ong(4) is assigned to Venezuela, Kayne(1) is not assigned to Yemen
solver.add(Implies(ven == 4, yem != 1))

# Constraint 4: If Landon(2) is assigned, it is to Zambia
landon_assigned = Or(ven == 2, yem == 2, zam == 2)
solver.add(Implies(landon_assigned, zam == 2))

# Define the answer options
# (A) Jaramillo is assigned to Zambia
opt_a = (zam == 0)
# (B) Kayne is assigned to Zambia
opt_b = (zam == 1)
# (C) Novetzke is assigned to Zambia
opt_c = (zam == 3)
# (D) Landon is not assigned to an ambassadorship
opt_d = Not(landon_assigned)
# (E) Ong is not assigned to an ambassadorship
ong_assigned = Or(ven == 4, yem == 4, zam == 4)
opt_e = Not(ong_assigned)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} is SAT: ven={m[ven]}, yem={m[yem]}, zam={m[zam]}")
    else:
        print(f"Option {letter} is UNSAT (CANNOT be true)")
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