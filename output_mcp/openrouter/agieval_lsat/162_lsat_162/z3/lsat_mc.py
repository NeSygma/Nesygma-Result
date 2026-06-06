from z3 import *

# Define variables for positions (1-indexed)
Peters = Int('Peters')
Quinn = Int('Quinn')
Rovero = Int('Rovero')
Stanton = Int('Stanton')
Tao = Int('Tao')
Villas = Int('Villas')
White = Int('White')

people = [Peters, Quinn, Rovero, Stanton, Tao, Villas, White]
solver = Solver()
# Domain constraints
for p in people:
    solver.add(p >= 1, p <= 7)
# All distinct
solver.add(Distinct(people))
# Base constraints
solver.add(Peters == 4)  # Peters fourth
solver.add(Villas + 1 == White)  # Villas immediately before White
solver.add(Abs(Stanton - Tao) != 1)  # not adjacent
solver.add(Quinn < Rovero)  # Quinn earlier than Rovero

# Helper to create constraint for a given ordering list
def ordering_constraint(order_list):
    # order_list is list of names in positions 1..7
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
    for idx, name in enumerate(order_list, start=1):
        cons.append(mapping[name] == idx)
    return And(cons)

# Define constraints for each option
opt_a_constr = ordering_constraint(['Quinn','Tao','Stanton','Peters','Villas','White','Rovero'])
opt_b_constr = ordering_constraint(['Quinn','White','Rovero','Peters','Stanton','Villas','Tao'])
opt_c_constr = ordering_constraint(['Villas','White','Quinn','Stanton','Peters','Tao','Rovero'])
opt_d_constr = ordering_constraint(['Villas','White','Stanton','Peters','Quinn','Tao','Rovero'])
opt_e_constr = ordering_constraint(['Villas','White','Stanton','Peters','Rovero','Tao','Quinn'])

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