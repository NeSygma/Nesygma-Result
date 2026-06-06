from z3 import *

# Books: F, G, H, I, K, L, M, O
books = ['F', 'G', 'H', 'I', 'K', 'L', 'M', 'O']
# Shelves: 0 (Top), 1 (Middle), 2 (Bottom)
# shelf[book] = 0, 1, or 2

solver = Solver()
shelf = {b: Int(f'shelf_{b}') for b in books}

# Domain constraints
for b in books:
    solver.add(shelf[b] >= 0, shelf[b] <= 2)

# Condition: At least two books on each shelf
for s in range(3):
    solver.add(Sum([If(shelf[b] == s, 1, 0) for b in books]) >= 2)

# Condition: More books on bottom than top
# Total books = 8. Let T, M, B be counts.
# T + M + B = 8
# T >= 2, M >= 2, B >= 2
# B > T
# If T=2, B can be 3 or 4.
# If T=3, B must be > 3 (impossible as M >= 2).
# So T must be 2.
solver.add(Sum([If(shelf[b] == 0, 1, 0) for b in books]) == 2)
solver.add(Sum([If(shelf[b] == 2, 1, 0) for b in books]) > Sum([If(shelf[b] == 0, 1, 0) for b in books]))

# Condition: I is on the middle shelf
solver.add(shelf['I'] == 1)

# Condition: K is on a higher shelf than F
solver.add(shelf['K'] < shelf['F'])

# Condition: O is on a higher shelf than L
solver.add(shelf['O'] < shelf['L'])

# Condition: F is on the same shelf as M
solver.add(shelf['F'] == shelf['M'])

# Question: If G is on the top shelf
solver.add(shelf['G'] == 0)

# Test each option for the middle shelf
# Options: (A)H, I (B)I, L (C)H, I, L (D)I, K, L (E)F, I, M
options = {
    "A": ["H", "I"],
    "B": ["I", "L"],
    "C": ["H", "I", "L"],
    "D": ["I", "K", "L"],
    "E": ["F", "I", "M"]
}

found_options = []
for label, books_in_middle in options.items():
    solver.push()
    # Constraint: Exactly these books are on the middle shelf
    for b in books:
        if b in books_in_middle:
            solver.add(shelf[b] == 1)
        else:
            solver.add(shelf[b] != 1)
    
    if solver.check() == sat:
        found_options.append(label)
    solver.pop()

print(f"STATUS: sat")
print(f"Valid options: {found_options}")