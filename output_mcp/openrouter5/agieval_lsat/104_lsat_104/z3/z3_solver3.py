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

# Let's first enumerate all possible solutions to see what's forced
solutions = []
decision_vars = [I_w, I_v, S_w, S_v, T_w, T_v]

while solver.check() == sat:
    m = solver.model()
    sol = {str(v): m.eval(v, model_completion=True).as_long() for v in decision_vars}
    solutions.append(sol)
    # Block this solution
    solver.add(Or([v != m.eval(v, model_completion=True) for v in decision_vars]))

print(f"Total solutions: {len(solutions)}")
for s in solutions:
    print(s)

# Now let's check each option more carefully
# The question asks "which one of the following MUST be true"
# So we need to check if an option holds in ALL solutions
# If an option is true in all solutions, then it MUST be true.

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

# For "must be true", we check if the negation of the option is UNSAT
# i.e., if adding NOT(option) makes the problem unsat, then option MUST be true

found_must = []
for letter, constr in [("A", I_v == 2), ("B", I_w == 2), ("C", I_w == 1), ("D", S_w == 2), ("E", S_w == 1)]:
    solver2.push()
    solver2.add(Not(constr))
    if solver2.check() == unsat:
        found_must.append(letter)
    solver2.pop()

print(f"Must be true options: {found_must}")

if len(found_must) == 1:
    print("STATUS: sat")
    print(f"answer:{found_must[0]}")
elif len(found_must) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_must}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")