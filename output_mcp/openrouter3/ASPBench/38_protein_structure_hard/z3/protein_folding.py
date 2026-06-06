from z3 import *

# Protein sequence: HPHPHHPHPH (10 residues)
sequence = "HPHPHHPHPH"
N = len(sequence)  # 10

# Create solver
solver = Solver()

# Declare coordinate variables for each residue
x = [Int(f'x_{i}') for i in range(N)]
y = [Int(f'y_{i}') for i in range(N)]

# Energy variable
energy = Int('energy')

# 1. Self-avoiding walk: All coordinates must be distinct
# For each pair (i, j) where i < j, coordinates must differ
for i in range(N):
    for j in range(i+1, N):
        solver.add(Or(x[i] != x[j], y[i] != y[j]))

# 2. Connectivity: Consecutive residues must be adjacent (Manhattan distance = 1)
for i in range(N-1):
    # Manhattan distance = |x[i] - x[i+1]| + |y[i] - y[i+1]| = 1
    solver.add(Abs(x[i] - x[i+1]) + Abs(y[i] - y[i+1]) == 1)

# 3. Energy calculation: Only non-sequential H-H pairs contribute -1 each
# First, identify H positions
H_positions = [i for i, residue in enumerate(sequence) if residue == 'H']
print(f"H positions: {H_positions}")

# Calculate energy as negative count of non-sequential H-H contacts
# For each pair of H residues (i, j) where |i - j| > 1 and they are adjacent
contact_terms = []
for i in range(N):
    for j in range(i+1, N):
        if sequence[i] == 'H' and sequence[j] == 'H':
            # Check if non-sequential
            if abs(i - j) > 1:
                # Check if adjacent (Manhattan distance = 1)
                is_adjacent = And(
                    Abs(x[i] - x[j]) + Abs(y[i] - y[j]) == 1
                )
                # If adjacent, contributes -1 to energy
                # We'll use a boolean variable to track this contact
                contact = Bool(f'contact_{i}_{j}')
                solver.add(contact == is_adjacent)
                contact_terms.append(contact)

# Energy = - (number of H-H contacts)
# We need to count how many contact_terms are true
# Use If expressions to count
contact_count = Sum([If(contact_terms[k], 1, 0) for k in range(len(contact_terms))])
solver.add(energy == -contact_count)

# 4. Objective: Minimize energy (which means maximize contact_count)
# Since we want minimum energy (most negative), we can maximize contact_count
# We'll use a two-step approach: first find maximum possible contacts, then find a configuration with that many contacts

# Step 1: Find maximum possible contacts
opt = Optimize()
opt.add(solver.assertions())  # Add all constraints from solver
opt.maximize(contact_count)

print("Finding maximum possible contacts...")
result = opt.check()
if result == sat:
    max_contacts = opt.model().eval(contact_count)
    print(f"Maximum contacts found: {max_contacts}")
    print(f"Minimum energy: {-max_contacts}")
    
    # Step 2: Find a configuration with exactly max_contacts contacts
    solver2 = Solver()
    solver2.add(solver.assertions())
    solver2.add(contact_count == max_contacts)
    
    result2 = solver2.check()
    if result2 == sat:
        model = solver2.model()
        print("\nSTATUS: sat")
        print("Solution found!")
        
        # Extract coordinates
        coordinates = []
        for i in range(N):
            x_val = model[x[i]].as_long()
            y_val = model[y[i]].as_long()
            coordinates.append([x_val, y_val])
            print(f"Residue {i+1} ({sequence[i]}): ({x_val}, {y_val})")
        
        # Verify energy calculation
        actual_energy = 0
        for i in range(N):
            for j in range(i+1, N):
                if sequence[i] == 'H' and sequence[j] == 'H' and abs(i - j) > 1:
                    x_i = model[x[i]].as_long()
                    y_i = model[y[i]].as_long()
                    x_j = model[x[j]].as_long()
                    y_j = model[y[j]].as_long()
                    if abs(x_i - x_j) + abs(y_i - y_j) == 1:
                        actual_energy -= 1
        
        print(f"\nActual energy: {actual_energy}")
        print(f"Expected minimum energy: -4")
        
        # Print in required format
        print(f"\nsequence: {sequence}")
        print(f"coordinates: {coordinates}")
        
        # Check if we achieved the expected minimum
        if actual_energy == -4:
            print("\n✓ Achieved expected minimum energy of -4")
        else:
            print(f"\n✗ Did not achieve expected minimum energy. Got {actual_energy} instead of -4")
    else:
        print("STATUS: unsat")
        print("Could not find configuration with maximum contacts")
else:
    print("STATUS: unknown")
    print("Could not determine maximum contacts")