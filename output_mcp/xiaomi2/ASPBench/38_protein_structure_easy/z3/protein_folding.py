from z3 import *

# Problem data
sequence = "HPPHPPHH"
n = len(sequence)
is_H = [sequence[i] == 'H' for i in range(n)]

# H positions: 0, 3, 6, 7
# Non-sequential H-H pairs: (0,3), (0,6), (0,7), (3,6), (3,7), (6,7)

opt = Optimize()
opt.set("timeout", 60000)

# Coordinate variables for each residue
x = [Int(f'x_{i}') for i in range(n)]
y = [Int(f'y_{i}') for i in range(n)]

# Bound coordinates to a reasonable range
BOUND = 8
for i in range(n):
    opt.add(x[i] >= -BOUND, x[i] <= BOUND)
    opt.add(y[i] >= -BOUND, y[i] <= BOUND)

# Constraint 1: Self-avoiding walk - all coordinates distinct
for i in range(n):
    for j in range(i+1, n):
        opt.add(Or(x[i] != x[j], y[i] != y[j]))

# Constraint 2: Consecutive residues must be Manhattan distance 1 apart
for i in range(n-1):
    dx = x[i+1] - x[i]
    dy = y[i+1] - y[i]
    opt.add(Or(
        And(dx == 1, dy == 0),
        And(dx == -1, dy == 0),
        And(dx == 0, dy == 1),
        And(dx == 0, dy == -1)
    ))

# Define contact detection for non-sequential H-H pairs
# A contact exists if Manhattan distance == 1
def manhattan_one(xi, yi, xj, yj):
    """Returns Z3 Bool that is True iff Manhattan distance between (xi,yi) and (xj,yj) is 1"""
    return Or(
        And(xi - xj == 1, yi == yj),
        And(xj - xi == 1, yi == yj),
        And(xi == xj, yi - yj == 1),
        And(xi == xj, yj - yi == 1)
    )

# Build list of contact Bool variables for all non-sequential H-H pairs
contacts = []
contact_pairs = []
for i in range(n):
    for j in range(i+2, n):  # |i-j| > 1 means j >= i+2
        if is_H[i] and is_H[j]:
            c = Bool(f'contact_{i}_{j}')
            opt.add(c == manhattan_one(x[i], y[i], x[j], y[j]))
            contacts.append(c)
            contact_pairs.append((i, j))

# Energy = -1 * (number of H-H contacts)
# Minimize energy = maximize number of contacts
num_contacts = Sum([If(c, 1, 0) for c in contacts])
opt.maximize(num_contacts)

print(f"Sequence: {sequence}")
print(f"H positions: {[i for i in range(n) if is_H[i]]}")
print(f"Non-sequential H-H pairs: {contact_pairs}")
print(f"Number of potential contacts: {len(contacts)}")
print()

result = opt.check()
print(f"Solver result: {result}")

if result == sat:
    m = opt.model()
    print("STATUS: sat")
    
    # Extract coordinates
    coords = []
    for i in range(n):
        cx = m.evaluate(x[i]).as_long()
        cy = m.evaluate(y[i]).as_long()
        coords.append((cx, cy))
    
    print(f"\nCoordinates (residue index -> (x, y)):")
    for i in range(n):
        print(f"  Residue {i} ({sequence[i]}): ({coords[i][0]}, {coords[i][1]})")
    
    # Verify adjacency
    print(f"\nAdjacency verification (consecutive residues):")
    for i in range(n-1):
        mdist = abs(coords[i+1][0] - coords[i][0]) + abs(coords[i+1][1] - coords[i][1])
        print(f"  {i}->{i+1}: Manhattan distance = {mdist} {'OK' if mdist == 1 else 'FAIL'}")
    
    # Verify self-avoiding
    print(f"\nSelf-avoiding verification:")
    all_unique = len(set(coords)) == n
    print(f"  All coordinates unique: {all_unique}")
    
    # Count and report contacts
    print(f"\nH-H contacts found:")
    total_contacts = 0
    for idx, (i, j) in enumerate(contact_pairs):
        mdist = abs(coords[j][0] - coords[i][0]) + abs(coords[j][1] - coords[i][1])
        is_contact = (mdist == 1)
        if is_contact:
            total_contacts += 1
            print(f"  Residue {i} ({sequence[i]}) <-> Residue {j} ({sequence[j]}): CONTACT (distance={mdist})")
    
    energy = -total_contacts
    print(f"\nTotal H-H contacts: {total_contacts}")
    print(f"Total energy: {energy}")
    print(f"Expected optimal energy: -3")
    print(f"Achieved optimal: {'YES' if energy == -3 else 'NO'}")
    
    # Print coordinates in requested format
    print(f"\ncoordinates = {coords}")
    
elif result == unsat:
    print("STATUS: unsat")
    print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")