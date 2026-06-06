from z3 import *

solver = Solver()

# Define shelf numbers: 1 = bottom, 2 = middle, 3 = top (higher number = higher shelf)
books = ['F', 'G', 'H', 'I', 'K', 'L', 'M', 'O']
book_vars = {b: Int(b) for b in books}

# Domain constraints: each book on shelf 1,2,3
for b in books:
    solver.add(1 <= book_vars[b], book_vars[b] <= 3)

# Base constraints
# I is on middle shelf
solver.add(book_vars['I'] == 2)

# K is on a higher shelf than F
solver.add(book_vars['K'] > book_vars['F'])

# O is on a higher shelf than L
solver.add(book_vars['O'] > book_vars['L'])

# F is on the same shelf as M
solver.add(book_vars['F'] == book_vars['M'])

# At least two books per shelf
def count_shelf(shelf):
    return Sum([If(book_vars[b] == shelf, 1, 0) for b in books])

c1 = count_shelf(1)  # bottom
c2 = count_shelf(2)  # middle
c3 = count_shelf(3)  # top

solver.add(c1 >= 2, c2 >= 2, c3 >= 2)

# More books on bottom shelf than top shelf
solver.add(c1 > c3)

# Total books = 8 (implicitly satisfied by domain and counts, but we can add for clarity)
solver.add(Sum([If(book_vars[b] >= 1, 1, 0) for b in books]) == 8)

# Check base satisfiability
if solver.check() != sat:
    print("STATUS: unsat")
    print("Base constraints unsatisfiable")
    exit()

# Now test each option's negation
options = [
    ("A", Not(book_vars['O'] > book_vars['M'])),
    ("B", Not(book_vars['K'] > book_vars['G'])),
    ("C", Not(book_vars['I'] > book_vars['F'])),
    ("D", Not(book_vars['G'] > book_vars['O'])),
    ("E", Not(book_vars['F'] > book_vars['L']))
]

must_true = []
for letter, neg_constr in options:
    solver.push()
    solver.add(neg_constr)
    res = solver.check()
    solver.pop()
    if res == unsat:
        must_true.append(letter)

if len(must_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_true[0]}")
elif len(must_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options must be true {must_true}")
else:
    print("STATUS: unsat")
    print("Refine: No option must be true")