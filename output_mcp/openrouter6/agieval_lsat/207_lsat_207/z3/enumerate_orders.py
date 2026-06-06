from itertools import permutations

# singers order: [K, L, T, W, Y, Z]
singers = ['K', 'L', 'T', 'W', 'Y', 'Z']

def satisfies_base(pos):
    # pos is a tuple of positions for K, L, T, W, Y, Z in that order
    pK, pL, pT, pW, pY, pZ = pos
    # distinct positions 1..6
    if len(set(pos)) != 6:
        return False
    # fourth audition cannot be recorded
    if pK == 4 or pL == 4:
        return False
    # fifth audition must be recorded
    if not (pK == 5 or pL == 5):
        return False
    # Kammer earlier than Trillo
    if not (pK < pT):
        return False
    # Zinn earlier than Yoshida
    if not (pZ < pY):
        return False
    return True

def satisfies_original(pos):
    pK, pL, pT, pW, pY, pZ = pos
    # Waite earlier than both recorded auditions (K and L)
    return pW < pK and pW < pL

def satisfies_option_A(pos):
    pK, pL, pT, pW, pY, pZ = pos
    # Zinn earlier than Waite
    if not (pZ < pW):
        return False
    # All others later than Waite
    if not (pK > pW and pL > pW and pT > pW and pY > pW):
        return False
    return True

def satisfies_option_B(pos):
    pK, pL, pT, pW, pY, pZ = pos
    # Waite immediately before or after Zinn
    return abs(pW - pZ) == 1

def satisfies_option_C(pos):
    pK, pL, pT, pW, pY, pZ = pos
    # Waite earlier than Lugo
    return pW < pL

def satisfies_option_D(pos):
    pK, pL, pT, pW, pY, pZ = pos
    # Waite first or second
    return pW == 1 or pW == 2

def satisfies_option_E(pos):
    pK, pL, pT, pW, pY, pZ = pos
    # First audition cannot be recorded
    return pK != 1 and pL != 1

# Generate all permutations of positions 1..6 assigned to K,L,T,W,Y,Z
all_perms = permutations(range(1,7))
base_solutions = []
for perm in all_perms:
    if satisfies_base(perm) and satisfies_original(perm):
        base_solutions.append(perm)

print(f"Number of solutions with original condition: {len(base_solutions)}")
# Print first few solutions for sanity
for i, sol in enumerate(base_solutions[:5]):
    print(f"  {i+1}: K={sol[0]}, L={sol[1]}, T={sol[2]}, W={sol[3]}, Y={sol[4]}, Z={sol[5]}")

# Now check each option
options = {
    'A': satisfies_option_A,
    'B': satisfies_option_B,
    'C': satisfies_option_C,
    'D': satisfies_option_D,
    'E': satisfies_option_E,
}

equivalent_options = []
for letter, func in options.items():
    option_solutions = []
    for perm in all_perms:
        if satisfies_base(perm) and func(perm):
            option_solutions.append(perm)
    # Compare sets
    if set(base_solutions) == set(option_solutions):
        equivalent_options.append(letter)
        print(f"Option {letter} yields same set of solutions ({len(option_solutions)} solutions)")
    else:
        print(f"Option {letter} yields different set ({len(option_solutions)} solutions)")

print("\nEquivalent options:", equivalent_options)

if len(equivalent_options) == 1:
    print("STATUS: sat")
    print(f"answer:{equivalent_options[0]}")
elif len(equivalent_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {equivalent_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")