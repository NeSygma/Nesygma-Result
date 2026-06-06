from z3 import *

# Create solver
solver = Solver()

# Define the 7 positions (1 to 7)
positions = [Int(f'pos_{i}') for i in range(1, 8)]

# Define the accomplices as integers for easier comparison
# We'll use: Peters=0, Quinn=1, Rovero=2, Stanton=3, Tao=4, Villas=5, White=6
accomplices = {
    'Peters': 0,
    'Quinn': 1,
    'Rovero': 2,
    'Stanton': 3,
    'Tao': 4,
    'Villas': 5,
    'White': 6
}

# Each position must contain exactly one accomplice, and each accomplice appears exactly once
# We'll use a different approach: create variables for each position that indicate which accomplice is there
pos_vars = [Int(f'p{i}') for i in range(1, 8)]  # p1, p2, ..., p7

# Each position variable must be in range 0-6 (the accomplice indices)
for i in range(7):
    solver.add(pos_vars[i] >= 0)
    solver.add(pos_vars[i] <= 6)

# All positions must have different accomplices
solver.add(Distinct(pos_vars))

# Constraint 4: Peters was recruited fourth (position 4)
# Position 4 is pos_vars[3] (since we index from 0)
solver.add(pos_vars[3] == accomplices['Peters'])

# Constraint 3: Villas was recruited immediately before White
# This means: if Villas is at position i, White is at position i+1
# We need to express this for all possible positions
for i in range(6):  # Villas can be at positions 1-6 (indices 0-5)
    solver.add(Implies(pos_vars[i] == accomplices['Villas'], 
                       pos_vars[i+1] == accomplices['White']))

# Constraint 2: Quinn was recruited earlier than Rovero
# Find positions of Quinn and Rovero
quinn_pos = Int('quinn_pos')
rovero_pos = Int('rovero_pos')

# We need to find which position has Quinn and which has Rovero
# Using Or-Loop pattern to avoid indexing with Z3 variables
solver.add(Or([pos_vars[i] == accomplices['Quinn'] for i in range(7)]))
solver.add(Or([pos_vars[i] == accomplices['Rovero'] for i in range(7)]))

# Define quinn_pos and rovero_pos based on the positions
for i in range(7):
    solver.add(Implies(pos_vars[i] == accomplices['Quinn'], quinn_pos == i+1))
    solver.add(Implies(pos_vars[i] == accomplices['Rovero'], rovero_pos == i+1))

solver.add(quinn_pos < rovero_pos)

# Constraint 1: Stanton was recruited neither immediately before nor immediately after Tao
# This means: Stanton and Tao are not adjacent
# Find positions of Stanton and Tao
stanton_pos = Int('stanton_pos')
tao_pos = Int('tao_pos')

solver.add(Or([pos_vars[i] == accomplices['Stanton'] for i in range(7)]))
solver.add(Or([pos_vars[i] == accomplices['Tao'] for i in range(7)]))

for i in range(7):
    solver.add(Implies(pos_vars[i] == accomplices['Stanton'], stanton_pos == i+1))
    solver.add(Implies(pos_vars[i] == accomplices['Tao'], tao_pos == i+1))

# Stanton and Tao are not adjacent: |stanton_pos - tao_pos| != 1
solver.add(Not(Or(stanton_pos == tao_pos + 1, stanton_pos == tao_pos - 1)))

# Now define the answer choices as constraints
# Each choice specifies the exact order from position 1 to 7

# Option A: Quinn, Tao, Stanton, Peters, Villas, White, Rovero
opt_a = And(
    pos_vars[0] == accomplices['Quinn'],
    pos_vars[1] == accomplices['Tao'],
    pos_vars[2] == accomplices['Stanton'],
    pos_vars[3] == accomplices['Peters'],
    pos_vars[4] == accomplices['Villas'],
    pos_vars[5] == accomplices['White'],
    pos_vars[6] == accomplices['Rovero']
)

# Option B: Quinn, White, Rovero, Peters, Stanton, Villas, Tao
opt_b = And(
    pos_vars[0] == accomplices['Quinn'],
    pos_vars[1] == accomplices['White'],
    pos_vars[2] == accomplices['Rovero'],
    pos_vars[3] == accomplices['Peters'],
    pos_vars[4] == accomplices['Stanton'],
    pos_vars[5] == accomplices['Villas'],
    pos_vars[6] == accomplices['Tao']
)

# Option C: Villas, White, Quinn, Stanton, Peters, Tao, Rovero
opt_c = And(
    pos_vars[0] == accomplices['Villas'],
    pos_vars[1] == accomplices['White'],
    pos_vars[2] == accomplices['Quinn'],
    pos_vars[3] == accomplices['Stanton'],
    pos_vars[4] == accomplices['Peters'],
    pos_vars[5] == accomplices['Tao'],
    pos_vars[6] == accomplices['Rovero']
)

# Option D: Villas, White, Stanton, Peters, Quinn, Tao, Rovero
opt_d = And(
    pos_vars[0] == accomplices['Villas'],
    pos_vars[1] == accomplices['White'],
    pos_vars[2] == accomplices['Stanton'],
    pos_vars[3] == accomplices['Peters'],
    pos_vars[4] == accomplices['Quinn'],
    pos_vars[5] == accomplices['Tao'],
    pos_vars[6] == accomplices['Rovero']
)

# Option E: Villas, White, Stanton, Peters, Rovero, Tao, Quinn
opt_e = And(
    pos_vars[0] == accomplices['Villas'],
    pos_vars[1] == accomplices['White'],
    pos_vars[2] == accomplices['Stanton'],
    pos_vars[3] == accomplices['Peters'],
    pos_vars[4] == accomplices['Rovero'],
    pos_vars[5] == accomplices['Tao'],
    pos_vars[6] == accomplices['Quinn']
)

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Print results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")