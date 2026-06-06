from z3 import *

# Define men and women
men = ['m1', 'm2', 'm3', 'm4']
women = ['w1', 'w2', 'w3', 'w4']

# Men's preferences (lower number = more preferred)
men_prefs = {
    'm1': ['w1', 'w2', 'w3'],
    'm2': ['w2', 'w3', 'w4'],
    'm3': ['w3', 'w4', 'w1'],
    'm4': ['w4', 'w1', 'w2']
}

# Women's preferences (lower number = more preferred)
women_prefs = {
    'w1': ['m4', 'm1', 'm3'],
    'w2': ['m1', 'm2', 'm4'],
    'w3': ['m2', 'm3', 'm1'],
    'w4': ['m3', 'm4', 'm2']
}

# Create preference ranking dictionaries for quick lookup
men_rank = {}
for man in men:
    men_rank[man] = {}
    for idx, woman in enumerate(men_prefs[man]):
        men_rank[man][woman] = idx  # Lower index = more preferred

women_rank = {}
for woman in women:
    women_rank[woman] = {}
    for idx, man in enumerate(women_prefs[woman]):
        women_rank[woman][man] = idx  # Lower index = more preferred

# Create Boolean variables for each possible pair
match = {}
for man in men:
    for woman in women:
        match[(man, woman)] = Bool(f'match_{man}_{woman}')

solver = Solver()

# Constraint 1: Each man can be matched to at most one woman
for man in men:
    # At most one woman per man
    solver.add(AtMost([match[(man, woman)] for woman in women] + [1]))

# Constraint 2: Each woman can be matched to at most one man
for woman in women:
    # At most one man per woman
    solver.add(AtMost([match[(man, woman)] for man in men] + [1]))

# Constraint 3: Only acceptable pairs can be matched
# A pair is acceptable if both find each other acceptable (in their preference lists)
for man in men:
    for woman in women:
        man_accepts = woman in men_rank[man]
        woman_accepts = man in women_rank[woman]
        if not (man_accepts and woman_accepts):
            # If either doesn't find the other acceptable, they cannot be matched
            solver.add(Not(match[(man, woman)]))

# Constraint 4: Stability - No blocking pairs
# A blocking pair (m, w) exists if:
# 1. m and w are not currently matched to each other
# 2. Both find each other acceptable
# 3. m prefers w over his current partner (or is unmatched)
# 4. w prefers m over her current partner (or is unmatched)

# For each possible pair (m, w), ensure it's not a blocking pair
for m in men:
    for w in women:
        # Skip if they're already matched (that's fine)
        # We need to ensure that if they're not matched, they don't form a blocking pair
        
        # Condition: If m prefers w over his current partner AND w prefers m over her current partner,
        # then they must be matched to each other
        
        # Get m's current partner (if any)
        # We need to express: m prefers w over his current partner
        # This means: either m is unmatched, or his current partner is less preferred than w
        
        # For each man m and woman w, we need to ensure:
        # If (m prefers w over his current partner) AND (w prefers m over her current partner)
        # THEN (m and w are matched)
        
        # Let's express this more carefully:
        # For each man m and woman w (where w is acceptable to m and m is acceptable to w):
        # If m is matched to someone less preferred than w, AND w is matched to someone less preferred than m,
        # THEN m and w must be matched to each other
        
        # We'll use a helper function to express "m prefers w over his current partner"
        # This is tricky because we need to consider all possible current partners
        
        # Alternative approach: For each pair (m, w), ensure that if they're not matched,
        # then either m doesn't prefer w over his current partner OR w doesn't prefer m over her current partner
        
        # Let's build the condition more systematically:
        
        # For each man m and woman w (where both find each other acceptable):
        # If m is matched to some woman w' where w' != w, and m prefers w over w',
        # AND w is matched to some man m' where m' != m, and w prefers m over m',
        # THEN this would be a blocking pair, which is not allowed
        
        # So we need: NOT( (m prefers w over current) AND (w prefers m over current) AND (m and w not matched) )
        
        # Let's express "m prefers w over his current partner"
        # This means: either m is unmatched, OR his current partner is less preferred than w
        
        # We'll create a helper expression for each (m, w) pair
        m_prefers_w_over_current = []
        w_prefers_m_over_current = []
        
        # For m's current partner: if m is matched to w', then w' must not be less preferred than w
        # Actually, we need: if m is matched to w' and w' != w, then m does NOT prefer w over w'
        # Which means: either m is unmatched, or his current partner is w, or his current partner is more preferred than w
        
        # Let's build the condition for "m prefers w over his current partner"
        # This is true if: m is unmatched OR (m is matched to some w' where w' != w AND m prefers w over w')
        
        # We'll use a different approach: For each (m, w) pair, ensure that if they're not matched,
        # then at least one of these is true:
        # 1. m is matched to someone he prefers at least as much as w
        # 2. w is matched to someone she prefers at least as much as m
        
        # Let's build the condition for "m prefers w over his current partner"
        m_prefers_w = []
        for w_prime in women:
            if w_prime == w:
                continue
            if w_prime in men_rank[m]:
                # m prefers w over w' if w is more preferred (lower rank) than w'
                if w in men_rank[m]:
                    m_prefers_w.append(And(match[(m, w_prime)], men_rank[m][w] < men_rank[m][w_prime]))
        
        # If m is unmatched, he prefers w over being unmatched (we consider unmatched as least preferred)
        # Actually, we need to handle the case where m is unmatched
        # Let's add: if m is unmatched, then he prefers w over being unmatched
        # But we need to be careful: being unmatched is not in the preference list
        
        # Alternative: Let's define that being unmatched is worse than any acceptable partner
        # So if m is unmatched, he prefers any acceptable w over being unmatched
        
        # For the stability condition, we need to consider:
        # If m is unmatched AND w is acceptable to m, then m would prefer w over being unmatched
        # Similarly for w
        
        # Let's build the full stability condition for pair (m, w):
        # If m and w are not matched, then:
        # Either m is matched to someone he prefers at least as much as w
        # OR w is matched to someone she prefers at least as much as m
        # OR at least one of them doesn't find the other acceptable
        
        # But we already have the acceptability constraint, so we know both find each other acceptable
        
        # So for acceptable pairs (m, w):
        # If not matched[(m, w)], then:
        # Either m is matched to someone he prefers at least as much as w
        # OR w is matched to someone she prefers at least as much as m
        
        # Let's build "m is matched to someone he prefers at least as much as w"
        m_has_better_or_equal = []
        for w_prime in women:
            if w_prime in men_rank[m]:
                # If m is matched to w', and w' is at least as preferred as w
                if w in men_rank[m]:
                    # w' is at least as preferred as w if men_rank[m][w_prime] <= men_rank[m][w]
                    m_has_better_or_equal.append(And(match[(m, w_prime)], men_rank[m][w_prime] <= men_rank[m][w]))
        
        # Also consider if m is unmatched - but we need to handle this differently
        # Actually, if m is unmatched, he doesn't have a "current partner" to compare to
        # So we need to consider: if m is unmatched, then he would prefer w over being unmatched
        # So the condition "m is matched to someone he prefers at least as much as w" is false if m is unmatched
        
        # Similarly for w
        
        # Let's build "w is matched to someone she prefers at least as much as m"
        w_has_better_or_equal = []
        for m_prime in men:
            if m_prime in women_rank[w]:
                # If w is matched to m', and m' is at least as preferred as m
                if m in women_rank[w]:
                    # m' is at least as preferred as m if women_rank[w][m_prime] <= women_rank[w][m]
                    w_has_better_or_equal.append(And(match[(m_prime, w)], women_rank[w][m_prime] <= women_rank[w][m]))
        
        # Now, for acceptable pairs (m, w):
        if w in men_rank[m] and m in women_rank[w]:
            # If not matched to each other, then at least one must have a better/equal partner
            # OR one of them is unmatched (which means they would prefer each other)
            
            # Actually, we need to be more precise:
            # If m is unmatched, he prefers w over being unmatched
            # If w is unmatched, she prefers m over being unmatched
            # So if both are unmatched, they form a blocking pair
            
            # Let's express: if m and w are not matched, then:
            # Either m is matched to someone he prefers at least as much as w
            # OR w is matched to someone she prefers at least as much as m
            # OR at least one of them is unmatched (but then they would prefer each other)
            
            # Actually, the correct condition is:
            # If m is unmatched OR w is unmatched, then they would prefer each other
            # So we need to ensure that if either is unmatched, they must be matched to each other
            
            # Let's think differently: For stability, we need that there is no pair (m, w) such that:
            # 1. m and w are not matched to each other
            # 2. m prefers w over his current partner (or is unmatched)
            # 3. w prefers m over her current partner (or is unmatched)
            
            # So we need to ensure that for every pair (m, w):
            # NOT( (m prefers w over current) AND (w prefers m over current) AND (not matched to each other) )
            
            # Let's build "m prefers w over his current partner"
            # This means: either m is unmatched, OR his current partner is less preferred than w
            
            # For m being unmatched: we need to check if m is matched to anyone
            m_is_matched = Or([match[(m, w_prime)] for w_prime in women])
            
            # If m is matched, his current partner is some w' where match[(m, w')] is true
            # We need to express: if m is matched to w', then w' is not less preferred than w
            # Actually, we need: if m is matched to w' and w' != w, then m does NOT prefer w over w'
            
            # Let's build the condition for "m prefers w over his current partner"
            # This is true if: (m is unmatched) OR (m is matched to some w' where w' != w AND m prefers w over w')
            
            # For m unmatched: m is unmatched if NOT(m_is_matched)
            m_unmatched = Not(m_is_matched)
            
            # For m matched to someone less preferred than w:
            m_prefers_w_over_current = []
            for w_prime in women:
                if w_prime == w:
                    continue
                if w_prime in men_rank[m] and w in men_rank[m]:
                    # m prefers w over w' if men_rank[m][w] < men_rank[m][w_prime]
                    m_prefers_w_over_current.append(And(match[(m, w_prime)], men_rank[m][w] < men_rank[m][w_prime]))
            
            # m prefers w over current if: m_unmatched OR (any of the m_prefers_w_over_current conditions)
            m_prefers_w_condition = Or([m_unmatched] + m_prefers_w_over_current)
            
            # Similarly for w
            w_is_matched = Or([match[(m_prime, w)] for m_prime in men])
            w_unmatched = Not(w_is_matched)
            
            w_prefers_m_over_current = []
            for m_prime in men:
                if m_prime == m:
                    continue
                if m_prime in women_rank[w] and m in women_rank[w]:
                    # w prefers m over m' if women_rank[w][m] < women_rank[w][m_prime]
                    w_prefers_m_over_current.append(And(match[(m_prime, w)], women_rank[w][m] < women_rank[w][m_prime]))
            
            w_prefers_m_condition = Or([w_unmatched] + w_prefers_m_over_current)
            
            # Now, the stability condition: if both prefer each other over current, they must be matched
            # NOT( (m_prefers_w_condition AND w_prefers_m_condition AND Not(match[(m, w)])) )
            solver.add(Not(And(m_prefers_w_condition, w_prefers_m_condition, Not(match[(m, w)]))))

# Now we need to find all stable matchings
# We'll use enumeration by blocking previous solutions

solutions = []
decision_vars = [match[(m, w)] for m in men for w in women]

while solver.check() == sat:
    model = solver.model()
    
    # Extract the matching from the model
    current_matching = []
    for m in men:
        for w in women:
            if is_true(model[match[(m, w)]]):
                current_matching.append([m, w])
    
    solutions.append(current_matching)
    
    # Block this solution by adding a constraint that at least one variable must be different
    blocking_clause = Or([match[(m, w)] != is_true(model[match[(m, w)]]) for m in men for w in women])
    solver.add(blocking_clause)

# Print results
print("STATUS: sat")
print(f"Total stable matchings found: {len(solutions)}")
print("Stable matchings:")
for i, matching in enumerate(solutions):
    print(f"  Matching {i+1}: {matching}")

# Also print in the required format
print(f"count: {len(solutions)}")
print("stable_matchings:", solutions)