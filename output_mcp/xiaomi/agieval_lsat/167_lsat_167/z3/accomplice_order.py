from z3 import *

solver = Solver()

# Seven accomplices: Peters, Quinn, Rovero, Stanton, Tao, Villas, White
# Positions 1-7
Peters = Int('Peters')
Quinn = Int('Quinn')
Rovero = Int('Rovero')
Stanton = Int('Stanton')
Tao = Int('Tao')
Villas = Int('Villas')
White = Int('White')

people = [Peters, Quinn, Rovero, Stanton, Tao, Villas, White]

# Each person has a unique position 1-7
for p in people:
    solver.add(p >= 1, p <= 7)
solver.add(Distinct(people))

# Constraint 1: Stanton was recruited neither immediately before nor immediately after Tao
solver.add(Stanton != Tao + 1)
solver.add(Stanton != Tao - 1)

# Constraint 2: Quinn was recruited earlier than Rovero
solver.add(Quinn < Rovero)

# Constraint 3: Villas was recruited immediately before White
solver.add(Villas + 1 == White)

# Constraint 4: Peters was recruited fourth
solver.add(Peters == 4)

# Constraint 5: White was recruited immediately before Quinn
solver.add(White + 1 == Quinn)

# Now check which person must be in position 6
# We test each option: the person is in position 6 in ALL valid solutions

options = {
    "A": Quinn,
    "B": Rovero,
    "C": Stanton,
    "D": Villas,
    "E": White
}

found_options = []
for letter, person in options.items():
    solver.push()
    solver.add(person == 6)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Now check which MUST be 6 (i.e., which cannot NOT be 6)
must_be_sixth = []
for letter, person in options.items():
    solver.push()
    solver.add(person != 6)
    if solver.check() == unsat:
        must_be_sixth.append(letter)
    solver.pop()

print(f"Options that CAN be 6th: {found_options}")
print(f"Options that MUST be 6th: {must_be_sixth}")

if len(must_be_sixth) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_sixth[0]}")
elif len(must_be_sixth) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options must be 6th {must_be_sixth}")
else:
    print("STATUS: unsat")
    print("Refine: No option must be 6th")