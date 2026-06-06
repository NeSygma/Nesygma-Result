from z3 import *

def enumerate_solutions(solver, variables):
    solutions = set()
    var_list = list(variables.values())
    while solver.check() == sat:
        m = solver.model()
        sol_tuple = tuple(m.eval(v, model_completion=True).as_long() for v in var_list)
        solutions.add(sol_tuple)
        solver.add(Or([v != m.eval(v, model_completion=True) for v in var_list]))
    return solutions

U, V, W, X, Y, Z = Ints('U V W X Y Z')
bands = {'U': U, 'V': V, 'W': W, 'X': X, 'Y': Y, 'Z': Z}

domain = [And(v >= 1, v <= 6) for v in bands.values()]
all_distinct = [Distinct(list(bands.values()))]

# Original constraints
c1 = V < Z
c2 = And(W < X, Z < X)
c3 = U >= 4
c4 = Y <= 3

s_orig = Solver()
s_orig.add(domain + all_distinct + [c1, c2, c3, c4])
orig_set = enumerate_solutions(s_orig, bands)

# Options (replacing c2)
options = {
    'A': And(V < X, W < X, Y < X, Z < X),
    'B': And(V < W, W < Z),
    'C': And(V < X, W < X),
    'D': Or(X == U - 1, X == U + 1),
    'E': Or(X == 5, X == 6),
}

found = []
for letter, opt in options.items():
    s = Solver()
    s.add(domain + all_distinct + [c1, c3, c4, opt])
    sols = enumerate_solutions(s, bands)
    if sols == orig_set:
        found.append(letter)

if len(found) == 1:
    print("STATUS: sat")
    print(f"answer:{found[0]}")
elif len(found) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")