from z3 import *

workers = ['Q', 'R', 'S', 'T', 'V', 'W', 'X']

def create_base_solver():
    solver = Solver()
    is_member = {w: Bool(f'member_{w}') for w in workers}
    is_leader = {w: Bool(f'leader_{w}') for w in workers}
    
    # Exactly 3 members
    solver.add(Sum([If(is_member[w], 1, 0) for w in workers]) == 3)
    
    # Exactly 1 leader
    solver.add(Sum([If(is_leader[w], 1, 0) for w in workers]) == 1)
    
    # Leader must be a member
    for w in workers:
        solver.add(Implies(is_leader[w], is_member[w]))
    
    # Constraint 1: Q or R can be member only if leading
    solver.add(Implies(is_member['Q'], is_leader['Q']))
    solver.add(Implies(is_member['R'], is_leader['R']))
    
    # Constraint 2: If S is member, T must be
    solver.add(Implies(is_member['S'], is_member['T']))
    
    # Constraint 3: If W is member, neither R nor V can be
    solver.add(Implies(is_member['W'], Not(is_member['R'])))
    solver.add(Implies(is_member['W'], Not(is_member['V'])))
    
    return solver, is_member, is_leader

def enumerate_solutions(solver, is_member, is_leader):
    decision_vars = [is_member[w] for w in workers] + [is_leader[w] for w in workers]
    solutions = []
    while solver.check() == sat:
        m = solver.model()
        sol = {}
        for w in workers:
            sol[f'm_{w}'] = is_true(m.evaluate(is_member[w]))
            sol[f'l_{w}'] = is_true(m.evaluate(is_leader[w]))
        solutions.append(sol)
        # Block current solution
        solver.add(Or([v != m.evaluate(v, model_completion=True) for v in decision_vars]))
    return solutions

# First, enumerate base solutions (no additional constraint)
solver, is_member, is_leader = create_base_solver()
base_sols = enumerate_solutions(solver, is_member, is_leader)
print(f"Base solutions (no option): {len(base_sols)}")
for s in base_sols:
    members = [w for w in workers if s[f'm_{w}']]
    leader = [w for w in workers if s[f'l_{w}']]
    print(f"  Members: {members}, Leader: {leader}")

# Define option constraints
option_defs = [
    ("A", lambda im: And(Not(im['Q']), Not(im['S']))),   # Neither Quinn nor Smith
    ("B", lambda im: And(Not(im['Q']), Not(im['T']))),   # Neither Quinn nor Taylor
    ("C", lambda im: And(Not(im['Q']), Not(im['X']))),   # Neither Quinn nor Xue
    ("D", lambda im: And(Not(im['R']), Not(im['W']))),   # Neither Ruiz nor Wells
    ("E", lambda im: And(Not(im['R']), Not(im['V']))),   # Neither Ruiz nor Verma
]

found_options = []

for letter, opt_constr in option_defs:
    solver, is_member, is_leader = create_base_solver()
    solver.add(opt_constr(is_member))
    sols = enumerate_solutions(solver, is_member, is_leader)
    print(f"\nOption {letter}: {len(sols)} solution(s)")
    for s in sols:
        members = [w for w in workers if s[f'm_{w}']]
        leader = [w for w in workers if s[f'l_{w}']]
        print(f"  Members: {members}, Leader: {leader}")
    if len(sols) == 1:
        found_options.append(letter)

print(f"\nFound options with exactly 1 solution: {found_options}")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")