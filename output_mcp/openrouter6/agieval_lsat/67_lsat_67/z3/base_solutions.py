from z3 import *

# Books
books = ['F', 'G', 'H', 'I', 'K', 'L', 'M', 'O']
shelf = {b: Int(f'shelf_{b}') for b in books}

solver = Solver()

# Each shelf is 0,1,2 (top, middle, bottom)
for b in books:
    solver.add(shelf[b] >= 0, shelf[b] <= 2)

# I is on middle shelf
solver.add(shelf['I'] == 1)

# F and M on same shelf
solver.add(shelf['F'] == shelf['M'])

# K higher than F (higher shelf means smaller number)
solver.add(shelf['K'] < shelf['F'])

# O higher than L
solver.add(shelf['O'] < shelf['L'])

# At least two books per shelf
for s in range(3):
    solver.add(Sum([If(shelf[b] == s, 1, 0) for b in books]) >= 2)

# Bottom shelf count > top shelf count
top_count = Sum([If(shelf[b] == 0, 1, 0) for b in books])
bottom_count = Sum([If(shelf[b] == 2, 1, 0) for b in books])
solver.add(bottom_count > top_count)

# Enumerate all solutions
solutions = []
while solver.check() == sat:
    m = solver.model()
    sol = {b: m[shelf[b]] for b in books}
    solutions.append(sol)
    # Blocking clause: at least one book has different shelf
    solver.add(Or([shelf[b] != m[shelf[b]] for b in books]))

print(f"Number of solutions to base constraints: {len(solutions)}")
for i, sol in enumerate(solutions):
    print(f"Solution {i+1}: {sol}")