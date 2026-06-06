from z3 import *

# Let me now systematically check each option.
# The question: which option, when substituted for "W < K and W < L", 
# produces the EXACT same set of possible orders?

# First, let me get the full set of original solutions.
K, L, T, W, Y, Z = Ints('K L T W Y Z')
singers = [K, L, T, W, Y, Z]
names = ['K', 'L', 'T', 'W', 'Y', 'Z']

s_orig = Solver()
s_orig.add(Distinct(singers))
for sv in singers:
    s_orig.add(sv >= 0, sv <= 5)
s_orig.add(K != 3)  # 4th cannot be recorded
s_orig.add(L != 3)  # 4th cannot be recorded
s_orig.add(Or(K == 4, L == 4))  # 5th must be recorded
s_orig.add(W < K)  # W earlier than recorded auditions
s_orig.add(W < L)  # W earlier than recorded auditions
s_orig.add(K < T)  # K earlier than T
s_orig.add(Z < Y)  # Z earlier than Y

orig_solutions = set()
while s_orig.check() == sat:
    m = s_orig.model()
    perm = tuple(m.eval(sv, model_completion=True).as_long() for sv in singers)
    order = ''.join(names[i] for i in sorted(range(6), key=lambda x: perm[x]))
    orig_solutions.add(order)
    s_orig.add(Or([sv != m.eval(sv, model_completion=True) for sv in singers]))

print("Original solutions:")
for sol in sorted(orig_solutions):
    print(' '.join(sol))
print(f"Total: {len(orig_solutions)}")
print()

# Now test each option
options = {
    "A": "Zinn's audition is the only one that can take place earlier than Waite's. (Z < W, and for all others: W < them)",
    "B": "Waite's audition must take place either immediately before or immediately after Zinn's.",
    "C": "Waite's audition must take place earlier than Lugo's.",
    "D": "Waite's audition must be either first or second.",
    "E": "The first audition cannot be recorded."
}

# Option A: Z < W, and W < K, W < L, W < T, W < Y
# "Zinn's audition is the only one that can take place earlier than Waite's."
# This means: Z < W, and for all others (K, L, T, Y), W < them.
def test_option(opt_constraints, label):
    s = Solver()
    s.add(Distinct(singers))
    for sv in singers:
        s.add(sv >= 0, sv <= 5)
    s.add(K != 3)
    s.add(L != 3)
    s.add(Or(K == 4, L == 4))
    s.add(K < T)
    s.add(Z < Y)
    for c in opt_constraints:
        s.add(c)
    
    solutions = set()
    while s.check() == sat:
        m = s.model()
        perm = tuple(m.eval(sv, model_completion=True).as_long() for sv in singers)
        order = ''.join(names[i] for i in sorted(range(6), key=lambda x: perm[x]))
        solutions.add(order)
        s.add(Or([sv != m.eval(sv, model_completion=True) for sv in singers]))
    
    print(f"Option {label}:")
    for sol in sorted(solutions):
        print(' '.join(sol))
    print(f"Total: {len(solutions)}")
    
    if solutions == orig_solutions:
        print(f"*** Option {label} MATCHES original! ***")
    else:
        extra = solutions - orig_solutions
        missing = orig_solutions - solutions
        if extra:
            print(f"  Extra solutions: {sorted(extra)}")
        if missing:
            print(f"  Missing solutions: {sorted(missing)}")
    print()
    return solutions == orig_solutions

# Option A: Z < W, and W < K, W < L, W < T, W < Y
test_option([Z < W, W < K, W < L, W < T, W < Y], "A")

# Option B: |W - Z| == 1 (immediately before or after)
test_option([Or(W - Z == 1, Z - W == 1)], "B")

# Option C: W < L (only Lugo, not Kammer)
test_option([W < L], "C")

# Option D: W == 0 or W == 1
test_option([Or(W == 0, W == 1)], "D")

# Option E: first audition (position 0) cannot be recorded -> K != 0 and L != 0
test_option([And(K != 0, L != 0)], "E")