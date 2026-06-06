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

print("Original solutions (W < K and W < L):")
for sol in sorted(original):
    print(f"  {sol}")

print(f"\nTotal: {len(original)}")

# Option D: Waite is first or second
opt_d = get_solutions([Or(W == 1, W == 2)])
print(f"\nOption D solutions (W==1 or W==2):")
for sol in sorted(opt_d):
    print(f"  {sol}")
print(f"Total: {len(opt_d)}")

# Check: is original a subset of opt_d?
print(f"\nOriginal subset of D: {original.issubset(opt_d)}")
print(f"D subset of original: {opt_d.issubset(original)}")

# Option E: First audition cannot be recorded
opt_e = get_solutions([K != 1, L != 1])
print(f"\nOption E solutions (K!=1 and L!=1):")
for sol in sorted(opt_e):
    print(f"  {sol}")
print(f"Total: {len(opt_e)}")
print(f"Original subset of E: {original.issubset(opt_e)}")

# Let me check: in the original, what positions can W take?
w_positions = set()
for sol in original:
    w_positions.add(sol.index('W') + 1)
print(f"\nW positions in original: {sorted(w_positions)}")

# In the original, what positions can K take?
k_positions = set()
for sol in original:
    k_positions.add(sol.index('K') + 1)
print(f"K positions in original: {sorted(k_positions)}")

# In the original, what positions can L take?
l_positions = set()
for sol in original:
    l_positions.add(sol.index('L') + 1)
print(f"L positions in original: {sorted(l_positions)}")