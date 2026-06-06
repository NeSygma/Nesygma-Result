from z3 import *

# The question asks which MUST be true (i.e., is true in ALL valid schedules).
# Strategy: For each option, check if its negation is UNSATISFIABLE given the base constraints.
# If Not(option) is unsat, then option MUST be true.

# Base constraints
def add_base_constraints(solver):
    witnesses = [Int(f'w_{i}') for i in range(5)]
    # Each witness testifies on exactly one day (0=Mon, 1=Tue, 2=Wed)
    for w in witnesses:
        solver.add(Or(w == 0, w == 1, w == 2))
    # Franco != Garcia
    solver.add(witnesses[0] != witnesses[1])
    # Iturbe on Wednesday
    solver.add(witnesses[3] == 2)
    # Exactly two witnesses on Tuesday
    solver.add(Sum([If(w == 1, 1, 0) for w in witnesses]) == 2)
    # Hong not on Monday
    solver.add(witnesses[2] != 0)
    # At least one on Monday
    solver.add(Sum([If(w == 0, 1, 0) for w in witnesses]) >= 1)
    # Jackson on Wednesday
    solver.add(witnesses[4] == 2)
    return witnesses

# (A) Franco on Monday
# (B) Garcia on Monday
# (C) Exactly one on Monday
# (D) Exactly two on Monday
# (E) Garcia same day as Hong

options = {
    "A": lambda w: w[0] == 0,
    "B": lambda w: w[1] == 0,
    "C": lambda w: Sum([If(x == 0, 1, 0) for x in w]) == 1,
    "D": lambda w: Sum([If(x == 0, 1, 0) for x in w]) == 2,
    "E": lambda w: w[1] == w[2],
}

must_be_true = []

for letter, opt_fn in options.items():
    s = Solver()
    w = add_base_constraints(s)
    # Try to find a model where the option is FALSE
    s.add(Not(opt_fn(w)))
    result = s.check()
    if result == unsat:
        # Option cannot be false => MUST be true
        must_be_true.append(letter)
        print(f"Option {letter}: MUST be true (negation is unsat)")
    elif result == sat:
        m = s.model()
        print(f"Option {letter}: NOT necessarily true (counterexample exists)")
        for i in range(5):
            print(f"  {['Franco','Garcia','Hong','Iturbe','Jackson'][i]} = {['Mon','Tue','Wed'][m.evaluate(w[i]).as_long()]}")
    else:
        print(f"Option {letter}: unknown")

print()
if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: proved")
    print(f"RESULT: Multiple must-be-true options: {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No option must be true")