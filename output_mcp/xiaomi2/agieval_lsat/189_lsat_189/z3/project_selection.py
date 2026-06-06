from z3 import *

names = ['Q', 'R', 'S', 'T', 'V', 'W', 'X']
n = 7

# Create variables once (Z3 reuses symbolic names)
member = [Bool(f'member_{names[i]}') for i in range(n)]
leader = [Bool(f'leader_{names[i]}') for i in range(n)]

def count_solutions(extra_constraint):
    solver = Solver()
    
    # Exactly 3 members
    solver.add(Sum([If(member[i], 1, 0) for i in range(n)]) == 3)
    
    # Exactly 1 leader
    solver.add(Sum([If(leader[i], 1, 0) for i in range(n)]) == 1)
    
    # Leader must be a member
    for i in range(n):
        solver.add(Implies(leader[i], member[i]))
    
    # Constraint 1: Q or R can be member only if leading
    solver.add(Implies(member[0], leader[0]))  # Q
    solver.add(Implies(member[1], leader[1]))  # R
    
    # Constraint 2: If S is member, T must be
    solver.add(Implies(member[2], member[3]))
    
    # Constraint 3: If W is member, neither R nor V can be
    solver.add(Implies(member[5], Not(member[1])))
    solver.add(Implies(member[5], Not(member[4])))
    
    # Add the extra constraint for this option
    solver.add(extra_constraint)
    
    # Enumerate all solutions
    decision_vars = member + leader
    solutions = []
    while solver.check() == sat:
        m = solver.model()
        sol = tuple(is_true(m.eval(v, model_completion=True)) for v in decision_vars)
        solutions.append(sol)
        # Block this solution
        solver.add(Or([v != m.eval(v, model_completion=True) for v in decision_vars]))
    
    return len(solutions), solutions

# Define options
options = [
    ("A", And(Not(member[0]), Not(member[2]))),  # Neither Q nor S
    ("B", And(Not(member[0]), Not(member[3]))),  # Neither Q nor T
    ("C", And(Not(member[0]), Not(member[6]))),  # Neither Q nor X
    ("D", And(Not(member[1]), Not(member[5]))),  # Neither R nor W
    ("E", And(Not(member[1]), Not(member[4]))),  # Neither R nor V
]

found_options = []
for letter, constr in options:
    count, sols = count_solutions(constr)
    print(f"Option {letter}: {count} solution(s)")
    if count == 1:
        # Print the unique solution
        sol = sols[0]
        mbrs = [names[i] for i in range(n) if sol[i]]
        ldrs = [names[i] for i in range(n) if sol[n + i]]
        print(f"  Members: {mbrs}, Leader: {ldrs}")
        found_options.append(letter)
    elif count > 1:
        for idx, sol in enumerate(sols[:5]):  # print first few
            mbrs = [names[i] for i in range(n) if sol[i]]
            ldrs = [names[i] for i in range(n) if sol[n + i]]
            print(f"  Sol {idx+1}: Members={mbrs}, Leader={ldrs}")
        if count > 5:
            print(f"  ... and {count - 5} more")

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