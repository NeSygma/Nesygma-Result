from z3 import *

# Days: 1=Mon, 2=Tue, 3=Wed, 4=Thu, 5=Fri
# Wednesday (3) is excluded by the problem condition
VALID_DAYS = [1, 2, 4, 5]

# Batches: O1,O2,O3 (oatmeal), P1,P2,P3 (peanut butter), S1,S2,S3 (sugar)
O1, O2, O3 = Ints('O1 O2 O3')
P1, P2, P3 = Ints('P1 P2 P3')
S1, S2, S3 = Ints('S1 S2 S3')

all_batches = [O1, O2, O3, P1, P2, P3, S1, S2, S3]

def base_constraints():
    """Return list of base constraints."""
    cons = []
    # Each batch on a valid day (not Wednesday)
    for b in all_batches:
        cons.append(Or([b == d for d in VALID_DAYS]))
    
    # No two batches of same kind on same day
    cons.append(Distinct(O1, O2, O3))
    cons.append(Distinct(P1, P2, P3))
    cons.append(Distinct(S1, S2, S3))
    
    # At least one batch on Monday
    cons.append(Or([b == 1 for b in all_batches]))
    
    # O2 same day as P1
    cons.append(O2 == P1)
    
    # S2 on Thursday
    cons.append(S2 == 4)
    
    return cons

# Count batches per day helper
def batches_on_day(d):
    return Sum([If(b == d, 1, 0) for b in all_batches])

# Define answer choice constraints (what each option claims)
# (A) Exactly 3 batches on Tuesday
opt_a = (batches_on_day(2) == 3)
# (B) Exactly 3 batches on Friday
opt_b = (batches_on_day(5) == 3)
# (C) At least 2 batches on Monday
opt_c = (batches_on_day(1) >= 2)
# (D) At least 2 batches on Thursday
opt_d = (batches_on_day(4) >= 2)
# (E) Fewer batches on Monday than on Tuesday
opt_e = (batches_on_day(1) < batches_on_day(2))

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

# For "must be true", we check if the NEGATION is unsatisfiable
# i.e., can we find a valid model where the option is FALSE?
# If NOT (negation is unsat), then the option MUST be true.

must_be_true = []
for letter, constr in options:
    s = Solver()
    s.add(base_constraints())
    s.add(Not(constr))  # Try to find a counterexample
    result = s.check()
    if result == unsat:
        # No counterexample exists -> must be true
        must_be_true.append(letter)
        print(f"Option {letter}: MUST BE TRUE (negation is unsat)")
    elif result == sat:
        m = s.model()
        print(f"Option {letter}: NOT necessarily true (counterexample exists)")
        # Print the counterexample
        day_names = {1: "Mon", 2: "Tue", 4: "Thu", 5: "Fri"}
        for b in all_batches:
            val = m.eval(b)
            print(f"  {b} = {day_names.get(int(str(val)), str(val))}")
        counts = {d: sum(1 for b in all_batches if m.eval(b).as_long() == d) for d in VALID_DAYS}
        print(f"  Day counts: {counts}")
    else:
        print(f"Option {letter}: UNKNOWN")
        must_be_true.append(letter + "(unknown)")

print()
print(f"Options that must be true: {must_be_true}")

# Now use the exact required skeleton for final answer
found_options = []
for letter, constr in options:
    s2 = Solver()
    s2.add(base_constraints())
    s2.add(Not(constr))
    if s2.check() == unsat:
        found_options.append(letter)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")