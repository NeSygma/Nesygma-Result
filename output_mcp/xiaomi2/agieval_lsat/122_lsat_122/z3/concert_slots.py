from z3 import *

# Band positions: Uneasy, Vegemite, Wellspring, Xpert, Yardsign, Zircon
U, V, W, X, Y, Z = Ints('U V W X Y Z')
bands = [U, V, W, X, Y, Z]

def add_base_constraints(solver):
    """Constraints that remain fixed: C1 (V<Z), C4 (U in last 3), C5 (Y in first 3)"""
    for b in bands:
        solver.add(And(b >= 1, b <= 6))
    solver.add(Distinct(bands))
    solver.add(V < Z)           # C1: Vegemite before Zircon
    solver.add(And(U >= 4, U <= 6))  # C4: Uneasy in last three slots
    solver.add(And(Y >= 1, Y <= 3))  # C5: Yardsign in first three slots

def enumerate_solutions(solver, variables):
    """Enumerate all satisfying assignments as a set of tuples."""
    solutions = set()
    while solver.check() == sat:
        m = solver.model()
        sol = tuple(m.eval(v, model_completion=True).as_long() for v in variables)
        solutions.add(sol)
        solver.add(Or([v != m.eval(v, model_completion=True) for v in variables]))
    return solutions

# === Original constraints: C1 + C2(W<X) + C3(Z<X) + C4 + C5 ===
s_orig = Solver()
add_base_constraints(s_orig)
s_orig.add(W < X)  # C2
s_orig.add(Z < X)  # C3
orig = enumerate_solutions(s_orig, bands)
print(f"Original: {len(orig)} solutions")

# === Option A: "Only Uneasy can perform in a later slot than Xpert" ===
# LSAT reading: "Only X can Y" = "If Y then X" => all bands except Uneasy
# must be in earlier slots than Xpert. U's position relative to X is unconstrained.
# This adds: V<X, W<X, Y<X, Z<X (note: V<X and Y<X are redundant given original)
s_a = Solver()
add_base_constraints(s_a)
s_a.add(V < X)
s_a.add(W < X)
s_a.add(Y < X)
s_a.add(Z < X)
sol_a = enumerate_solutions(s_a, bands)
match_a = (orig == sol_a)
print(f"Option A: {len(sol_a)} solutions, match={match_a}")

# === Option B: "Vegemite < Wellspring < Zircon" ===
s_b = Solver()
add_base_constraints(s_b)
s_b.add(V < W)
s_b.add(W < Z)
sol_b = enumerate_solutions(s_b, bands)
match_b = (orig == sol_b)
print(f"Option B: {len(sol_b)} solutions, match={match_b}")

# === Option C: "Vegemite < Xpert and Wellspring < Xpert" ===
s_c = Solver()
add_base_constraints(s_c)
s_c.add(V < X)
s_c.add(W < X)
sol_c = enumerate_solutions(s_c, bands)
match_c = (orig == sol_c)
print(f"Option C: {len(sol_c)} solutions, match={match_c}")

# === Option D: "Xpert performs immediately before or after Uneasy" ===
s_d = Solver()
add_base_constraints(s_d)
s_d.add(Or(X - U == 1, U - X == 1))
sol_d = enumerate_solutions(s_d, bands)
match_d = (orig == sol_d)
print(f"Option D: {len(sol_d)} solutions, match={match_d}")

# === Option E: "Xpert in slot 5 or slot 6" ===
s_e = Solver()
add_base_constraints(s_e)
s_e.add(Or(X == 5, X == 6))
sol_e = enumerate_solutions(s_e, bands)
match_e = (orig == sol_e)
print(f"Option E: {len(sol_e)} solutions, match={match_e}")

# === Determine answer ===
found_options = []
for letter, match in [('A', match_a), ('B', match_b), ('C', match_c), ('D', match_d), ('E', match_e)]:
    if match:
        found_options.append(letter)

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