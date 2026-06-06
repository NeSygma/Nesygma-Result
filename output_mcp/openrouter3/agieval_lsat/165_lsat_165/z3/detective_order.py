from z3 import *

# Create solver
solver = Solver()

# Define positions 1-7
positions = [Int(f'pos_{i}') for i in range(7)]  # positions[0] = position 1, etc.

# Define accomplices as integers for easier handling
Peters, Quinn, Rovero, Stanton, Tao, Villas, White = 0, 1, 2, 3, 4, 5, 6

# Each position has exactly one accomplice, and each accomplice has exactly one position
# We'll use a different approach: create variables for each accomplice's position
p_peters = Int('p_peters')
p_quinn = Int('p_quinn')
p_rovero = Int('p_rovero')
p_stanton = Int('p_stanton')
p_tao = Int('p_tao')
p_villas = Int('p_villas')
p_white = Int('p_white')

all_positions = [p_peters, p_quinn, p_rovero, p_stanton, p_tao, p_villas, p_white]

# All positions are between 1 and 7
for p in all_positions:
    solver.add(p >= 1, p <= 7)

# All positions are distinct
solver.add(Distinct(all_positions))

# Constraint 4: Peters was recruited fourth
solver.add(p_peters == 4)

# Constraint 3: Villas was recruited immediately before White
solver.add(p_villas + 1 == p_white)

# Constraint 2: Quinn was recruited earlier than Rovero
solver.add(p_quinn < p_rovero)

# Constraint 1: Stanton was recruited neither immediately before nor immediately after Tao
solver.add(Not(Or(p_stanton + 1 == p_tao, p_stanton - 1 == p_tao)))

# Additional condition: If Quinn was recruited immediately before Rovero
# We'll test this condition separately

# Now test each answer choice
# The question: "If Quinn was recruited immediately before Rovero, then Stanton CANNOT have been recruited [position]"
# We need to find which position Stanton cannot be in when Quinn is immediately before Rovero

# First, let's find all possible positions for Stanton when Quinn is immediately before Rovero
# We'll create a separate solver for this
solver_with_condition = Solver()
# Add all base constraints
for p in all_positions:
    solver_with_condition.add(p >= 1, p <= 7)
solver_with_condition.add(Distinct(all_positions))
solver_with_condition.add(p_peters == 4)
solver_with_condition.add(p_villas + 1 == p_white)
solver_with_condition.add(p_quinn < p_rovero)
solver_with_condition.add(Not(Or(p_stanton + 1 == p_tao, p_stanton - 1 == p_tao)))

# Add the condition: Quinn immediately before Rovero
solver_with_condition.add(p_quinn + 1 == p_rovero)

# Check if this condition is satisfiable
if solver_with_condition.check() == sat:
    print("Condition 'Quinn immediately before Rovero' is satisfiable")
    # Now test each answer choice
    # For each position (1-7), check if Stanton CAN be in that position
    # If Stanton CAN be in a position, then that position is NOT the answer
    # The answer is the position where Stanton CANNOT be
    
    possible_stanton_positions = []
    for pos in range(1, 8):
        s = Solver()
        # Add all base constraints
        for p in all_positions:
            s.add(p >= 1, p <= 7)
        s.add(Distinct(all_positions))
        s.add(p_peters == 4)
        s.add(p_villas + 1 == p_white)
        s.add(p_quinn < p_rovero)
        s.add(Not(Or(p_stanton + 1 == p_tao, p_stanton - 1 == p_tao)))
        s.add(p_quinn + 1 == p_rovero)  # Quinn immediately before Rovero
        s.add(p_stanton == pos)  # Stanton at this position
        
        if s.check() == sat:
            possible_stanton_positions.append(pos)
    
    print(f"Stanton can be in positions: {possible_stanton_positions}")
    
    # The answer is the position Stanton CANNOT be in
    all_positions_set = set(range(1, 8))
    impossible_positions = all_positions_set - set(possible_stanton_positions)
    print(f"Stanton cannot be in positions: {impossible_positions}")
    
    # Now test each answer choice using the exact skeleton
    found_options = []
    
    # Answer choices: (A)first (B)second (C)third (D)fifth (E)seventh
    # Position mapping: first=1, second=2, third=3, fifth=5, seventh=7
    
    # For each choice, we need to check if Stanton CANNOT be in that position
    # This means: when Quinn is immediately before Rovero, Stanton is NOT in that position
    # We need to check if it's impossible for Stanton to be in that position
    
    choices = [
        ("A", 1),  # first
        ("B", 2),  # second  
        ("C", 3),  # third
        ("D", 5),  # fifth
        ("E", 7)   # seventh
    ]
    
    for letter, pos in choices:
        # Check if Stanton CAN be in this position
        s = Solver()
        for p in all_positions:
            s.add(p >= 1, p <= 7)
        s.add(Distinct(all_positions))
        s.add(p_peters == 4)
        s.add(p_villas + 1 == p_white)
        s.add(p_quinn < p_rovero)
        s.add(Not(Or(p_stanton + 1 == p_tao, p_stanton - 1 == p_tao)))
        s.add(p_quinn + 1 == p_rovero)  # Quinn immediately before Rovero
        s.add(p_stanton == pos)  # Stanton at this position
        
        # If this is UNSAT, then Stanton CANNOT be in this position
        if s.check() == unsat:
            found_options.append(letter)
    
    if len(found_options) == 1:
        print("STATUS: sat")
        print(f"answer:{found_options[0]}")
    elif len(found_options) > 1:
        print("STATUS: unsat")
        print(f"Refine: Multiple options found {found_options}")
    else:
        print("STATUS: unsat")
        print("Refine: No options found")
        
else:
    print("Condition 'Quinn immediately before Rovero' is NOT satisfiable")
    print("STATUS: unsat")
    print("Refine: The additional condition makes the problem unsatisfiable")