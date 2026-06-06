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

options = {
    "A": And(Not(is_member['Q']), Not(is_member['S'])),
    "B": And(Not(is_member['R']), Not(is_member['T'])),
    "C": And(Not(is_member['S']), Not(is_member['T'])),
    "D": And(Not(is_member['S']), Not(is_member['X'])),
    "E": And(Not(is_member['T']), Not(is_member['W']))
}

found_options = []
for letter, constr in options.items():
    solver.push()
    solver.add(is_leader['V'] == True)
    solver.add(constr)
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