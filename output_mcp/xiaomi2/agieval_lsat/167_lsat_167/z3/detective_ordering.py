from z3 import *

solver = Solver()

# Seven accomplices, positions 1-7
Peters, Quinn, Rovero, Stanton, Tao, Villas, White = Ints('Peters Quinn Rovero Stanton Tao Villas White')
accomplices = [Peters, Quinn, Rovero, Stanton, Tao, Villas, White]

# All positions are between 1 and 7
for a in accomplices:
    solver.add(a >= 1, a <= 7)

# All different positions
solver.add(Distinct(accomplices))

# Constraint 1: Stanton neither immediately before nor immediately after Tao
solver.add(Abs(Stanton - Tao) != 1)

# Constraint 2: Quinn recruited earlier than Rovero
solver.add(Quinn < Rovero)

# Constraint 3: Villas immediately before White
solver.add(Villas + 1 == White)

# Constraint 4: Peters recruited fourth
solver.add(Peters == 4)

# Constraint 5 (additional): White immediately before Quinn
solver.add(White + 1 == Quinn)

# Now check which option MUST be at position 6
# We check each option: is it ALWAYS at position 6 across all valid models?

options = {
    "A": Quinn,
    "B": Rovero,
    "C": Stanton,
    "D": Villas,
    "E": White,
}

found_options = []
for letter, var in options.items():
    solver.push()
    solver.add(var == 6)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Also check: which options can NEVER be at position 6?
# For "must be sixth", we need: option is at 6 in ALL models
# Equivalently: the option NOT at 6 is unsat
must_be_sixth = []
for letter, var in options.items():
    solver.push()
    solver.add(var != 6)
    result = solver.check()
    if result == unsat:
        must_be_sixth.append(letter)
    solver.pop()

print(f"Options that CAN be at position 6: {found_options}")
print(f"Options that MUST be at position 6 (cannot be elsewhere): {must_be_sixth}")

if len(must_be_sixth) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_sixth[0]}")
elif len(must_be_sixth) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options must be sixth {must_be_sixth}")
else:
    print("STATUS: unsat")
    print("Refine: No option must be sixth")