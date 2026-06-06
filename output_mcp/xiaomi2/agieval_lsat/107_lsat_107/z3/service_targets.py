from z3 import *

# Define variables for each client's website and voicemail targets
# Clients: Image (I), Solide (S), Truvest (T)
# Each target is 1, 2, or 3 days
IW = Int('IW')  # Image website
IV = Int('IV')  # Image voicemail
SW = Int('SW')  # Solide website
SV = Int('SV')  # Solide voicemail
TW = Int('TW')  # Truvest website
TV = Int('TV')  # Truvest voicemail

all_vars = [IW, IV, SW, SV, TW, TV]

def add_base_constraints(solver):
    # Domain: each target is 1, 2, or 3
    for v in all_vars:
        solver.add(And(v >= 1, v <= 3))
    
    # Constraint 1: Website target <= voicemail target for each client
    solver.add(IW <= IV)
    solver.add(SW <= SV)
    solver.add(TW <= TV)
    
    # Constraint 2: Image's voicemail target is shorter than others' voicemail targets
    solver.add(IV < SV)
    solver.add(IV < TV)
    
    # Constraint 3: Solide's website target is shorter than Truvest's website target
    solver.add(SW < TW)

# For each option, check if that target can be set for 2 or more clients
# If it CANNOT (unsat for 2+ clients), that's the answer

options = {
    "A": "1-day website target",
    "B": "2-day voicemail target",
    "C": "2-day website target",
    "D": "3-day voicemail target",
    "E": "3-day website target",
}

# Option A: Can 2+ clients have website target = 1?
# Check: at least 2 of {IW, SW, TW} == 1
def check_two_plus_website(solver, val):
    """Check if at least 2 clients can have website target = val"""
    solver.push()
    # At least 2 of the three website targets equal val
    solver.add(Or(
        And(IW == val, SW == val),
        And(IW == val, TW == val),
        And(SW == val, TW == val)
    ))
    result = solver.check()
    solver.pop()
    return result == sat

def check_two_plus_voicemail(solver, val):
    """Check if at least 2 clients can have voicemail target = val"""
    solver.push()
    solver.add(Or(
        And(IV == val, SV == val),
        And(IV == val, TV == val),
        And(SV == val, TV == val)
    ))
    result = solver.check()
    solver.pop()
    return result == sat

solver = Solver()
add_base_constraints(solver)

results = {}

# A: 1-day website target for 2+ clients
results['A'] = check_two_plus_website(solver, 1)

# B: 2-day voicemail target for 2+ clients
results['B'] = check_two_plus_voicemail(solver, 2)

# C: 2-day website target for 2+ clients
results['C'] = check_two_plus_website(solver, 2)

# D: 3-day voicemail target for 2+ clients
results['D'] = check_two_plus_voicemail(solver, 3)

# E: 3-day website target for 2+ clients
results['E'] = check_two_plus_website(solver, 3)

print("Can be set for 2+ clients:")
for letter in ['A', 'B', 'C', 'D', 'E']:
    print(f"  ({letter}) {options[letter]}: {results[letter]}")

# The answer is the option that CANNOT be set for more than one client
cannot_be_multiple = [letter for letter in results if not results[letter]]

print(f"\nCannot be set for more than one client: {cannot_be_multiple}")

found_options = []
for letter in ['A', 'B', 'C', 'D', 'E']:
    if not results[letter]:
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