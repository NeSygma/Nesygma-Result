from z3 import *

# We have 7 positions (1-7) for houses J, K, L, M, N, O, P
# Morning: positions 1,2
# Afternoon: positions 3,4,5
# Evening: positions 6,7

# We'll encode each option as a specific ordering and check if it satisfies all rules.

# Rules:
# 1. J must be shown in the evening (positions 6 or 7)
# 2. K cannot be shown in the morning (positions 1 or 2)
# 3. L must be shown at some time after K and before M (K before L before M)

# Let's define positions for each house using Int variables
houses = ['J', 'K', 'L', 'M', 'N', 'O', 'P']
pos = {h: Int(f'pos_{h}') for h in houses}

def check_option(order_list):
    """order_list is a list of 7 house letters in order from first to seventh"""
    solver = Solver()
    
    # Each house gets a unique position from 1 to 7
    for h in houses:
        solver.add(pos[h] >= 1, pos[h] <= 7)
    solver.add(Distinct([pos[h] for h in houses]))
    
    # Fix the order: position i gets the house at index i-1
    for i, h in enumerate(order_list):
        solver.add(pos[h] == i + 1)
    
    # Rule 1: J must be in evening (positions 6 or 7)
    solver.add(Or(pos['J'] == 6, pos['J'] == 7))
    
    # Rule 2: K cannot be in morning (positions 1 or 2)
    solver.add(Not(Or(pos['K'] == 1, pos['K'] == 2)))
    
    # Rule 3: L after K and before M
    solver.add(pos['K'] < pos['L'])
    solver.add(pos['L'] < pos['M'])
    
    return solver.check()

# Define each option's order
options = {
    'A': ['K', 'O', 'L', 'M', 'N', 'J', 'P'],
    'B': ['N', 'L', 'P', 'K', 'M', 'O', 'J'],
    'C': ['O', 'P', 'K', 'L', 'N', 'M', 'J'],
    'D': ['O', 'P', 'M', 'N', 'K', 'L', 'J'],
    'E': ['P', 'O', 'K', 'J', 'L', 'N', 'M']
}

found_options = []
for letter, order in options.items():
    result = check_option(order)
    if result == sat:
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