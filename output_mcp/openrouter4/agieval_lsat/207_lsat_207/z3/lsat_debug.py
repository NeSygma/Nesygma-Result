from z3 import *

pos_K, pos_L, pos_T, pos_W, pos_Y, pos_Z = Ints('pos_K pos_L pos_T pos_W pos_Y pos_Z')
singer_positions = [pos_K, pos_L, pos_T, pos_W, pos_Y, pos_Z]
singer_names = ['K', 'L', 'T', 'W', 'Y', 'Z']

def base_constraints(solver):
    for p in singer_positions:
        solver.add(p >= 1, p <= 6)
    solver.add(Distinct(singer_positions))

def add_other_constraints(solver):
    solver.add(pos_K != 4)
    solver.add(pos_L != 4)
    solver.add(Or(pos_K == 5, pos_L == 5))
    solver.add(pos_K < pos_T)
    solver.add(pos_Z < pos_Y)

def add_original_cond4(solver):
    solver.add(pos_W < pos_K)
    solver.add(pos_W < pos_L)

def enumerate_solutions(solver_setup_func):
    solver = Solver()
    base_constraints(solver)
    add_other_constraints(solver)
    solver_setup_func(solver)
    
    solutions = []
    while solver.check() == sat:
        m = solver.model()
        sol = {
            'K': m.eval(pos_K).as_long(),
            'L': m.eval(pos_L).as_long(),
            'T': m.eval(pos_T).as_long(),
            'W': m.eval(pos_W).as_long(),
            'Y': m.eval(pos_Y).as_long(),
            'Z': m.eval(pos_Z).as_long()
        }
        solutions.append(sol)
        solver.add(Or([p != m.eval(p).as_long() for p in singer_positions]))
    return solutions

print("Original solutions:")
orig = enumerate_solutions(add_original_cond4)
for s in orig:
    print(f"  K:{s['K']} L:{s['L']} T:{s['T']} W:{s['W']} Y:{s['Y']} Z:{s['Z']}")

print()

def opt_a(solver):
    solver.add(And([p > pos_W for name, p in zip(singer_names, singer_positions) if name != 'W' and name != 'Z']))

print("Option A solutions:")
a_sols = enumerate_solutions(opt_a)
for s in a_sols:
    print(f"  K:{s['K']} L:{s['L']} T:{s['T']} W:{s['W']} Y:{s['Y']} Z:{s['Z']}")

# Check if they are exactly the same
orig_tuples = set((s['K'], s['L'], s['T'], s['W'], s['Y'], s['Z']) for s in orig)
a_tuples = set((s['K'], s['L'], s['T'], s['W'], s['Y'], s['Z']) for s in a_sols)
print(f"\nOriginal set size: {len(orig_tuples)}")
print(f"Option A set size: {len(a_tuples)}")
print(f"Difference (orig - A): {orig_tuples - a_tuples}")
print(f"Difference (A - orig): {a_tuples - orig_tuples}")