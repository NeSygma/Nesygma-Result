from z3 import *

workers = ['Q', 'R', 'S', 'T', 'V', 'W', 'X']

member = {w: Bool(f'member_{w}') for w in workers}
leader = {w: Bool(f'leader_{w}') for w in workers}

def make_base_solver():
    solver = Solver()
    solver.add(Sum([If(member[w], 1, 0) for w in workers]) == 3)
    solver.add(Sum([If(leader[w], 1, 0) for w in workers]) == 1)
    for w in workers:
        solver.add(Implies(leader[w], member[w]))
    solver.add(Implies(member['Q'], leader['Q']))
    solver.add(Implies(member['R'], leader['R']))
    solver.add(Implies(member['S'], member['T']))
    solver.add(Implies(member['W'], Not(member['R'])))
    solver.add(Implies(member['W'], Not(member['V'])))
    return solver

# Show the unique solution for Option B
solver = make_base_solver()
solver.add(And(Not(member['Q']), Not(member['T'])))
result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("Unique solution under Option B (Neither Quinn nor Taylor selected):")
    print("Members:")
    for w in workers:
        if m.eval(member[w]):
            print(f"  {w} - {'Leader' if m.eval(leader[w]) else 'Member'}")
else:
    print("STATUS: unsat")