from z3 import *

# Define books and shelf variables (1=bottom,2=middle,3=top)
books = ['F','G','H','I','K','L','M','O']
shelf = {b: Int(f'shelf_{b}') for b in books}
solver = Solver()
# domain constraints
for b in books:
    solver.add(And(shelf[b] >= 1, shelf[b] <= 3))
# at least two books per shelf
for level in [1,2,3]:
    solver.add(Sum([If(shelf[b] == level, 1, 0) for b in books]) >= 2)
# more books on bottom than top
bottom_cnt = Sum([If(shelf[b] == 1, 1, 0) for b in books])
top_cnt = Sum([If(shelf[b] == 3, 1, 0) for b in books])
solver.add(bottom_cnt > top_cnt)
# I on middle
solver.add(shelf['I'] == 2)
# K higher than F
solver.add(shelf['K'] > shelf['F'])
# O higher than L
solver.add(shelf['O'] > shelf['L'])
# F same as M
solver.add(shelf['F'] == shelf['M'])

# Options definitions
options = {
    'A': ['F','M'],
    'B': ['F','H','M'],
    'C': ['G','H','K'],
    'D': ['F','G','M','O'],
    'E': ['G','H','L','M']
}

found_options = []
for letter, books_on_bottom in options.items():
    solver.push()
    # enforce bottom shelf exactly these books
    for b in books:
        if b in books_on_bottom:
            solver.add(shelf[b] == 1)
        else:
            solver.add(shelf[b] != 1)
    # check
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")