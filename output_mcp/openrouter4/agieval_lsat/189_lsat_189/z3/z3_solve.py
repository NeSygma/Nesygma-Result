from z3 import *

workers = ['Q', 'R', 'S', 'T', 'V', 'W', 'X']

# Create member and leader variables
member = {w: Bool(f'member_{w}') for w in workers}
leader = {w: Bool(f'leader_{w}') for w in workers}

def make_base_solver():
    solver = Solver()
    
    # Exactly 3 members
    solver.add(Sum([If(member[w], 1, 0) for w in workers]) == 3)
    
    # Exactly 1 leader
    solver.add(Sum([If(leader[w], 1, 0) for w in workers]) == 1)
    
    # Leader must be a member
    for w in workers:
        solver.add(Implies(leader[w], member[w]))
    
    # Constraint 1: Quinn or Ruiz can be a project member only if leading the project
    solver.add(Implies(member['Q'], leader['Q']))
    solver.add(Implies(member['R'], leader['R']))
    
    # Constraint 2: If Smith is a project member, Taylor must also be
    solver.add(Implies(member['S'], member['T']))
    
    # Constraint 3: If Wells is a project member, neither Ruiz nor Verma can be
    solver.add(Implies(member['W'], Not(member['R'])))
    solver.add(Implies(member['W'], Not(member['V'])))
    
    return solver

# Test each option
options = [
    ("A", And(Not(member['Q']), Not(member['S']))),
    ("B", And(Not(member['Q']), Not(member['T']))),
    ("C", And(Not(member['Q']), Not(member['X']))),
    ("D", And(Not(member['R']), Not(member['W']))),
    ("E", And(Not(member['R']), Not(member['V']))),
]

found_options = []
for letter, constr in options:
    solver = make_base_solver()
    solver.add(constr)
    
    # Enumerate all solutions
    count = 0
    while solver.check() == sat:
        count += 1
        m = solver.model()
        # Block this solution
        solver.add(Or([member[w] != m.eval(member[w]) for w in workers] + 
                      [leader[w] != m.eval(leader[w]) for w in workers]))
    
    print(f"Option {letter}: {count} solutions")
    if count == 1:
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