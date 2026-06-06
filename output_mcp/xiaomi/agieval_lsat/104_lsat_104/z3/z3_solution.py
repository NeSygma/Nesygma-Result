from z3 import *

solver = Solver()

# Define variables for each client's website and voicemail targets
# Values: 1, 2, or 3 days
I_w = Int('I_w')  # Image website
I_v = Int('I_v')  # Image voicemail
S_w = Int('S_w')  # Solide website
S_v = Int('S_v')  # Solide voicemail
T_w = Int('T_w')  # Truvest website
T_v = Int('T_v')  # Truvest voicemail

# Domain constraints: each target is 1, 2, or 3
for v in [I_w, I_v, S_w, S_v, T_w, T_v]:
    solver.add(Or(v == 1, v == 2, v == 3))

# Condition 1: None of the clients can have a website target that is longer than its voicemail target.
solver.add(I_w <= I_v)
solver.add(S_w <= S_v)
solver.add(T_w <= T_v)

# Condition 2: Image's voicemail target must be shorter than the other clients' voicemail targets.
solver.add(I_v < S_v)
solver.add(I_v < T_v)

# Condition 3: Solide's website target must be shorter than Truvest's website target.
solver.add(S_w < T_w)

# Additional condition from question: Truvest's website target is shorter than its voicemail target
solver.add(T_w < T_v)

# Let's enumerate all valid assignments to understand the solution space
print("=== All valid assignments ===")
count = 0
while solver.check() == sat:
    m = solver.model()
    count += 1
    iw = m[I_w].as_long()
    iv = m[I_v].as_long()
    sw = m[S_w].as_long()
    sv = m[S_v].as_long()
    tw = m[T_w].as_long()
    tv = m[T_v].as_long()
    print(f"Sol {count}: I_w={iw}, I_v={iv}, S_w={sw}, S_v={sv}, T_w={tw}, T_v={tv}")
    # Block this solution
    solver.add(Or(I_w != iw, I_v != iv, S_w != sw, S_v != sv, T_w != tw, T_v != tv))

print(f"\nTotal solutions: {count}")

# Now check which options are ALWAYS true (must be true in ALL solutions)
print("\n=== Checking which options must be true ===")

# Re-create solver with all base constraints
solver2 = Solver()
for v in [I_w, I_v, S_w, S_v, T_w, T_v]:
    solver2.add(Or(v == 1, v == 2, v == 3))
solver2.add(I_w <= I_v)
solver2.add(S_w <= S_v)
solver2.add(T_w <= T_v)
solver2.add(I_v < S_v)
solver2.add(I_v < T_v)
solver2.add(S_w < T_w)
solver2.add(T_w < T_v)

# For each option, check if its negation is UNSAT (meaning the option must be true)
options = {
    "A": (I_v == 2),
    "B": (I_w == 2),
    "C": (I_w == 1),
    "D": (S_w == 2),
    "E": (S_w == 1),
}

must_be_true = []
for letter, constr in options.items():
    s = Solver()
    for v in [I_w, I_v, S_w, S_v, T_w, T_v]:
        s.add(Or(v == 1, v == 2, v == 3))
    s.add(I_w <= I_v)
    s.add(S_w <= S_v)
    s.add(T_w <= T_v)
    s.add(I_v < S_v)
    s.add(I_v < T_v)
    s.add(S_w < T_w)
    s.add(T_w < T_v)
    # Try to find a model where the option is FALSE
    s.add(Not(constr))
    result = s.check()
    if result == unsat:
        print(f"Option {letter}: MUST BE TRUE (negation is unsat)")
        must_be_true.append(letter)
    else:
        print(f"Option {letter}: NOT necessarily true (counterexample exists)")

print(f"\nOptions that must be true: {must_be_true}")
if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple must-be-true options {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No must-be-true options found")