from z3 import *

opt = Optimize()
opt.set("timeout", 120000)

n = 10
sequence = "HPHPHHPHPH"
h_positions = [i for i in range(n) if sequence[i] == 'H']
print(f"H positions (0-indexed): {h_positions}")

# Coordinates for each residue
x = [Int(f'x_{i}') for i in range(n)]
y = [Int(f'y_{i}') for i in range(n)]

# Fix first residue at origin to break symmetry
opt.add(x[0] == 0, y[0] == 0)

# Bounds: with 10 residues, max displacement from origin is 9
for i in range(n):
    opt.add(x[i] >= -9, x[i] <= 9)
    opt.add(y[i] >= -9, y[i] <= 9)

# Constraint 1: Self-avoiding walk - all positions distinct
for i in range(n):
    for j in range(i + 1, n):
        opt.add(Or(x[i] != x[j], y[i] != y[j]))

# Constraint 2: Connectivity - consecutive residues at Manhattan distance 1
for i in range(n - 1):
    dx = x[i + 1] - x[i]
    dy = y[i + 1] - y[i]
    opt.add(Or(
        And(dx == 1, dy == 0),
        And(dx == -1, dy == 0),
        And(dx == 0, dy == 1),
        And(dx == 0, dy == -1)
    ))

# Energy model: count non-sequential H-H contacts
# Each such contact contributes -1 to energy
contact = []
for idx_a in range(len(h_positions)):
    for idx_b in range(idx_a + 1, len(h_positions)):
        i = h_positions[idx_a]
        j = h_positions[idx_b]
        if abs(i - j) > 1:  # non-sequential only
            is_adj = Bool(f'contact_{i}_{j}')
            dx = x[j] - x[i]
            dy = y[j] - y[i]
            # Adjacent iff Manhattan distance == 1
            opt.add(is_adj == Or(
                And(dx == 1, dy == 0),
                And(dx == -1, dy == 0),
                And(dx == 0, dy == 1),
                And(dx == 0, dy == -1)
            ))
            contact.append(is_adj)

print(f"Total potential H-H contact pairs: {len(contact)}")

# Minimize energy = -1 * (number of contacts)
energy = -1 * Sum([If(c, 1, 0) for c in contact])
opt.minimize(energy)

result = opt.check()
if result == sat:
    m = opt.model()
    print("STATUS: sat")
    
    coords = []
    for i in range(n):
        cx = int(str(m.evaluate(x[i])))
        cy = int(str(m.evaluate(y[i])))
        coords.append([cx, cy])
    
    num_contacts = sum(1 for c in contact if is_true(m.evaluate(c)))
    print(f"Energy: {-num_contacts}")
    print(f"Number of H-H contacts: {num_contacts}")
    print(f"sequence: {sequence}")
    print(f"coordinates: {coords}")
    
    # Print residue positions
    for i in range(n):
        print(f"  Residue {i+1} ({sequence[i]}): ({coords[i][0]}, {coords[i][1]})")
    
    # Print contact details
    print("H-H contacts:")
    for idx_a in range(len(h_positions)):
        for idx_b in range(idx_a + 1, len(h_positions)):
            i = h_positions[idx_a]
            j = h_positions[idx_b]
            if abs(i - j) > 1:
                c = Bool(f'contact_{i}_{j}')
                if is_true(m.evaluate(c)):
                    print(f"  Contact: Residue {i+1}(H) - Residue {j+1}(H)")
    
    # Verify constraints
    print("\nVerification:")
    # Check self-avoiding
    all_unique = True
    for i in range(n):
        for j in range(i+1, n):
            if coords[i] == coords[j]:
                all_unique = False
                break
    print(f"  Self-avoiding: {all_unique}")
    
    # Check connectivity
    all_connected = True
    for i in range(n-1):
        mdist = abs(coords[i+1][0] - coords[i][0]) + abs(coords[i+1][1] - coords[i][1])
        if mdist != 1:
            all_connected = False
            print(f"  Bad connection: {i+1}->{i+2}, dist={mdist}")
    print(f"  All connected: {all_connected}")
    
    # Verify energy count
    manual_contacts = 0
    for idx_a in range(len(h_positions)):
        for idx_b in range(idx_a + 1, len(h_positions)):
            i = h_positions[idx_a]
            j = h_positions[idx_b]
            if abs(i - j) > 1:
                mdist = abs(coords[j][0] - coords[i][0]) + abs(coords[j][1] - coords[i][1])
                if mdist == 1:
                    manual_contacts += 1
                    print(f"  Manual contact: Residue {i+1}(H) - Residue {j+1}(H), dist={mdist}")
    print(f"  Manual contact count: {manual_contacts}")
    print(f"  Manual energy: {-manual_contacts}")
    
elif result == unsat:
    print("STATUS: unsat")
    print("No valid folding found")
else:
    print("STATUS: unknown")
    print(f"Solver returned: {result}")