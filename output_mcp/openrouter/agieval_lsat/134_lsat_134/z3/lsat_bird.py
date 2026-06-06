from z3 import *

solver = Solver()

# Location variables for each of the 5 positions: True = Gladwyn Hall (G), False = Howard Auditorium (H)
isG = [Bool(f'isG_{i}') for i in range(5)]

# Base constraints common to all options
# 1. First lecture (position 0) is in Gladwyn Hall
solver.add(isG[0] == True)
# 2. Fourth lecture (position 3) is in Howard Auditorium
solver.add(isG[3] == False)
# 3. Exactly three lectures are in Gladwyn Hall
solver.add(Sum([If(isG[i], 1, 0) for i in range(5)]) == 3)

# Helper to create position constraints for a given ordering list
def add_order_constraints(order):
    # order is a list of bird names in positions 0..4
    # Create position variables for each bird (1-indexed positions for readability)
    pos = {}
    for idx, bird in enumerate(order):
        pos[bird] = idx + 1  # positions 1..5
    # Add constraints linking bird positions to the generic constraints
    # sandpipers earlier than oystercatchers
    solver.add(pos['sandpipers'] < pos['oystercatchers'])
    # terns earlier than petrels
    solver.add(pos['terns'] < pos['petrels'])
    # sandpipers location is Howard Auditorium (False)
    solver.add(isG[pos['sandpipers'] - 1] == False)
    # petrels location is Gladwyn Hall (True)
    solver.add(isG[pos['petrels'] - 1] == True)
    # No need to add distinctness; order list already distinct
    return pos

# Define the five answer options
options = {
    "A": ["oystercatchers", "petrels", "rails", "sandpipers", "terns"],
    "B": ["petrels", "sandpipers", "oystercatchers", "terns", "rails"],
    "C": ["rails", "sandpipers", "terns", "petrels", "oystercatchers"],
    "D": ["sandpipers", "terns", "oystercatchers", "rails", "petrels"],
    "E": ["terns", "petrels", "sandpipers", "oystercatchers", "rails"],
}

found_options = []
for letter, order in options.items():
    solver.push()
    # Add constraints specific to this ordering
    add_order_constraints(order)
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