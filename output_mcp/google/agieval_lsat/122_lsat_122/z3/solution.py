from itertools import permutations

# Bands
bands = ['U', 'V', 'W', 'X', 'Y', 'Z']
# Slots 0-5 (representing 1-6)
all_perms = list(permutations(range(6)))

def get_band_pos(perm, band_name):
    # Map band names to indices 0-5
    mapping = {'U': 0, 'V': 1, 'W': 2, 'X': 3, 'Y': 4, 'Z': 5}
    # perm is a tuple of band indices (0-5)
    # We need to find where the band is in the permutation
    # Actually, let's redefine: perm[slot] = band_index
    # So we need to find the slot index for a given band_index
    band_idx = mapping[band_name]
    return perm.index(band_idx)

def check_constraints(perm, base_constraints, extra_constraints):
    # base_constraints: V < Z, U in {3, 4, 5}, Y in {0, 1, 2}
    # (using 0-5 for slots)
    
    # V < Z
    if not (get_band_pos(perm, 'V') < get_band_pos(perm, 'Z')):
        return False
    # U in {3, 4, 5}
    if not (get_band_pos(perm, 'U') >= 3):
        return False
    # Y in {0, 1, 2}
    if not (get_band_pos(perm, 'Y') <= 2):
        return False
        
    # extra_constraints
    return extra_constraints(perm)

# Original extra constraints: W < X and Z < X
def orig_extra(perm):
    return (get_band_pos(perm, 'W') < get_band_pos(perm, 'X')) and \
           (get_band_pos(perm, 'Z') < get_band_pos(perm, 'X'))

# Generate S_orig
S_orig = set()
for p in all_perms:
    if check_constraints(p, None, orig_extra):
        S_orig.add(p)

# Options
def opt_A(perm):
    # Only Uneasy can perform in a later slot than Xpert.
    # This means for all bands B != U, pos(B) < pos(X)
    # Wait, "Only Uneasy can perform in a later slot than Xpert"
    # means if pos(B) > pos(X), then B must be U.
    # So for all B in {V, W, Y, Z}, pos(B) < pos(X).
    for b in ['V', 'W', 'Y', 'Z']:
        if not (get_band_pos(perm, b) < get_band_pos(perm, 'X')):
            return False
    return True

def opt_B(perm):
    # Vegemite performs in an earlier slot than Wellspring, 
    # which performs in an earlier slot than Zircon.
    # V < W < Z
    return (get_band_pos(perm, 'V') < get_band_pos(perm, 'W')) and \
           (get_band_pos(perm, 'W') < get_band_pos(perm, 'Z'))

def opt_C(perm):
    # Vegemite and Wellspring each perform in an earlier slot than Xpert.
    # V < X and W < X
    return (get_band_pos(perm, 'V') < get_band_pos(perm, 'X')) and \
           (get_band_pos(perm, 'W') < get_band_pos(perm, 'X'))

def opt_D(perm):
    # Xpert performs either immediately before or immediately after Uneasy.
    # |pos(X) - pos(U)| == 1
    return abs(get_band_pos(perm, 'X') - get_band_pos(perm, 'U')) == 1

def opt_E(perm):
    # Xpert performs in either slot five or slot six.
    # pos(X) in {4, 5}
    return get_band_pos(perm, 'X') >= 4

options = [('A', opt_A), ('B', opt_B), ('C', opt_C), ('D', opt_D), ('E', opt_E)]

for name, func in options:
    S_new = set()
    for p in all_perms:
        if check_constraints(p, None, func):
            S_new.add(p)
    if S_new == S_orig:
        print(f"STATUS: sat")
        print(f"answer:{name}")
        break
else:
    print("STATUS: unsat")