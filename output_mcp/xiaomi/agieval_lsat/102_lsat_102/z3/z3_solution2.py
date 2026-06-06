from z3 import *

# Base constraints
def add_base(solver):
    # Witnesses: Franco=0, Garcia=1, Hong=2, Iturbe=3, Jackson=4
    # Days: Monday=0, Tuesday=1, Wednesday=2
    witnesses = [Int(f'w_{i}') for i in range(5)]
    
    for w in witnesses:
        solver.add(Or(w == 0, w == 1, w == 2))
    
    # Franco does not testify on the same day as Garcia
    solver.add(witnesses[0] != witnesses[1])
    
    # Iturbe testifies on Wednesday
    solver.add(witnesses[3] == 2)
    
    # Exactly two witnesses testify on Tuesday
    solver.add(Sum([If(w == 1, 1, 0) for w in witnesses]) == 2)
    
    # Hong does not testify on Monday
    solver.add(witnesses[2] != 0)
    
    # At least one witness testifies on Monday
    solver.add(Sum([If(w == 0, 1, 0) for w in witnesses]) >= 1)
    
    # Franco is scheduled to testify on the same day as Hong
    solver.add(witnesses[0] == witnesses[2])
    
    return witnesses

# For "must be true" logic: an option MUST be true if its negation is unsatisfiable
# i.e., there is NO valid schedule where the option is false

options = {
    "A": "Franco is scheduled to testify on Wednesday.",
    "B": "Garcia is scheduled to testify on Monday.",
    "C": "Garcia is scheduled to testify on Wednesday.",
    "D": "Hong is scheduled to testify on Tuesday.",
    "E": "Iturbe is the only witness scheduled to testify on Wednesday."
}

# Option negations (what we check for unsatisfiability)
def get_option_negation(letter, witnesses):
    if letter == "A":
        # NOT: Franco on Wednesday
        return witnesses[0] != 2
    elif letter == "B":
        # NOT: Garcia on Monday
        return witnesses[1] != 0
    elif letter == "C":
        # NOT: Garcia on Wednesday
        return witnesses[1] != 2
    elif letter == "D":
        # NOT: Hong on Tuesday
        return witnesses[2] != 1
    elif letter == "E":
        # NOT: Iturbe is the only one on Wednesday
        # i.e., at least one other witness is also on Wednesday
        return Or(witnesses[0] == 2, witnesses[1] == 2, witnesses[2] == 2, witnesses[4] == 2)

must_be_true = []

for letter in ["A", "B", "C", "D", "E"]:
    s = Solver()
    witnesses = add_base(s)
    s.add(get_option_negation(letter, witnesses))
    result = s.check()
    if result == unsat:
        # The negation is unsatisfiable, so the option MUST be true
        must_be_true.append(letter)
    elif result == sat:
        print(f"Option {letter} can be false (counterexample exists)")
    else:
        print(f"Option {letter}: unknown")

print(f"\nMust be true options: {must_be_true}")

if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple must-be-true options {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No must-be-true options found")