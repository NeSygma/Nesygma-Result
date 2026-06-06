from z3 import *

# We have 3 clients: Image, Solide, Truvest
# For each client, two targets: website and voicemail
# Targets are 1, 2, or 3 days (1 = shortest, 3 = longest)

I_w, I_v = Ints('I_w I_v')  # Image website, Image voicemail
S_w, S_v = Ints('S_w S_v')  # Solide website, Solide voicemail
T_w, T_v = Ints('T_w T_v')  # Truvest website, Truvest voicemail

solver = Solver()

# Domain constraints: each target is 1, 2, or 3 days
for var in [I_w, I_v, S_w, S_v, T_w, T_v]:
    solver.add(Or(var == 1, var == 2, var == 3))

# Condition 1: None of the clients can have a website target that is longer than its voicemail target.
# So website <= voicemail for each client
solver.add(I_w <= I_v)
solver.add(S_w <= S_v)
solver.add(T_w <= T_v)

# Condition 2: Image's voicemail target must be shorter than the other clients' voicemail targets.
# I_v < S_v and I_v < T_v
solver.add(I_v < S_v)
solver.add(I_v < T_v)

# Condition 3: Solide's website target must be shorter than Truvest's website target.
# S_w < T_w
solver.add(S_w < T_w)

# Additional condition from the question: Truvest's website target is shorter than its voicemail target.
# T_w < T_v
solver.add(T_w < T_v)

# Let's first check if the base constraints are satisfiable and see all possible models
print("Checking base constraints...")
result = solver.check()
print(f"Base result: {result}")

if result == sat:
    m = solver.model()
    print(f"I_w = {m[I_w]}, I_v = {m[I_v]}")
    print(f"S_w = {m[S_w]}, S_v = {m[S_v]}")
    print(f"T_w = {m[T_w]}, T_v = {m[T_v]}")

# Let's enumerate all solutions to see what MUST be true
solutions = []
decision_vars = [I_w, I_v, S_w, S_v, T_w, T_v]

# Create a fresh solver for enumeration
solver2 = Solver()
for var in [I_w, I_v, S_w, S_v, T_w, T_v]:
    solver2.add(Or(var == 1, var == 2, var == 3))
solver2.add(I_w <= I_v)
solver2.add(S_w <= S_v)
solver2.add(T_w <= T_v)
solver2.add(I_v < S_v)
solver2.add(I_v < T_v)
solver2.add(S_w < T_w)
solver2.add(T_w < T_v)

while solver2.check() == sat:
    m = solver2.model()
    sol = {v: m.eval(v, model_completion=True) for v in decision_vars}
    solutions.append(sol)
    solver2.add(Or([v != m.eval(v, model_completion=True) for v in decision_vars]))

print(f"\nTotal solutions: {len(solutions)}")
for i, sol in enumerate(solutions):
    print(f"Solution {i+1}: I_w={sol[I_w]}, I_v={sol[I_v]}, S_w={sol[S_w]}, S_v={sol[S_v]}, T_w={sol[T_w]}, T_v={sol[T_v]}")

# Now check each option across ALL solutions
# An option "must be true" if it holds in EVERY solution
option_values = {
    "A": lambda sol: sol[I_v] == 2,
    "B": lambda sol: sol[I_w] == 2,
    "C": lambda sol: sol[I_w] == 1,
    "D": lambda sol: sol[S_w] == 2,
    "E": lambda sol: sol[S_w] == 1,
}

must_be_true = []
for letter, check_fn in option_values.items():
    if all(check_fn(sol) for sol in solutions):
        must_be_true.append(letter)

print(f"\nMust be true options: {must_be_true}")

# Now use the multiple choice skeleton
found_options = []
for letter, constr in [("A", I_v == 2), ("B", I_w == 2), ("C", I_w == 1), ("D", S_w == 2), ("E", S_w == 1)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
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