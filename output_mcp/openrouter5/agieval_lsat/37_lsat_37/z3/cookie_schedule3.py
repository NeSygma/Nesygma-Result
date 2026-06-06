from z3 import *

# Let me think more carefully about the problem.
# We have 3 kinds: oatmeal (O), peanut butter (P), sugar (S)
# Each kind has 3 batches: first, second, third
# Days: Monday=0, Tuesday=1, Wednesday=2, Thursday=3, Friday=4

O1, O2, O3 = Ints('O1 O2 O3')
P1, P2, P3 = Ints('P1 P2 P3')
S1, S2, S3 = Ints('S1 S2 S3')

all_batches = [O1, O2, O3, P1, P2, P3, S1, S2, S3]

# Base constraints
solver_base = Solver()
for b in all_batches:
    solver_base.add(b >= 0, b <= 4)

# No two batches of the same kind on the same day
solver_base.add(Distinct(O1, O2, O3))
solver_base.add(Distinct(P1, P2, P3))
solver_base.add(Distinct(S1, S2, S3))

# At least one batch on Monday
solver_base.add(Or([b == 0 for b in all_batches]))

# Second oatmeal = first peanut butter
solver_base.add(O2 == P1)

# Second sugar on Thursday
solver_base.add(S2 == 3)

# Now, each option gives a COMPLETE AND ACCURATE list of days for each kind.
# This means: for each kind, the set of days its 3 batches are made on is exactly as listed.
# The batches are ordered (1st, 2nd, 3rd), so we need to assign which batch goes on which day.

# Let me encode each option properly.

def option_constr(O_days, P_days, S_days):
    """O_days, P_days, S_days are lists of 3 distinct days each."""
    # O1, O2, O3 must be a permutation of O_days
    o = Or([And(O1==a, O2==b, O3==c) for a in O_days for b in O_days for c in O_days 
            if len({a,b,c})==3 and sorted([a,b,c])==sorted(O_days)])
    p = Or([And(P1==a, P2==b, P3==c) for a in P_days for b in P_days for c in P_days 
            if len({a,b,c})==3 and sorted([a,b,c])==sorted(P_days)])
    s = Or([And(S1==a, S2==b, S3==c) for a in S_days for b in S_days for c in S_days 
            if len({a,b,c})==3 and sorted([a,b,c])==sorted(S_days)])
    return And(o, p, s)

# Option A: O: Mon, Wed, Thu (0,2,3); P: Wed, Thu, Fri (2,3,4); S: Mon, Thu, Fri (0,3,4)
opt_a = option_constr([0,2,3], [2,3,4], [0,3,4])

# Option B: O: Mon, Tue, Thu (0,1,3); P: Tue, Wed, Thu (1,2,3); S: Mon, Wed, Thu (0,2,3)
opt_b = option_constr([0,1,3], [1,2,3], [0,2,3])

# Option C: O: Tue, Wed, Thu (1,2,3); P: Wed, Thu, Fri (2,3,4); S: Tue, Thu, Fri (1,3,4)
opt_c = option_constr([1,2,3], [2,3,4], [1,3,4])

# Option D: O: Mon, Tue, Thu (0,1,3); P: Mon, Wed, Thu (0,2,3); S: Mon, Thu, Fri (0,3,4)
opt_d = option_constr([0,1,3], [0,2,3], [0,3,4])

# Option E: O: Mon, Thu, Fri (0,3,4); P: Tue, Wed, Thu (1,2,3); S: Mon, Thu, Fri (0,3,4)
opt_e = option_constr([0,3,4], [1,2,3], [0,3,4])

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    s = Solver()
    s.add(solver_base.assertions())
    s.add(constr)
    if s.check() == sat:
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