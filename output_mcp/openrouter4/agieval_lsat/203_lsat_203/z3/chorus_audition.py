from z3 import *

solver = Solver()

# Positions 1-6 for each singer
Kammer, Lugo, Trillo, Waite, Yoshida, Zinn = Ints('Kammer Lugo Trillo Waite Yoshida Zinn')
singers = [Kammer, Lugo, Trillo, Waite, Yoshida, Zinn]

# Domain: positions 1-6
for s in singers:
    solver.add(s >= 1, s <= 6)

# All distinct positions
solver.add(Distinct(singers))

# Constraint 1: The fourth audition cannot be recorded (Kammer or Lugo)
solver.add(Kammer != 4)
solver.add(Lugo != 4)

# Constraint 2: The fifth audition must be recorded (Kammer or Lugo)
solver.add(Or(Kammer == 5, Lugo == 5))

# Constraint 3: Waite's audition must take place earlier than the two recorded auditions
solver.add(Waite < Kammer)
solver.add(Waite < Lugo)

# Constraint 4: Kammer's audition earlier than Trillo's
solver.add(Kammer < Trillo)

# Constraint 5: Zinn's audition earlier than Yoshida's
solver.add(Zinn < Yoshida)

# Now test each option for being the second audition
found_options = []
option_constraints = {
    "A": Kammer == 2,
    "B": Lugo == 2,
    "C": Trillo == 2,
    "D": Waite == 2,
    "E": Zinn == 2
}

for letter, constr in option_constraints.items():
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