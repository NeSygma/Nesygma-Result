from z3 import *

# Variables: each cookbook's season (0 = spring, 1 = fall)
K, L, M, N, O, P = Bools('K L M N O P')
# True = fall, False = spring

solver = Solver()

# Constraints:
# 1. M and P cannot be in the same season
solver.add(M != P)

# 2. K and N must be in the same season
solver.add(K == N)

# 3. If K is in fall, O must also be in fall
solver.add(Implies(K, O))

# 4. If M is in fall, N must be in spring
solver.add(Implies(M, Not(N)))

# Now evaluate each option.
# Each option adds an extra constraint. We want the option that FULLY DETERMINES the schedule,
# meaning that with that extra constraint, there is exactly one solution.

# We'll check each option: if sat, we'll also count how many solutions exist.
# The correct answer is the one where exactly one solution exists.

options = [
    ("A", And(K, Not(L))),  # K is fall, L is spring
    ("B", And(O, Not(P))),  # O is fall, P is spring
    ("C", And(P, Not(L))),  # P is fall, L is spring
    ("D", And(Not(K), Not(L))),  # Both K and L are spring
    ("E", And(M, L))  # Both M and L are fall
]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        # Count solutions
        count = 0
        s_copy = Solver()
        # Re-add all constraints
        # We need to copy constraints. Let's just use a fresh solver approach.
        # Actually, let's count by blocking.
        temp_solver = Solver()
        # Add base constraints
        temp_solver.add(M != P)
        temp_solver.add(K == N)
        temp_solver.add(Implies(K, O))
        temp_solver.add(Implies(M, Not(N)))
        temp_solver.add(constr)
        
        # Enumerate all solutions
        vars_list = [K, L, M, N, O, P]
        while temp_solver.check() == sat:
            count += 1
            m = temp_solver.model()
            temp_solver.add(Or([v != m.eval(v) for v in vars_list]))
        
        if count == 1:
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