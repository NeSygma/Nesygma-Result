from z3 import *

# Define variables for each accomplice
Peters = Int('Peters')
Quinn = Int('Quinn')
Rovero = Int('Rovero')
Stanton = Int('Stanton')
Tao = Int('Tao')
Villas = Int('Villas')
White = Int('White')

people = [Peters, Quinn, Rovero, Stanton, Tao, Villas, White]
solver = Solver()

# Domain constraints: positions 1..7 and all distinct
for p in people:
    solver.add(p >= 1, p <= 7)
solver.add(Distinct(people))

# Base constraints
solver.add(Peters == 4)                     # Peters recruited fourth
solver.add(Villas + 1 == White)             # Villas immediately before White
solver.add(Abs(Stanton - Tao) != 1)         # Stanton not immediately before/after Tao
solver.add(Quinn < Rovero)                  # Quinn earlier than Rovero

# Helper to build option constraint
def option_constraint(seq):
    # seq is list of (person_name, position) for positions 2..6
    mapping = {
        'Peters': Peters,
        'Quinn': Quinn,
        'Rovero': Rovero,
        'Stanton': Stanton,
        'Tao': Tao,
        'Villas': Villas,
        'White': White,
    }
    cons = []
    for name, pos in seq:
        cons.append(mapping[name] == pos)
    return And(cons)

# Define option constraints for A-E (positions 2..6)
opt_a_constr = option_constraint([
    ('Quinn', 2),
    ('Stanton', 3),
    ('Peters', 4),
    ('Tao', 5),
    ('Villas', 6)
])
opt_b_constr = option_constraint([
    ('Quinn', 2),
    ('Stanton', 3),
    ('Peters', 4),
    ('Tao', 5),
    ('White', 6)
])
opt_c_constr = option_constraint([
    ('Villas', 2),
    ('White', 3),
    ('Peters', 4),
    ('Quinn', 5),
    ('Stanton', 6)
])
opt_d_constr = option_constraint([
    ('Villas', 2),
    ('White', 3),
    ('Peters', 4),
    ('Rovero', 5),
    ('Stanton', 6)
])
opt_e_constr = option_constraint([
    ('Villas', 2),
    ('White', 3),
    ('Quinn', 4),
    ('Rovero', 5),
    ('Stanton', 6)
])

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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