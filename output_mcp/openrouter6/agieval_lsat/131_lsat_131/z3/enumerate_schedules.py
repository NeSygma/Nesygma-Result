from z3 import *

# Slot numbers: 1: screen1-7, 2: screen1-9, 3: screen2-7, 4: screen2-9, 5: screen3-8
horror = Int('horror')
mystery = Int('mystery')
romance = Int('romance')
scifi = Int('scifi')
western = Int('western')

solver = Solver()
solver.add(horror >= 1, horror <= 5)
solver.add(mystery >= 1, mystery <= 5)
solver.add(romance >= 1, romance <= 5)
solver.add(scifi >= 1, scifi <= 5)
solver.add(western >= 1, western <= 5)
solver.add(Distinct([horror, mystery, romance, scifi, western]))

def get_screen(s):
    return If(Or(s == 1, s == 2), 1,
              If(Or(s == 3, s == 4), 2, 3))

def get_time(s):
    return If(Or(s == 1, s == 3), 7,
              If(Or(s == 2, s == 4), 9, 8))

# Base constraints
solver.add(get_time(western) < get_time(horror))
solver.add(get_screen(scifi) != 3)
solver.add(get_screen(romance) != 2)
solver.add(get_screen(horror) != get_screen(mystery))
# Additional condition: romance before western
solver.add(get_time(romance) < get_time(western))

# Enumerate all solutions
solutions = []
decision_vars = [horror, mystery, romance, scifi, western]
while solver.check() == sat:
    m = solver.model()
    sol = {v: m.eval(v, model_completion=True) for v in decision_vars}
    solutions.append(sol)
    # Blocking clause
    solver.add(Or([v != m.eval(v, model_completion=True) for v in decision_vars]))

print(f"Total solutions: {len(solutions)}")
if len(solutions) == 0:
    print("No solutions")
else:
    # For each solution, evaluate options
    opt_a_count = 0
    opt_b_count = 0
    opt_c_count = 0
    opt_d_count = 0
    opt_e_count = 0
    for sol in solutions:
        h = sol[horror].as_long()
        m = sol[mystery].as_long()
        r = sol[romance].as_long()
        s = sol[scifi].as_long()
        w = sol[western].as_long()
        # Option A: horror on screen 1
        if h in [1,2]:
            opt_a_count += 1
        # Option B: mystery begins at 7 PM (slot 1 or 3)
        if m in [1,3]:
            opt_b_count += 1
        # Option C: mystery on screen 2 (slot 3 or 4)
        if m in [3,4]:
            opt_c_count += 1
        # Option D: sci-fi begins at 9 PM (slot 2 or 4)
        if s in [2,4]:
            opt_d_count += 1
        # Option E: sci-fi on screen 2 (slot 3 or 4)
        if s in [3,4]:
            opt_e_count += 1
    print(f"Option A true in {opt_a_count} solutions")
    print(f"Option B true in {opt_b_count} solutions")
    print(f"Option C true in {opt_c_count} solutions")
    print(f"Option D true in {opt_d_count} solutions")
    print(f"Option E true in {opt_e_count} solutions")
    # Determine which option is true in all solutions
    always_true = []
    if opt_a_count == len(solutions):
        always_true.append('A')
    if opt_b_count == len(solutions):
        always_true.append('B')
    if opt_c_count == len(solutions):
        always_true.append('C')
    if opt_d_count == len(solutions):
        always_true.append('D')
    if opt_e_count == len(solutions):
        always_true.append('E')
    print(f"Options always true: {always_true}")