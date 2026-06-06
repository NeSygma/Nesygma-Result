from z3 import *

# We have 3 kinds: oatmeal (O), peanut butter (P), sugar (S)
# Each kind has 3 batches (first, second, third)
# Days: Monday=0, Tuesday=1, Wednesday=2, Thursday=3, Friday=4

O1, O2, O3 = Ints('O1 O2 O3')
P1, P2, P3 = Ints('P1 P2 P3')
S1, S2, S3 = Ints('S1 S2 S3')

all_batches = [O1, O2, O3, P1, P2, P3, S1, S2, S3]

solver = Solver()

# Domain: each batch day is Monday(0) through Friday(4)
for b in all_batches:
    solver.add(b >= 0, b <= 4)

# Condition 1: No two batches of the same kind are made on the same day.
solver.add(Distinct(O1, O2, O3))
solver.add(Distinct(P1, P2, P3))
solver.add(Distinct(S1, S2, S3))

# Condition 2: At least one batch of cookies is made on Monday.
solver.add(Or([b == 0 for b in all_batches]))

# Condition 3: The second batch of oatmeal cookies is made on the same day as the first batch of peanut butter cookies.
solver.add(O2 == P1)

# Condition 4: The second batch of sugar cookies is made on Thursday.
solver.add(S2 == 3)  # Thursday = 3

# Now let's think more carefully about what each option means.
# Each option gives a SET of days for each kind (unordered). The batches are ordered (first, second, third).
# So for oatmeal: Monday, Wednesday, Thursday means the three batches are on Mon, Wed, Thu in some order.
# But we also have the constraint O2 == P1 which relates specific batch numbers.

# Let me re-encode each option more carefully.
# For each option, the set of days for each kind is fixed. We need to check if there exists an assignment
# of which batch (1st, 2nd, 3rd) goes on which day that satisfies all constraints.

# Option A: oatmeal: {Mon, Wed, Thu}, peanut butter: {Wed, Thu, Fri}, sugar: {Mon, Thu, Fri}
# O days: 0,2,3 ; P days: 2,3,4 ; S days: 0,3,4
# S2 = 3 (Thu) - this is already in S's set, good.
# O2 == P1 - O2 must equal P1. So O2 and P1 must be the same day, which must be in both O's set and P's set.
# Intersection of O days {0,2,3} and P days {2,3,4} is {2,3}. So O2=P1 must be 2 or 3.

# Option B: O: {Mon, Tue, Thu} = {0,1,3}, P: {Tue, Wed, Thu} = {1,2,3}, S: {Mon, Wed, Thu} = {0,2,3}
# S2=3 is in S's set. O2=P1 must be in {0,1,3} ∩ {1,2,3} = {1,3}

# Option C: O: {Tue, Wed, Thu} = {1,2,3}, P: {Wed, Thu, Fri} = {2,3,4}, S: {Tue, Thu, Fri} = {1,3,4}
# S2=3 is in S's set. O2=P1 must be in {1,2,3} ∩ {2,3,4} = {2,3}

# Option D: O: {Mon, Tue, Thu} = {0,1,3}, P: {Mon, Wed, Thu} = {0,2,3}, S: {Mon, Thu, Fri} = {0,3,4}
# S2=3 is in S's set. O2=P1 must be in {0,1,3} ∩ {0,2,3} = {0,3}

# Option E: O: {Mon, Thu, Fri} = {0,3,4}, P: {Tue, Wed, Thu} = {1,2,3}, S: {Mon, Thu, Fri} = {0,3,4}
# S2=3 is in S's set. O2=P1 must be in {0,3,4} ∩ {1,2,3} = {3}

# Let me encode each option more carefully using permutations.

def days_set_constraint(vars, allowed_days):
    """The three batch days for a kind must be exactly the allowed set (as a set)."""
    # Each var must be in allowed_days
    c1 = And([Or([v == d for d in allowed_days]) for v in vars])
    # All distinct (already enforced globally)
    # The set of values must be exactly the allowed set - i.e., each allowed day is used by some batch
    c2 = And([Or([v == d for d in allowed_days]) for v in vars])
    c3 = And([Or([v == d for v in vars]) for d in allowed_days])
    return And(c1, c3)

# Actually, let me just use a simpler approach: for each option, the three days for each kind are fixed.
# So we just need to check if there's a bijection between batches and days for each kind.

# Let me use permutations explicitly.

def option_constraint(O_days, P_days, S_days):
    """O_days, P_days, S_days are lists of 3 days each."""
    # O1, O2, O3 must be a permutation of O_days
    o_constr = Or([And(O1==a, O2==b, O3==c) for a in O_days for b in O_days for c in O_days if len({a,b,c})==3])
    p_constr = Or([And(P1==a, P2==b, P3==c) for a in P_days for b in P_days for c in P_days if len({a,b,c})==3])
    s_constr = Or([And(S1==a, S2==b, S3==c) for a in S_days for b in S_days for c in S_days if len({a,b,c})==3])
    return And(o_constr, p_constr, s_constr)

# Option A
opt_a = option_constraint([0,2,3], [2,3,4], [0,3,4])
# Option B
opt_b = option_constraint([0,1,3], [1,2,3], [0,2,3])
# Option C
opt_c = option_constraint([1,2,3], [2,3,4], [1,3,4])
# Option D
opt_d = option_constraint([0,1,3], [0,2,3], [0,3,4])
# Option E
opt_e = option_constraint([0,3,4], [1,2,3], [0,3,4])

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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