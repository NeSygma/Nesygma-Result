from z3 import *

# Workers: Quinn, Ruiz, Smith, Taylor, Verma, Wells, Xue
workers = ['Quinn', 'Ruiz', 'Smith', 'Taylor', 'Verma', 'Wells', 'Xue']
n = len(workers)

# Boolean variables: is worker selected as member?
member = {w: Bool(f'member_{w}') for w in workers}

# Exactly 3 members selected
solver = Solver()
solver.add(Sum([If(member[w], 1, 0) for w in workers]) == 3)

# Exactly one leader among the selected members
# leader[w] means w is the leader (implies member[w])
leader = {w: Bool(f'leader_{w}') for w in workers}
solver.add(Sum([If(leader[w], 1, 0) for w in workers]) == 1)
for w in workers:
    solver.add(Implies(leader[w], member[w]))

# Constraint 1: Quinn or Ruiz can be a project member only if leading the project.
solver.add(Implies(member['Quinn'], leader['Quinn']))
solver.add(Implies(member['Ruiz'], leader['Ruiz']))

# Constraint 2: If Smith is a project member, Taylor must also be.
solver.add(Implies(member['Smith'], member['Taylor']))

# Constraint 3: If Wells is a project member, neither Ruiz nor Verma can be.
solver.add(Implies(member['Wells'], And(Not(member['Ruiz']), Not(member['Verma']))))

# Now test each option to see which one completely determines the selection.
# "Completely determined" means adding that constraint yields exactly one valid assignment.

# Helper: enumerate all solutions under a given extra constraint
def count_solutions(extra_constr):
    s = Solver()
    # Copy base constraints
    s.add(Sum([If(member[w], 1, 0) for w in workers]) == 3)
    s.add(Sum([If(leader[w], 1, 0) for w in workers]) == 1)
    for w in workers:
        s.add(Implies(leader[w], member[w]))
    s.add(Implies(member['Quinn'], leader['Quinn']))
    s.add(Implies(member['Ruiz'], leader['Ruiz']))
    s.add(Implies(member['Smith'], member['Taylor']))
    s.add(Implies(member['Wells'], And(Not(member['Ruiz']), Not(member['Verma']))))
    s.add(extra_constr)
    
    solutions = []
    decision_vars = [member[w] for w in workers] + [leader[w] for w in workers]
    while s.check() == sat:
        m = s.model()
        sol = tuple(m.eval(v, model_completion=True) for v in decision_vars)
        solutions.append(sol)
        s.add(Or([v != m.eval(v, model_completion=True) for v in decision_vars]))
    return len(solutions)

# Option constraints
opt_a = And(Not(member['Quinn']), Not(member['Smith']))
opt_b = And(Not(member['Quinn']), Not(member['Taylor']))
opt_c = And(Not(member['Quinn']), Not(member['Xue']))
opt_d = And(Not(member['Ruiz']), Not(member['Wells']))
opt_e = And(Not(member['Ruiz']), Not(member['Verma']))

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

found_options = []
for letter, constr in options:
    n_sol = count_solutions(constr)
    print(f"Option {letter}: {n_sol} solution(s)")
    if n_sol == 1:
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