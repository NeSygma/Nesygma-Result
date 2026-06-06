from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Define the birds and their integer representations
# 0: oystercatchers, 1: petrels, 2: rails, 3: sandpipers, 4: terns

# Define the locations
# 0: Gladwyn Hall (G), 1: Howard Auditorium (H)

# We'll evaluate each option by constraining the order of birds and checking consistency

solver = Solver()

# Helper function to check if an option is valid
def check_option(option_name, bird_order):
    # bird_order is a list of bird values in order from first to fifth lecture
    # e.g., [0, 1, 2, 3, 4] means oystercatchers, petrels, rails, sandpipers, terns
    
    # Create position variables for each bird (to track their positions)
    pos = [Int(f'pos_{i}') for i in range(5)]  # pos[i] = position of bird i
    
    # Create location variables for each position
    location = [Int(f'loc_{i+1}') for i in range(5)]  # location[0] = position 1, location[4] = position 5
    
    # Each bird must be at exactly one position
    solver.push()
    
    # Constraint: Each bird is at a unique position (1-5)
    solver.add(Distinct(pos))
    
    # Constraint: Each position has exactly one bird
    for i in range(5):
        solver.add(Or([pos[b] == i+1 for b in range(5)]))
    
    # Constraint: The bird at each position
    for i in range(5):
        solver.add(Or([And(pos[b] == i+1, bird_order[i] == b) for b in range(5)]))
    
    # Constraint 1: First lecture (position 1) is in Gladwyn Hall
    solver.add(location[0] == 0)
    
    # Constraint 2: Fourth lecture (position 4) is in Howard Auditorium
    solver.add(location[3] == 1)
    
    # Constraint 3: Exactly three lectures are in Gladwyn Hall
    solver.add(Sum([location[i] == 0 for i in range(5)]) == 3)
    
    # Constraint 4: Sandpipers (bird 3) is in Howard Auditorium and earlier than oystercatchers (bird 0)
    # Find position of sandpipers and oystercatchers
    solver.add(Or([And(pos[3] == i+1, location[i] == 1) for i in range(5)]))
    solver.add(pos[3] < pos[0])
    
    # Constraint 5: Terns (bird 4) is earlier than petrels (bird 1), and petrels is in Gladwyn Hall
    solver.add(pos[4] < pos[1])
    solver.add(Or([And(pos[1] == i+1, location[i] == 0) for i in range(5)]))
    
    # Check if this option is satisfiable
    result = solver.check()
    solver.pop()
    
    return result == sat

# Define the options as bird orders (first to fifth)
# 0: oystercatchers, 1: petrels, 2: rails, 3: sandpipers, 4: terns

options = {
    "A": [0, 1, 2, 3, 4],  # oystercatchers, petrels, rails, sandpipers, terns
    "B": [1, 3, 0, 4, 2],  # petrels, sandpipers, oystercatchers, terns, rails
    "C": [2, 3, 4, 1, 0],  # rails, sandpipers, terns, petrels, oystercatchers
    "D": [3, 4, 0, 2, 1],  # sandpipers, terns, oystercatchers, rails, petrels
    "E": [4, 1, 3, 0, 2],  # terns, petrels, sandpipers, oystercatchers, rails
}

found_options = []
for letter, bird_order in options.items():
    if check_option(letter, bird_order):
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