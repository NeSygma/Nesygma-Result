from z3 import *

# Define items
items = ['harmonica', 'lamp', 'mirror', 'sundial', 'table', 'vase']
# Create Int variables for day of each item
item_day = {name: Int(name) for name in items}

solver = Solver()
# Domain constraints: days 1..6
for d in item_day.values():
    solver.add(d >= 1, d <= 6)
# All days distinct
solver.add(Distinct(list(item_day.values())))

# Base constraints
# 1. sundial not on June 1
solver.add(item_day['sundial'] != 1)
# 2. If harmonica earlier than lamp, then mirror earlier than lamp
solver.add(Implies(item_day['harmonica'] < item_day['lamp'], item_day['mirror'] < item_day['lamp']))
# 3. sundial earlier than mirror and earlier than vase
solver.add(item_day['sundial'] < item_day['mirror'])
solver.add(item_day['sundial'] < item_day['vase'])
# 4. table earlier than harmonica OR earlier than vase, but not both
A = item_day['table'] < item_day['harmonica']
B = item_day['table'] < item_day['vase']
solver.add(Or(A, B))
solver.add(Not(And(A, B)))

# Define option constraints
options = {
    'A': [
        item_day['harmonica'] == 1,
        item_day['table'] == 2,
        item_day['sundial'] == 3,
        item_day['lamp'] == 4,
        item_day['vase'] == 5,
        item_day['mirror'] == 6
    ],
    'B': [
        item_day['lamp'] == 1,
        item_day['harmonica'] == 2,
        item_day['sundial'] == 3,
        item_day['mirror'] == 4,
        item_day['vase'] == 5,
        item_day['table'] == 6
    ],
    'C': [
        item_day['harmonica'] == 1,
        item_day['sundial'] == 2,
        item_day['table'] == 3,
        item_day['mirror'] == 4,
        item_day['lamp'] == 5,
        item_day['vase'] == 6
    ],
    'D': [
        item_day['sundial'] == 1,
        item_day['mirror'] == 2,
        item_day['harmonica'] == 3,
        item_day['table'] == 4,
        item_day['vase'] == 5,
        item_day['lamp'] == 6
    ],
    'E': [
        item_day['vase'] == 1,
        item_day['sundial'] == 2,
        item_day['lamp'] == 3,
        item_day['harmonica'] == 4,
        item_day['table'] == 5,
        item_day['mirror'] == 6
    ]
}

found_options = []
for letter, constr in options.items():
    solver.push()
    for c in constr:
        solver.add(c)
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