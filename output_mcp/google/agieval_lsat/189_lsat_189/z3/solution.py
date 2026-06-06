from z3 import *

workers = ['Q', 'R', 'S', 'T', 'V', 'W', 'X']
member = {w: Bool(f'm_{w}') for w in workers}
leader = {w: Bool(f'l_{w}') for w in workers}

def get_base_constraints():
    constraints = []
    # Exactly 3 members
    constraints.append(Sum([If(member[w], 1, 0) for w in workers]) == 3)
    # Exactly 1 leader
    constraints.append(Sum([If(leader[w], 1, 0) for w in workers]) == 1)
    # Leader must be a member
    for w in workers:
        constraints.append(Implies(leader[w], member[w]))
    # Q or R can be a member only if leading
    constraints.append(Implies(member['Q'], leader['Q']))
    constraints.append(Implies(member['R'], leader['R']))
    # If S is a member, T must be
    constraints.append(Implies(member['S'], member['T']))
    # If W is a member, neither R nor V can be
    constraints.append(Implies(member['W'], And(Not(member['R']), Not(member['V']))))
    return constraints

def count_solutions(extra_constraint):
    solver = Solver()
    solver.add(get_base_constraints())
    solver.add(extra_constraint)
    
    solutions = []
    while solver.check() == sat:
        m = solver.model()
        sol = {w: (is_true(m.eval(member[w])), is_true(m.eval(leader[w]))) for w in workers}
        solutions.append(sol)
        # Block this solution
        block = []
        for w in workers:
            block.append(member[w] != m.eval(member[w]))
            block.append(leader[w] != m.eval(leader[w]))
        solver.add(Or(block))
    return len(solutions)

# Options
opt_a = And(Not(member['Q']), Not(member['S']))
opt_b = And(Not(member['Q']), Not(member['T']))
opt_c = And(Not(member['Q']), Not(member['X']))
opt_d = And(Not(member['R']), Not(member['W']))
opt_e = And(Not(member['R']), Not(member['V']))

options = [
    ("A", opt_a),
    ("B", opt_b),
    ("C", opt_c),
    ("D", opt_d),
    ("E", opt_e)
]

found_options = []
for letter, constr in options:
    if count_solutions(constr) == 1:
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