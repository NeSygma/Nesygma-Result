from z3 import *

# 7 workers
names = ['Q', 'R', 'S', 'T', 'V', 'W', 'X']
member = {n: Bool(f'{n}_member') for n in names}
leader = {n: Bool(f'{n}_leader') for n in names}

def base_solver():
    s = Solver()
    # Exactly 3 members
    s.add(Sum([If(member[n], 1, 0) for n in names]) == 3)
    # Exactly 1 leader
    s.add(Sum([If(leader[n], 1, 0) for n in names]) == 1)
    # Leader implies member
    for n in names:
        s.add(Implies(leader[n], member[n]))
    # Q or R only if leading
    s.add(Implies(member['Q'], leader['Q']))
    s.add(Implies(member['R'], leader['R']))
    # If Smith is member, Taylor must be too
    s.add(Implies(member['S'], member['T']))
    # If Wells is member, neither Ruiz nor Verma can be
    s.add(Implies(member['W'], And(Not(member['R']), Not(member['V']))))
    return s

# Define option constraints
options = {
    "A": And(Not(member['Q']), Not(member['S'])),
    "B": And(Not(member['Q']), Not(member['T'])),
    "C": And(Not(member['Q']), Not(member['X'])),
    "D": And(Not(member['R']), Not(member['W'])),
    "E": And(Not(member['R']), Not(member['V']))
}

decision_vars = [member[n] for n in names] + [leader[n] for n in names]

found_options = []
for letter, opt_constr in options.items():
    s = base_solver()
    s.add(opt_constr)
    # Count all solutions
    solutions = []
    while s.check() == sat:
        m = s.model()
        # Record solution
        sol = tuple(m.eval(v, model_completion=True) for v in decision_vars)
        solutions.append(sol)
        # Block this solution
        s.add(Or([v != m.eval(v, model_completion=True) for v in decision_vars]))
    print(f"Option {letter}: {len(solutions)} solution(s)")
    if len(solutions) == 1:
        found_options.append(letter)
        # Also print the unique solution
        m = None
        # Re-solve to get model
        s2 = base_solver()
        s2.add(opt_constr)
        s2.check()
        m2 = s2.model()
        print(f"  Members: {[n for n in names if is_true(m2.eval(member[n]))]}")
        print(f"  Leader: {[n for n in names if is_true(m2.eval(leader[n]))]}")
    elif len(solutions) == 0:
        print("  (unsat)")
    else:
        print(f"  Multiple solutions found")
        for i, sol in enumerate(solutions):
            print(f"  Solution {i+1}: {sol}")

print()
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")