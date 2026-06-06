from z3 import *

# Workers
workers = ['Q', 'R', 'S', 'T', 'V', 'W', 'X']
member = {w: Bool(f'member_{w}') for w in workers}
leader = {w: Bool(f'leader_{w}') for w in workers}

solver = Solver()

# Exactly 3 members
solver.add(Sum([If(member[w], 1, 0) for w in workers]) == 3)

# Exactly 1 leader
solver.add(Sum([If(leader[w], 1, 0) for w in workers]) == 1)

# Leader must be a member
for w in workers:
    solver.add(Implies(leader[w], member[w]))

# Constraint 1: Quinn or Ruiz can be a project member only if leading the project.
solver.add(Implies(member['Q'], leader['Q']))
solver.add(Implies(member['R'], leader['R']))

# Constraint 2: If Smith is a project member, Taylor must also be.
solver.add(Implies(member['S'], member['T']))

# Constraint 3: If Wells is a project member, neither Ruiz nor Verma can be.
solver.add(Implies(member['W'], And(Not(member['R']), Not(member['V']))))

# Question condition: Taylor is not a project member
solver.add(Not(member['T']))

# Check if there are any valid models at all
if solver.check() == sat:
    print("STATUS: sat")
    # Find all valid models to see which workers are always members
    # Actually, the previous logic was correct: if adding Not(member[w]) is unsat, then w must be a member.
    # Let's re-verify the options.
    options = {'A': 'Q', 'B': 'R', 'C': 'V', 'D': 'W', 'E': 'X'}
    for letter, w in options.items():
        solver.push()
        solver.add(Not(member[w]))
        if solver.check() == unsat:
            print(f"answer:{letter}")
        solver.pop()
else:
    print("STATUS: unsat")