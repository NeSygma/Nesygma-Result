from z3 import *

# Define the antiques and days
antiques = ['harmonica', 'lamp', 'mirror', 'sundial', 'table', 'vase']
days = [1, 2, 3, 4, 5, 6]

# Create a solver
solver = Solver()

# Create variables for each antique's day
day_of = {a: Int(f'day_{a}') for a in antiques}

# Each antique is assigned to a day between 1 and 6
for a in antiques:
    solver.add(day_of[a] >= 1, day_of[a] <= 6)

# All antiques are on different days
solver.add(Distinct([day_of[a] for a in antiques]))

# Base constraints from the problem
# 1. The sundial is not auctioned on June 1st.
solver.add(day_of['sundial'] != 1)

# 2. If the harmonica is auctioned on an earlier date than the lamp, then the mirror is also auctioned on an earlier date than the lamp.
solver.add(Implies(day_of['harmonica'] < day_of['lamp'], day_of['mirror'] < day_of['lamp']))

# 3. The sundial is auctioned on an earlier date than the mirror and also on an earlier date than the vase.
solver.add(day_of['sundial'] < day_of['mirror'])
solver.add(day_of['sundial'] < day_of['vase'])

# 4. The table is auctioned on an earlier date than the harmonica or on an earlier date than the vase, but not both.
solver.add(Xor(day_of['table'] < day_of['harmonica'], day_of['table'] < day_of['vase']))

# Define the answer choices as constraints
# Each choice is a list of antiques in order from June 1st to June 6th
choices = {
    "A": ['harmonica', 'table', 'sundial', 'lamp', 'vase', 'mirror'],
    "B": ['lamp', 'harmonica', 'sundial', 'mirror', 'vase', 'table'],
    "C": ['harmonica', 'sundial', 'table', 'mirror', 'lamp', 'vase'],
    "D": ['sundial', 'mirror', 'harmonica', 'table', 'vase', 'lamp'],
    "E": ['vase', 'sundial', 'lamp', 'harmonica', 'table', 'mirror']
}

found_options = []
for letter, order in choices.items():
    solver.push()
    # Add constraints that the antique at position i (0-indexed) is on day i+1
    for i, antique in enumerate(order):
        solver.add(day_of[antique] == i + 1)
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