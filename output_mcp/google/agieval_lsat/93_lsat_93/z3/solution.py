from z3 import *

# Houses: J, K, L, M, N, O, P
houses = ['J', 'K', 'L', 'M', 'N', 'O', 'P']
# Positions: 1, 2, 3, 4, 5, 6, 7

def check_order(order):
    # order is a list of house names in order of position 1 to 7
    pos = {house: i + 1 for i, house in enumerate(order)}
    
    # Rule 1: J must be shown in the evening (6 or 7)
    rule1 = (pos['J'] == 6 or pos['J'] == 7)
    
    # Rule 2: K cannot be shown in the morning (K > 2)
    rule2 = (pos['K'] > 2)
    
    # Rule 3: L must be shown after K and before M (K < L < M)
    rule3 = (pos['K'] < pos['L'] and pos['L'] < pos['M'])
    
    return rule1 and rule2 and rule3

# Define options
options = {
    "A": ["K", "O", "L", "M", "N", "J", "P"],
    "B": ["N", "L", "P", "K", "M", "O", "J"],
    "C": ["O", "P", "K", "L", "N", "M", "J"],
    "D": ["O", "P", "M", "N", "K", "L", "J"],
    "E": ["P", "O", "K", "J", "L", "N", "M"]
}

# Use the required skeleton
solver = Solver()

found_options = []
for letter, order in options.items():
    # We don't need to add constraints to the solver for these specific options,
    # we can just check them directly as they are fully specified.
    if check_order(order):
        found_options.append(letter)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")