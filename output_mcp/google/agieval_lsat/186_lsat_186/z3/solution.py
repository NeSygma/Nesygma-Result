from z3 import *

workers = ['Q', 'R', 'S', 'T', 'V', 'W', 'X']
is_member = {w: Bool(f'member_{w}') for w in workers}
is_leader = {w: Bool(f'leader_{w}') for w in workers}

solver = Solver()

# Exactly 3 members
solver.add(Sum([If(is_member[w], 1, 0) for w in workers]) == 3)

# Exactly 1 leader
solver.add(Sum([If(is_leader[w], 1, 0) for w in workers]) == 1)

# Leader must be a member
for w in workers:
    solver.add(Implies(is_leader[w], is_member[w]))

# Constraint 1: Quinn or Ruiz can be a project member only if leading the project.
solver.add(Implies(is_member['Q'], is_leader['Q']))
solver.add(Implies(is_member['R'], is_leader['R']))

# Constraint 2: If Smith is a project member, Taylor must also be.
solver.add(Implies(is_member['S'], is_member['T']))

# Constraint 3: If Wells is a project member, neither Ruiz nor Verma can be.
solver.add(Implies(is_member['W'], And(Not(is_member['R']), Not(is_member['V']))))

# Question condition: Taylor is the project leader and Wells is a project member
solver.add(is_leader['T'] == True)
solver.add(is_member['W'] == True)

# Find all possible third members
# The members are {T, W, X_third}
# X_third must be one of {Q, R, S, V, X}
possible_third_members = []
for w in ['Q', 'R', 'S', 'V', 'X']:
    solver.push()
    solver.add(is_member[w] == True)
    # Ensure w is not T or W (already members)
    if w != 'T' and w != 'W':
        if solver.check() == sat:
            possible_third_members.append(w)
    solver.pop()

print(f"Possible third members: {possible_third_members}")

# Test options
options = {
    "A": ['Q', 'S'],
    "B": ['Q', 'X'],
    "C": ['R', 'V'],
    "D": ['S', 'X'],
    "E": ['V', 'X']
}

found_options = []
for label, members in options.items():
    solver.push()
    # The third member must be one of the members in the option
    # AND no other member can be the third member
    # Actually, the question asks "the third project member must be either X or Y"
    # This means the set of possible third members is exactly {X, Y}
    
    # Let's check if the set of possible third members is exactly the set in the option
    # Or if the option is a subset of the possible third members?
    # Usually "must be either X or Y" means the third member is in {X, Y}.
    
    # Let's check if all possible third members are in the option
    # AND if the option members are possible.
    
    is_subset = all(m in members for m in possible_third_members)
    # Also check if the option members are actually possible
    are_members_possible = all(m in possible_third_members for m in members)
    
    if is_subset and are_members_possible:
        found_options.append(label)
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