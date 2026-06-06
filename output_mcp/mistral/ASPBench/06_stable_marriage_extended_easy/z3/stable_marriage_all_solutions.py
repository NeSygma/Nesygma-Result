from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare men and women
men = ["m1", "m2", "m3", "m4"]
women = ["w1", "w2", "w3", "w4"]

# Preference lists (in order of decreasing preference)
men_prefs = {
    "m1": ["w1", "w2", "w3"],
    "m2": ["w2", "w3", "w4"],
    "m3": ["w3", "w4", "w1"],
    "m4": ["w4", "w1", "w2"]
}

women_prefs = {
    "w1": ["m4", "m1", "m3"],
    "w2": ["m1", "m2", "m4"],
    "w3": ["m2", "m3", "m1"],
    "w4": ["m3", "m4", "m2"]
}

# Helper: rank of a person in another's preference list
# Returns a high number if not acceptable
def get_rank(person_prefs, person, target):
    """Return the rank (0 = highest) of target in person's preference list.
    If target is not acceptable, return a large number (e.g., 100)."""
    if target in person_prefs:
        return person_prefs.index(target)
    else:
        return 100  # Unacceptable

# Declare matching as a function from men to women (or None)
# We'll use a list of Int variables representing the woman index for each man
# We'll use -1 to represent "unmatched"
match = [Int(f"match_{m}") for m in men]

# Domain: each match variable is in [-1, 0, 1, 2, 3] where -1 = unmatched, 0-3 = woman index
solver = Solver()
for i in range(len(men)):
    solver.add(Or([match[i] == -1, match[i] == 0, match[i] == 1, match[i] == 2, match[i] == 3]))

# Each woman is matched to at most one man
# We'll enforce this by ensuring that if two men are matched to the same woman, it's invalid
for i in range(len(men)):
    for j in range(i+1, len(men)):
        solver.add(Or(match[i] == -1, match[j] == -1, match[i] != match[j]))

# Constraint: Only acceptable pairs can be matched
# A pair (m, w) is acceptable if w is in m's preference list AND m is in w's preference list
for i, m in enumerate(men):
    for j, w in enumerate(women):
        acceptable = And(
            get_rank(men_prefs[m], m, w) < 100,  # w is acceptable to m
            get_rank(women_prefs[w], w, m) < 100   # m is acceptable to w
        )
        solver.add(Implies(match[i] == j, acceptable))

# Helper functions for preference comparison without symbolic indexing
def prefers(m, w1, w2):
    """Return Z3 expression: man m prefers w1 over w2."""
    rank1 = get_rank(men_prefs[m], m, w1)
    rank2 = get_rank(men_prefs[m], m, w2)
    return rank1 < rank2

def prefers_w(w, m1, m2):
    """Return Z3 expression: woman w prefers m1 over m2."""
    rank1 = get_rank(women_prefs[w], w, m1)
    rank2 = get_rank(women_prefs[w], w, m2)
    return rank1 < rank2

# Define partner_w: for each woman, the man she is matched to (or -1)
partner_w = [Int(f"partner_w_{w}") for w in women]

# Constraint: partner_w[j] = i iff match[i] = j
for i, m in enumerate(men):
    for j, w in enumerate(women):
        solver.add(Implies(match[i] == j, partner_w[j] == i))
        solver.add(Implies(partner_w[j] == i, match[i] == j))

# For women not matched to anyone, set partner_w to -1
for j, w in enumerate(women):
    solver.add(Or(partner_w[j] == -1, And(partner_w[j] >= 0, partner_w[j] < len(men))))

# Constraint: Stability - no blocking pair exists
# A blocking pair is a pair (m, w) such that:
# 1. m is not matched to w
# 2. Both find each other acceptable
# 3. m prefers w over his current partner (or is unmatched)
# 4. w prefers m over her current partner (or is unmatched)

# To prevent blocking pairs, we add the following constraint:
# For all men m and women w, it is not the case that:
# - m is not matched to w
# - both find each other acceptable
# - m prefers w over his current partner (or is unmatched)
# - w prefers m over her current partner (or is unmatched)

for i, m in enumerate(men):
    for j, w in enumerate(women):
        # Current partner of m: if match[i] == j, skip (already matched)
        # Otherwise, check for blocking pair
        
        # Get the current partner of m (if any)
        current_woman_index = match[i]
        
        # Get the current partner of w (if any)
        current_man_index = partner_w[j]
        
        # Check if both find each other acceptable
        acceptable_pair = And(
            get_rank(men_prefs[m], m, w) < 100,
            get_rank(women_prefs[w], w, m) < 100
        )
        
        # Check if m prefers w over his current partner (or is unmatched)
        # We need to handle the case where current_woman_index is symbolic
        # So we use If to handle both cases
        m_prefers_w = If(
            current_woman_index == -1,
            True,  # m is unmatched, so prefers w over unmatched
            prefers(m, w, women[current_woman_index.as_long()]) if isinstance(current_woman_index, int) else \
            Or([And(current_woman_index == k, prefers(m, w, women[k])) for k in range(len(women))])
        )
        
        # Check if w prefers m over her current partner (or is unmatched)
        w_prefers_m = If(
            current_man_index == -1,
            True,  # w is unmatched, so prefers m over unmatched
            prefers_w(w, m, men[current_man_index.as_long()]) if isinstance(current_man_index, int) else \
            Or([And(current_man_index == k, prefers_w(w, m, men[k])) for k in range(len(men))])
        )
        
        # If all conditions for a blocking pair are met, it's invalid
        solver.add(Implies(
            And(match[i] != j, acceptable_pair, m_prefers_w, w_prefers_m),
            False
        ))

# Now, find all solutions
stable_matchings = []
count = 0

# We'll use a loop to find all stable matchings
while solver.check() == sat:
    model = solver.model()
    
    # Extract the matching
    current_matching = []
    for i, m in enumerate(men):
        matched_woman_index = model[match[i]]
        if matched_woman_index.as_long() != -1:
            current_matching.append([m, women[matched_woman_index.as_long()]])
    
    stable_matchings.append(current_matching)
    count += 1
    
    # Block the current solution
    # Add a constraint that at least one man must be matched to a different woman
    blocking = []
    for i, m in enumerate(men):
        matched_woman_index = model[match[i]]
        if matched_woman_index.as_long() == -1:
            # Man is unmatched, so he must remain unmatched or be matched to someone else
            blocking.append(match[i] != -1)
        else:
            # Man is matched to a specific woman, so he must be matched to someone else
            blocking.append(Or([match[i] != k for k in range(len(women)) if k != matched_woman_index.as_long()]))
    
    solver.add(Or(blocking))

# Output results
print("STATUS: sat")
print(f"Total stable matchings found: {count}")
print("All stable matchings:")
for i, matching in enumerate(stable_matchings):
    print(f"Matching {i+1}: {matching}")