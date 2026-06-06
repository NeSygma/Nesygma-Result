from z3 import *

def get_solutions(extra_constraints):
    """Get all valid orderings with given extra constraints (replacing condition 3)"""
    solutions = []
    K, L, T, W, Y, Z = Ints('K L T W Y Z')
    singers = [K, L, T, W, Y, Z]
    names = ['K', 'L', 'T', 'W', 'Y', 'Z']
    
    s = Solver()
    
    for singer in singers:
        s.add(singer >= 1, singer <= 6)
    s.add(Distinct(singers))
    
    # Condition 1: Position 4 cannot be recorded (K and L are recorded)
    s.add(K != 4)
    s.add(L != 4)
    
    # Condition 2: Position 5 must be recorded
    s.add(Or(K == 5, L == 5))
    
    # Condition 4: Kammer before Trillo
    s.add(K < T)
    
    # Condition 5: Zinn before Yoshida
    s.add(Z < Y)
    
    for c in extra_constraints:
        s.add(c)
    
    while s.check() == sat:
        m = s.model()
        order = [0]*6
        for i in range(6):
            pos = m[singers[i]].as_long()
            order[pos-1] = names[i]
        solutions.append(tuple(order))
        s.add(Or([singer != m[singer] for singer in singers]))
    
    return set(solutions)

K, L, T, W, Y, Z = Ints('K L T W Y Z')

# Original condition 3: Waite before both Kammer and Lugo
original = get_solutions([W < K, W < L])
print(f"Original: {len(original)} solutions")

# Option A: Zinn's audition is the only one that can take place earlier than Waite's
# This means: Z < W, and no other singer is before W
# So W must be position 2, Z must be position 1
opt_a = get_solutions([Z == 1, W == 2])
print(f"Option A (Z=1, W=2): {len(opt_a)} solutions")
print(f"  Original == A: {original == opt_a}")

# Option B: Waite's audition must take place either immediately before or immediately after Zinn's
opt_b = get_solutions([Or(W == Z + 1, W == Z - 1)])
print(f"Option B (|W-Z|=1): {len(opt_b)} solutions")
print(f"  Original == B: {original == opt_b}")

# Option C: Waite's audition must take place earlier than Lugo's
opt_c = get_solutions([W < L])
print(f"Option C (W < L): {len(opt_c)} solutions")
print(f"  Original == C: {original == opt_c}")

# Option D: Waite's audition must be either first or second
opt_d = get_solutions([Or(W == 1, W == 2)])
print(f"Option D (W=1 or W=2): {len(opt_d)} solutions")
print(f"  Original == D: {original == opt_d}")

# Option E: The first audition cannot be recorded
opt_e = get_solutions([K != 1, L != 1])
print(f"Option E (K!=1, L!=1): {len(opt_e)} solutions")
print(f"  Original == E: {original == opt_e}")

# Let's also check: in the original, what positions can W take?
w_positions = set()
for sol in original:
    w_positions.add(sol[4])  # W is at index 4 in names
print(f"\nIn original, W can be at positions: {sorted(w_positions)}")

# Check what's extra in D
extra_d = opt_d - original
print(f"\nExtra in D but not in original ({len(extra_d)}):")
for sol in sorted(extra_d)[:10]:
    print(f"  {sol}")

# Check what's extra in E
extra_e = opt_e - original
print(f"\nExtra in E but not in original ({len(extra_e)}):")
for sol in sorted(extra_e)[:10]:
    print(f"  {sol}")

# Check what's missing in A
missing_a = original - opt_a
print(f"\nMissing in A but in original ({len(missing_a)}):")
for sol in sorted(missing_a)[:10]:
    print(f"  {sol}")

# Check what's missing in B
missing_b = original - opt_b
print(f"\nMissing in B but in original ({len(missing_b)}):")
for sol in sorted(missing_b)[:10]:
    print(f"  {sol}")

# Check what's missing in C
missing_c = original - opt_c
print(f"\nMissing in C but in original ({len(missing_c)}):")
for sol in sorted(missing_c)[:10]:
    print(f"  {sol}")

# Check what's missing in D
missing_d = original - opt_d
print(f"\nMissing in D but in original ({len(missing_d)}):")
for sol in sorted(missing_d)[:10]:
    print(f"  {sol}")

# Check what's missing in E
missing_e = original - opt_e
print(f"\nMissing in E but in original ({len(missing_e)}):")
for sol in sorted(missing_e)[:10]:
    print(f"  {sol}")