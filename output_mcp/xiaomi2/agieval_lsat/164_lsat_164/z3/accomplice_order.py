from z3 import *

solver = Solver()

# Seven accomplices, positions 1-7
Peters = Int('Peters')
Quinn = Int('Quinn')
Rovero = Int('Rovero')
Stanton = Int('Stanton')
Tao = Int('Tao')
Villas = Int('Villas')
White = Int('White')

all_vars = [Peters, Quinn, Rovero, Stanton, Tao, Villas, White]
var_names = ['Peters', 'Quinn', 'Rovero', 'Stanton', 'Tao', 'Villas', 'White']

# Each position is between 1 and 7
for v in all_vars:
    solver.add(v >= 1, v <= 7)

# All distinct positions
solver.add(Distinct(all_vars))

# Constraint 1: Stanton neither immediately before nor immediately after Tao
solver.add(Abs(Stanton - Tao) != 1)

# Constraint 2: Quinn recruited earlier than Rovero
solver.add(Quinn < Rovero)

# Constraint 3: Villas recruited immediately before White
solver.add(Villas + 1 == White)

# Constraint 4: Peters recruited fourth
solver.add(Peters == 4)

# Constraint 5: Tao recruited second
solver.add(Tao == 2)

# Now test each option
found_options = []

# (A) Quinn was recruited third
opt_a = (Quinn == 3)
# (B) Rovero was recruited fifth
opt_b = (Rovero == 5)
# (C) Stanton was recruited sixth
opt_c = (Stanton == 6)
# (D) Villas was recruited sixth
opt_d = (Villas == 6)
# (E) White was recruited third
opt_e = (White == 3)

for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        m = solver.model()
        found_options.append(letter)
        print(f"Option {letter} is SAT: " + ", ".join(f"{n}={m[v]}" for v, n in zip(all_vars, var_names)))
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