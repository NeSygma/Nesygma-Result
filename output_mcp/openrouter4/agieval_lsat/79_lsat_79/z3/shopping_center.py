from z3 import *

# Seven positions 1..7
# Businesses: optometrist, pharmacy, two restaurants, shoe store, toy store, veterinarian

optom = Int('optom')
pharm = Int('pharm')
rest1 = Int('rest1')
rest2 = Int('rest2')
shoe = Int('shoe')
toy = Int('toy')
vet = Int('vet')
all_vars = [optom, pharm, rest1, rest2, shoe, toy, vet]

solver = Solver()

# Domain: each position 1..7
for v in all_vars:
    solver.add(v >= 1, v <= 7)

# All distinct positions
solver.add(Distinct(all_vars))

# Constraint 1: Pharmacy at one end, one of the restaurants at the other
solver.add(Or(
    And(pharm == 1, Or(rest1 == 7, rest2 == 7)),
    And(pharm == 7, Or(rest1 == 1, rest2 == 1))
))

# Constraint 2: Two restaurants separated by at least 2 other businesses
# |rest1 - rest2| >= 3
solver.add(Or(rest1 - rest2 >= 3, rest2 - rest1 >= 3))

# Constraint 3: Pharmacy next to optometrist or veterinarian
# |pharm - optom| == 1 OR |pharm - vet| == 1
solver.add(Or(
    Or(pharm - optom == 1, optom - pharm == 1),
    Or(pharm - vet == 1, vet - pharm == 1)
))

# Constraint 4: Toy store cannot be next to veterinarian
# |toy - vet| != 1
solver.add(Not(Or(toy - vet == 1, vet - toy == 1)))

# Additional condition: optometrist next to shoe store
solver.add(Or(optom - shoe == 1, shoe - optom == 1))

# Now we need to find the flanking businesses.
# The O-S pair is two adjacent positions. The flanking businesses are
# the ones at positions min(pos(O),pos(S))-1 and max(pos(O),pos(S))+1.
# We need to ensure both sides exist (the pair is not at an end).

# Let's enumerate all valid solutions and see what the flanking businesses are
solutions_data = []
while solver.check() == sat:
    m = solver.model()
    o_pos = m[optom].as_long()
    p_pos = m[pharm].as_long()
    r1_pos = m[rest1].as_long()
    r2_pos = m[rest2].as_long()
    s_pos = m[shoe].as_long()
    t_pos = m[toy].as_long()
    v_pos = m[vet].as_long()
    
    # Determine O-S pair bounds
    left_pos = min(o_pos, s_pos)
    right_pos = max(o_pos, s_pos)
    
    # Only consider cases where both sides exist (pair not at edges)
    if left_pos > 1 and right_pos < 7:
        left_flank = None
        right_flank = None
        # Left flank business (at left_pos - 1)
        lf_pos = left_pos - 1
        for name, pos in [('optom', o_pos), ('pharm', p_pos), ('rest1', r1_pos), ('rest2', r2_pos),
                          ('shoe', s_pos), ('toy', t_pos), ('vet', v_pos)]:
            if pos == lf_pos:
                left_flank = name
                break
        
        # Right flank business (at right_pos + 1)
        rf_pos = right_pos + 1
        for name, pos in [('optom', o_pos), ('pharm', p_pos), ('rest1', r1_pos), ('rest2', r2_pos),
                          ('shoe', s_pos), ('toy', t_pos), ('vet', v_pos)]:
            if pos == rf_pos:
                right_flank = name
                break
        
        solutions_data.append((left_flank, right_flank, o_pos, p_pos, r1_pos, r2_pos, s_pos, t_pos, v_pos))
    
    # Block this solution
    solver.add(Or([v != m.eval(v, model_completion=True) for v in all_vars]))

print(f"Found {len(solutions_data)} valid configurations with O-S pair flanked on both sides.")
print()

# Analyze flanking pairs
flank_sets = set()
for left, right, o, p, r1, r2, s, t, v in solutions_data:
    flank_pair = tuple(sorted([left, right]))
    flank_sets.add(flank_pair)
    print(f"O={o} S={s} | Left={left} Right={right} | P={p} R1={r1} R2={r2} T={t} V={v}")

print()
print("Distinct flanking pairs found:")
for fp in sorted(flank_sets):
    print(f"  {fp}")

# Now check each answer choice
# The flanking businesses are: one on left side, one on right side.
# We need to see what they "must be" - i.e., what is always true across all solutions.

# Let's check which answer choices are ALWAYS true (for all solutions)
# Since the question says "must be", we need to find what's common across ALL solutions.

# Compute all possible left flank businesses and right flank businesses
left_set = set()
right_set = set()
for left, right, _, _, _, _, _, _, _ in solutions_data:
    left_set.add(left)
    right_set.add(right)

print()
print(f"Possible left flank businesses: {left_set}")
print(f"Possible right flank businesses: {right_set}")

# Check each option
# A: pharmacy and a restaurant -> the pair must be {pharm, rest1} or {pharm, rest2}
# B: pharmacy and toy store -> the pair must be {pharm, toy}
# C: two restaurants -> the pair must be {rest1, rest2}
# D: a restaurant and toy store -> {rest1/rest2, toy}
# E: a restaurant and veterinarian -> {rest1/rest2, vet}

def is_restaurant(name):
    return name in ('rest1', 'rest2')

def has_restaurant(pair_set):
    return any(is_restaurant(n) for n in pair_set)

def check_option(pair_set):
    """Check if for ALL solutions, the flanking pair matches the given set description."""
    all_match = True
    for left, right, _, _, _, _, _, _, _ in solutions_data:
        actual_pair = {left, right}
        if actual_pair != pair_set:
            all_match = False
            break
    return all_match

# Since we might have multiple solution types, let's check what MUST be common
# across all solutions. If a specific pair appears in ALL solutions, that "must be" correct.

print()
print("Checking each option (must be true across all configs):")
print()

# Test each option by seeing if the pair described ALWAYS holds
# Option A: {pharm, restaurant}
option_a_matches = all(
    ('pharm' in {l, r} and is_restaurant(l if r != l else r)) or 
    ('pharm' in {l, r} and is_restaurant(r if l != r else l))
    for l, r, _, _, _, _, _, _, _ in solutions_data
)
print(f"Option A (pharmacy and a restaurant): {option_a_matches}")

# Option B: {pharm, toy}
option_b_matches = all(
    'pharm' in {l, r} and 'toy' in {l, r}
    for l, r, _, _, _, _, _, _, _ in solutions_data
)
print(f"Option B (pharmacy and toy store): {option_b_matches}")

# Option C: {rest1, rest2}
option_c_matches = all(
    (l == 'rest1' and r == 'rest2') or (l == 'rest2' and r == 'rest1')
    for l, r, _, _, _, _, _, _, _ in solutions_data
)
print(f"Option C (two restaurants): {option_c_matches}")

# Option D: {restaurant, toy}
option_d_matches = all(
    (is_restaurant(l) and r == 'toy') or (is_restaurant(r) and l == 'toy')
    for l, r, _, _, _, _, _, _, _ in solutions_data
)
print(f"Option D (restaurant and toy store): {option_d_matches}")

# Option E: {restaurant, vet}
option_e_matches = all(
    (is_restaurant(l) and r == 'vet') or (is_restaurant(r) and l == 'vet')
    for l, r, _, _, _, _, _, _, _ in solutions_data
)
print(f"Option E (restaurant and veterinarian): {option_e_matches}")

# Now also use the LSAT skeleton approach
print()
print("=== LSAT Multiple Choice Skeleton ===")
solver2 = Solver()

# Re-add all constraints
for v in all_vars:
    solver2.add(v >= 1, v <= 7)
solver2.add(Distinct(all_vars))
solver2.add(Or(
    And(pharm == 1, Or(rest1 == 7, rest2 == 7)),
    And(pharm == 7, Or(rest1 == 1, rest2 == 1))
))
solver2.add(Or(rest1 - rest2 >= 3, rest2 - rest1 >= 3))
solver2.add(Or(
    Or(pharm - optom == 1, optom - pharm == 1),
    Or(pharm - vet == 1, vet - pharm == 1)
))
solver2.add(Not(Or(toy - vet == 1, vet - toy == 1)))
solver2.add(Or(optom - shoe == 1, shoe - optom == 1))

# For each option, test if it MUST be true by checking if its negation is possible
# The flanking businesses: at positions left_pos-1 and right_pos+1 where left_pos = min(O,S), right_pos = max(O,S)
left_pos = If(optom < shoe, optom, shoe)
right_pos = If(optom < shoe, shoe, optom)
left_flank_pos = left_pos - 1
right_flank_pos = right_pos + 1

# Ensure both sides exist
solver2.add(left_pos > 1)
solver2.add(right_pos < 7)

# For "must be" logic, we check: given the base constraints (including O next to S),
# is it possible that the answer choice is FALSE?
# If the answer choice being false is unsat, then it MUST be true.

# Let me try a different approach that's more aligned with the skeleton.
# For each option, add it as a constraint and check if sat.
# But since the question asks "must be", we need to be careful.

# Let me use the theorem-proving-like approach:
# For each option, try to prove that it's necessarily true.
# Option X is "must be true" if: base constraints + NOT(option X) is unsat.

# Define what each option means in terms of flanking businesses
# We need a function that tells us what the flanking businesses are
# Let's use Z3 variables for the flanking businesses

left_biz = Int('left_biz')  # 0=optom, 1=pharm, 2=rest1, 3=rest2, 4=shoe, 5=toy, 6=vet
right_biz = Int('right_biz')

# Map business to its position
# We need to figure out which business is at left_pos-1 and which is at right_pos+1
# This is getting complex. Let me try a simpler constrained approach.

# Let me check each option by creating a separate solver for each
print("\n=== Testing each option for 'must be true' ===")
print("(Checking if NOT(option) is inconsistent with base constraints)")

# Actually, let me just go with: which option is uniquely SAT when added as an additional constraint?
# Since the skeleton approach says to find which option is SAT.

# Let me create constraints for each option about the flanking businesses
# and test them.

print("\n=== Let me just enumerate and see the pattern ===")
# Let me redefine and enumerate all valid configurations including edge cases