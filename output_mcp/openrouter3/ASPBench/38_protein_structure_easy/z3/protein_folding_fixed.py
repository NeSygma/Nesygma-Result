from z3 import *

# Protein sequence: HPPHPPHH
sequence = ['H', 'P', 'P', 'H', 'P', 'P', 'H', 'H']
N = len(sequence)  # 8 residues

# Create solver with optimization
opt = Optimize()

# Declare coordinate variables for each residue
x = [Int(f'x_{i}') for i in range(N)]
y = [Int(f'y_{i}') for i in range(N)]

# Constraint 1: Self-avoiding walk - all coordinates distinct
# For each pair (i, j) where i < j, coordinates must differ
for i in range(N):
    for j in range(i+1, N):
        opt.add(Or(x[i] != x[j], y[i] != y[j]))

# Constraint 2: Consecutive residues must be adjacent (Manhattan distance = 1)
for i in range(N-1):
    opt.add(Abs(x[i] - x[i+1]) + Abs(y[i] - y[i+1]) == 1)

# Objective: Minimize energy (maximize H-H contacts)
# Energy = - (number of H-H contacts between non-sequential neighbors)
energy_terms = []

# For each pair (i, j) where i < j and j ≠ i+1 (non-sequential)
for i in range(N):
    for j in range(i+1, N):
        if j != i+1:  # non-sequential
            # Check if both are H
            if sequence[i] == 'H' and sequence[j] == 'H':
                # Check if adjacent (Manhattan distance = 1)
                is_adjacent = (Abs(x[i] - x[j]) + Abs(y[i] - y[j]) == 1)
                # If adjacent, contributes -1 to energy (so +1 to contact count)
                # We'll maximize contact count, then negate for energy
                contact = If(is_adjacent, 1, 0)
                energy_terms.append(contact)

# Total contacts = sum of all H-H adjacent pairs
total_contacts = Sum(energy_terms)

# Minimize energy = -total_contacts
# So maximize total_contacts
opt.maximize(total_contacts)

# Check and print results
BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    print("\nOptimal solution found:")
    contacts_val = model.eval(total_contacts)
    print(f"Total H-H contacts: {contacts_val}")
    print(f"Energy: {-contacts_val}")
    print("\nCoordinates (x, y) for each residue:")
    for i in range(N):
        x_val = model.eval(x[i])
        y_val = model.eval(y[i])
        print(f"Residue {i} ({sequence[i]}): ({x_val}, {y_val})")
    
    # Verify constraints
    print("\nVerification:")
    # Check consecutive adjacency
    for i in range(N-1):
        x1 = model.eval(x[i])
        y1 = model.eval(y[i])
        x2 = model.eval(x[i+1])
        y2 = model.eval(y[i+1])
        # Convert to Python integers for calculation
        x1_int = int(str(x1))
        y1_int = int(str(y1))
        x2_int = int(str(x2))
        y2_int = int(str(y2))
        dist = abs(x1_int - x2_int) + abs(y1_int - y2_int)
        print(f"Distance between {i} and {i+1}: {dist}")
    
    # Check H-H contacts
    print("\nH-H contacts (non-sequential):")
    contact_count = 0
    for i in range(N):
        for j in range(i+1, N):
            if j != i+1 and sequence[i] == 'H' and sequence[j] == 'H':
                x1 = model.eval(x[i])
                y1 = model.eval(y[i])
                x2 = model.eval(x[j])
                y2 = model.eval(y[j])
                # Convert to Python integers
                x1_int = int(str(x1))
                y1_int = int(str(y1))
                x2_int = int(str(x2))
                y2_int = int(str(y2))
                dist = abs(x1_int - x2_int) + abs(y1_int - y2_int)
                if dist == 1:
                    contact_count += 1
                    print(f"  Contact between {i} and {j}: distance = {dist}")
    print(f"Total verified contacts: {contact_count}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")