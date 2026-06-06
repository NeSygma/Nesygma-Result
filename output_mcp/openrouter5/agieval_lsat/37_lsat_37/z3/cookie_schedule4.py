from z3 import *

# Let me re-read the problem more carefully.
# "Exactly three batches of each kind of cookie are made each week (Monday through Friday)"
# "each batch is made, from start to finish, on a single day"
# "No two batches of the same kind of cookie are made on the same day."
# "At least one batch of cookies is made on Monday."
# "The second batch of oatmeal cookies is made on the same day as the first batch of peanut butter cookies."
# "The second batch of sugar cookies is made on Thursday."

# The question asks: "Which one of the following could be a complete and accurate list of the days on which the batches of each kind of cookie are made?"

# So each option lists the days (not the order/batch number) for each kind.
# For example, option A says oatmeal: Monday, Wednesday, Thursday -- meaning the 3 oatmeal batches are made on Mon, Wed, Thu (in some order).

# Let me think about what constraints I might be missing.
# "At least one batch of cookies is made on Monday" - this is about ANY batch, not necessarily oatmeal.
# Also, there are exactly 9 batches total (3 kinds * 3 batches each), and 5 days.
# So some days have multiple batches.

# Let me also check: the second batch of oatmeal is on the same day as the first batch of peanut butter.
# And the second batch of sugar is on Thursday.

# Let me debug by checking each option individually.

def check_option(letter, O_days, P_days, S_days):
    O1, O2, O3 = Ints('O1 O2 O3')
    P1, P2, P3 = Ints('P1 P2 P3')
    S1, S2, S3 = Ints('S1 S2 S3')
    all_batches = [O1, O2, O3, P1, P2, P3, S1, S2, S3]
    
    s = Solver()
    for b in all_batches:
        s.add(b >= 0, b <= 4)
    
    s.add(Distinct(O1, O2, O3))
    s.add(Distinct(P1, P2, P3))
    s.add(Distinct(S1, S2, S3))
    
    s.add(Or([b == 0 for b in all_batches]))
    s.add(O2 == P1)
    s.add(S2 == 3)
    
    # The days for each kind must be exactly the given set
    s.add(And([Or([O1 == d, O2 == d, O3 == d]) for d in O_days]))
    s.add(And([Or([O1 == d, O2 == d, O3 == d]) for d in O_days]))
    # Actually, let me use a cleaner encoding:
    # The set {O1, O2, O3} must equal the set O_days
    s.add(And([Or([O1==d, O2==d, O3==d]) for d in O_days]))
    s.add(And([Or([d==O1, d==O2, d==O3]) for d in O_days]))
    
    s.add(And([Or([P1==d, P2==d, P3==d]) for d in P_days]))
    s.add(And([Or([d==P1, d==P2, d==P3]) for d in P_days]))
    
    s.add(And([Or([S1==d, S2==d, S3==d]) for d in S_days]))
    s.add(And([Or([d==S1, d==S2, d==S3]) for d in S_days]))
    
    res = s.check()
    if res == sat:
        m = s.model()
        print(f"Option {letter}: SAT")
        print(f"  O1={m[O1]}, O2={m[O2]}, O3={m[O3]}")
        print(f"  P1={m[P1]}, P2={m[P2]}, P3={m[P3]}")
        print(f"  S1={m[S1]}, S2={m[S2]}, S3={m[S3]}")
        return True
    else:
        print(f"Option {letter}: UNSAT")
        return False

# Option A: O: Mon(0), Wed(2), Thu(3); P: Wed(2), Thu(3), Fri(4); S: Mon(0), Thu(3), Fri(4)
check_option("A", [0,2,3], [2,3,4], [0,3,4])
print()

# Option B: O: Mon(0), Tue(1), Thu(3); P: Tue(1), Wed(2), Thu(3); S: Mon(0), Wed(2), Thu(3)
check_option("B", [0,1,3], [1,2,3], [0,2,3])
print()

# Option C: O: Tue(1), Wed(2), Thu(3); P: Wed(2), Thu(3), Fri(4); S: Tue(1), Thu(3), Fri(4)
check_option("C", [1,2,3], [2,3,4], [1,3,4])
print()

# Option D: O: Mon(0), Tue(1), Thu(3); P: Mon(0), Wed(2), Thu(3); S: Mon(0), Thu(3), Fri(4)
check_option("D", [0,1,3], [0,2,3], [0,3,4])
print()

# Option E: O: Mon(0), Thu(3), Fri(4); P: Tue(1), Wed(2), Thu(3); S: Mon(0), Thu(3), Fri(4)
check_option("E", [0,3,4], [1,2,3], [0,3,4])