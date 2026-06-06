from z3 import *

# Define accomplice constants
Peters = 0
Quinn = 1
Rovero = 2
Stanton = 3
Tao = 4
Villas = 5
White = 6

# Create a solver
solver = Solver()

# Declare the sequence of 7 accomplices (positions 0 to 6)
seq = [Int(f'seq_{i}') for i in range(7)]

# Each position must be assigned one of the accomplices
accomplices = [Peters, Quinn, Rovero, Stanton, Tao, Villas, White]
solver.add(Distinct(seq))
for i in range(7):
    solver.add(Or([seq[i] == a for a in accomplices]))

# Constraint 1: Peters was recruited fourth (index 3)
solver.add(seq[3] == Peters)

# Constraint 2: Villas was recruited immediately before White
# There exists an index i such that seq[i] == Villas and seq[i+1] == White
solver.add(Or([And(seq[i] == Villas, seq[i+1] == White) for i in range(6)]))

# Constraint 3: Quinn was recruited earlier than Rovero
# There exist indices i < j such that seq[i] == Quinn and seq[j] == Rovero
solver.add(Or([And(seq[i] == Quinn, seq[j] == Rovero) for i in range(7) for j in range(i+1, 7)]))

# Constraint 4: Stanton was recruited neither immediately before nor immediately after Tao
# For all i from 0 to 5, not (seq[i] == Stanton and seq[i+1] == Tao) and not (seq[i] == Tao and seq[i+1] == Stanton)
for i in range(6):
    solver.add(Not(And(seq[i] == Stanton, seq[i+1] == Tao)))
    solver.add(Not(And(seq[i] == Tao, seq[i+1] == Stanton)))

# Now evaluate the multiple-choice options
# Each option specifies the middle five accomplices (positions 1 to 5, 0-indexed)
# We will check if the option is consistent with the constraints

# Helper function to create constraints for an option
def option_constraints(option_name, middle_five):
    # middle_five is a list of 5 accomplices in order for positions 1 to 5
    constraints = []
    for idx, accomplice in enumerate(middle_five):
        pos = 1 + idx  # position in 0-indexed (1 to 5)
        constraints.append(seq[pos] == accomplice)
    return constraints

# Define the options as tuples of accomplice lists for positions 1 to 5
# Using the constants defined above
options = [
    ("A", [Quinn, Stanton, Peters, Tao, Villas]),
    ("B", [Quinn, Stanton, Peters, Tao, White]),
    ("C", [Villas, White, Peters, Quinn, Stanton]),
    ("D", [Villas, White, Peters, Rovero, Stanton]),
    ("E", [Villas, White, Quinn, Rovero, Stanton])
]

found_options = []
for letter, middle_five in options:
    solver.push()
    # Add the option's constraints for positions 1 to 5
    for constr in option_constraints(letter, middle_five):
        solver.add(constr)
    # Check satisfiability
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Output the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")