from z3 import *

def get_solutions(extra_constraints):
    """Get all valid orderings with given extra constraints (replacing condition 3)"""
    solutions = []
    K, L, T, W, Y, Z = Ints('K L T W Y Z')
    singers = [K, L, T, W, Y, Z]
    names = ['K', 'L', 'T', 'W', 'Y', 'Z']
    
    s = Solver()
    
    # Each singer in position 1-6
    for singer in singers:
        s.add(singer >= 1, singer <= 6)
    
    # All different positions
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
    
    # Add the extra constraints (replacing condition 3)
    for c in extra_constraints:
        s.add(c)
    
    while s.check() == sat:
        m = s.model()
        sol = tuple(sorted([(names[i], m[singers[i]].as_long()) for i in range(6)], key=lambda x: x[1]))
        solutions.append(sol)
        s.add(Or([singer != m[singer] for singer in singers]))
    
    return set(solutions)

K, L, T, W, Y, Z = Ints('K L T W Y Z')

# Original condition 3: Waite before both Kammer and Lugo
original = get_solutions([W < K, W < L])

print(f"Original solutions count: {len(original)}")

# Option A: Zinn is the only one before Waite
# Z < W, K > W, L > W, T > W, Y > W
opt_a = get_solutions([Z < W, K > W, L > W, T > W, Y > W])
print(f"Option A solutions count: {len(opt_a)}")
print(f"Option A matches original: {opt_a == original}")

# Option B: |W - Z| == 1 (immediately before or after)
opt_b = get_solutions([Or(W - Z == 1, Z - W == 1)])
print(f"Option B solutions count: {len(opt_b)}")
print(f"Option B matches original: {opt_b == original}")

# Option C: Waite before Lugo
opt_c = get_solutions([W < L])
print(f"Option C solutions count: {len(opt_c)}")
print(f"Option C matches original: {opt_c == original}")

# Option D: Waite is first or second
opt_d = get_solutions([Or(W == 1, W == 2)])
print(f"Option D solutions count: {len(opt_d)}")
print(f"Option D matches original: {opt_d == original}")

# Option E: First audition cannot be recorded
opt_e = get_solutions([K != 1, L != 1])
print(f"Option E solutions count: {len(opt_e)}")
print(f"Option E matches original: {opt_e == original}")

# Check which options match
matches = []
for letter, sol_set in [('A', opt_a), ('B', opt_b), ('C', opt_c), ('D', opt_d), ('E', opt_e)]:
    if sol_set == original:
        matches.append(letter)

print(f"\nMatching options: {matches}")

# Also check subset/superset relationships
for letter, sol_set in [('A', opt_a), ('B', opt_b), ('C', opt_c), ('D', opt_d), ('E', opt_e)]:
    is_subset = sol_set.issubset(original)
    is_superset = sol_set.issuperset(original)
    print(f"Option {letter}: subset={is_subset}, superset={is_superset}, equal={sol_set == original}")