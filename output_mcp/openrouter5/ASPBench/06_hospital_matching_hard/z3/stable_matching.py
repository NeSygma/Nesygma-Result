from z3 import *

# ============================================================
# Stable Matching Problem: 40 Residents, 20 Hospitals
# ============================================================

# Residents: r1..r40 (indices 0..39)
R = 40
# Hospitals: h1..h20 (indices 0..19)
H = 20

# Hospital capacities
cap = [2, 2, 2, 2, 2, 2,   # h1-h6
       4, 3, 1,             # h7-h9
       3, 3, 2,             # h10-h12
       3, 3, 2,             # h13-h15
       2, 2,                # h16-h17
       1, 1, 1]             # h18-h20 (no acceptable residents)

# ============================================================
# Preference lists (0-indexed)
# ============================================================

# Resident preferences: list of lists of hospital indices
# Only acceptable hospitals listed
res_prefs = [
    # Block A1 (r1-r4): indices 0-3
    [0, 1],          # r1: h1 > h2
    [0, 1],          # r2: h1 > h2
    [1, 0],          # r3: h2 > h1
    [1, 0],          # r4: h2 > h1
    # Block A2 (r5-r8): indices 4-7
    [2, 3],          # r5: h3 > h4
    [2, 3],          # r6: h3 > h4
    [3, 2],          # r7: h4 > h3
    [3, 2],          # r8: h4 > h3
    # Block A3 (r9-r12): indices 8-11
    [4, 5],          # r9: h5 > h6
    [4, 5],          # r10: h5 > h6
    [5, 4],          # r11: h6 > h5
    [5, 4],          # r12: h6 > h5
    # Block B1 (r13-r20): indices 12-19
    [6, 7, 8],       # r13: h7 > h8 > h9
    [6, 7, 8],       # r14: h7 > h8 > h9
    [7, 6, 8],       # r15: h8 > h7 > h9
    [7, 6, 8],       # r16: h8 > h7 > h9
    [6, 7, 8],       # r17: h7 > h8 > h9
    [6, 8, 7],       # r18: h7 > h9 > h8
    [7, 8, 6],       # r19: h8 > h9 > h7
    [8, 7, 6],       # r20: h9 > h8 > h7
    # Block B2 (r21-r28): indices 20-27
    [9, 10, 11],     # r21: h10 > h11 > h12
    [9, 11, 10],     # r22: h10 > h12 > h11
    [10, 9, 11],     # r23: h11 > h10 > h12
    [10, 11, 9],     # r24: h11 > h12 > h10
    [9, 10, 11],     # r25: h10 > h11 > h12
    [10, 9, 11],     # r26: h11 > h10 > h12
    [11, 10, 9],     # r27: h12 > h11 > h10
    [11, 9, 10],     # r28: h12 > h10 > h11
    # Block B3 (r29-r36): indices 28-35
    [12, 13, 14],    # r29: h13 > h14 > h15
    [12, 14, 13],    # r30: h13 > h15 > h14
    [13, 12, 14],    # r31: h14 > h13 > h15
    [13, 14, 12],    # r32: h14 > h15 > h13
    [12, 13, 14],    # r33: h13 > h14 > h15
    [13, 12, 14],    # r34: h14 > h13 > h15
    [14, 13, 12],    # r35: h15 > h14 > h13
    [14, 12, 13],    # r36: h15 > h13 > h14
    # Block A4 (r37-r40): indices 36-39
    [15, 16],        # r37: h16 > h17
    [15, 16],        # r38: h16 > h17
    [16, 15],        # r39: h17 > h16
    [16, 15],        # r40: h17 > h16
]

# Hospital preferences: list of lists of resident indices
# Only acceptable residents listed
hosp_prefs = [
    # Block A1
    [2, 3, 0, 1],       # h1: r3 > r4 > r1 > r2
    [0, 1, 2, 3],       # h2: r1 > r2 > r3 > r4
    # Block A2
    [6, 7, 4, 5],       # h3: r7 > r8 > r5 > r6
    [4, 5, 6, 7],       # h4: r5 > r6 > r7 > r8
    # Block A3
    [10, 11, 8, 9],     # h5: r11 > r12 > r9 > r10
    [8, 9, 10, 11],     # h6: r9 > r10 > r11 > r12
    # Block B1
    [12, 13, 16, 17, 14, 15, 18, 19],  # h7
    [14, 15, 18, 12, 13, 16, 17, 19],  # h8
    [19, 18, 17, 16, 15, 14, 13, 12],  # h9
    # Block B2
    [20, 21, 24, 22, 23, 25, 26, 27],  # h10
    [22, 23, 25, 20, 21, 24, 26, 27],  # h11
    [26, 27, 22, 23, 20, 21, 24, 25],  # h12
    # Block B3
    [28, 29, 32, 30, 31, 33, 34, 35],  # h13
    [30, 31, 33, 28, 29, 32, 34, 35],  # h14
    [34, 35, 30, 31, 28, 29, 32, 33],  # h15
    # Block A4
    [38, 39, 36, 37],   # h16: r39 > r40 > r37 > r38
    [36, 37, 38, 39],   # h17: r37 > r38 > r39 > r40
    # h18, h19, h20: no acceptable residents
    [], [], []
]

# ============================================================
# Helper: rank of hospital h in resident r's preference list
# (lower = more preferred). Returns -1 if not acceptable.
# ============================================================
def res_rank(r, h):
    prefs = res_prefs[r]
    for i, hp in enumerate(prefs):
        if hp == h:
            return i
    return -1

# Helper: rank of resident r in hospital h's preference list
def hosp_rank(h, r):
    prefs = hosp_prefs[h]
    for i, rp in enumerate(prefs):
        if rp == r:
            return i
    return -1

# ============================================================
# Build the solver
# ============================================================
solver = Solver()

# Decision variables:
# match[r] = hospital assigned to resident r, or -1 if unmatched
match = [Int(f'match_{r}') for r in range(R)]

# For each hospital h, we have cap[h] slots.
# We'll use an array of variables: slot[h][k] = resident assigned to slot k of hospital h, or -1 if empty
slot = [[Int(f'slot_{h}_{k}') for k in range(cap[h])] for h in range(H)]

# Domain constraints
for r in range(R):
    solver.add(Or([match[r] == h for h in res_prefs[r]] + [match[r] == -1]))

for h in range(H):
    for k in range(cap[h]):
        solver.add(Or([slot[h][k] == r for r in hosp_prefs[h]] + [slot[h][k] == -1]))

# Consistency: match[r] == h iff r is assigned to some slot of h
for r in range(R):
    for h in range(H):
        if res_rank(r, h) >= 0 and hosp_rank(h, r) >= 0:
            # If r is matched to h, then r must occupy exactly one slot of h
            r_in_h_slots = [slot[h][k] == r for k in range(cap[h])]
            solver.add(Implies(match[r] == h, Or(r_in_h_slots)))
            # If r is in any slot of h, then match[r] == h
            for k in range(cap[h]):
                solver.add(Implies(slot[h][k] == r, match[r] == h))
        elif res_rank(r, h) >= 0 or hosp_rank(h, r) >= 0:
            # Only one side finds the other acceptable - can't match
            solver.add(match[r] != h)
            for k in range(cap[h]):
                solver.add(slot[h][k] != r)

# Each slot of a hospital gets a distinct resident (or -1)
for h in range(H):
    for k1 in range(cap[h]):
        for k2 in range(k1+1, cap[h]):
            solver.add(Or(slot[h][k1] == -1, slot[h][k2] == -1, slot[h][k1] != slot[h][k2]))

# Each resident matched to at most one hospital (already enforced by match[r] being a single value)

# ============================================================
# Stability constraints
# ============================================================
# For each pair (r, h) that are mutually acceptable:
# If r prefers h over their current match (or r is unmatched), 
# then h must NOT prefer r over at least one of its current assignees.
# In other words: if r prefers h, then h must be "full" with all current
# assignees being preferred over r.

for r in range(R):
    for h in range(H):
        rr = res_rank(r, h)
        hr = hosp_rank(h, r)
        if rr < 0 or hr < 0:
            continue  # not mutually acceptable
        
        # r prefers h over current match if:
        # - r is unmatched (match[r] == -1), OR
        # - match[r] is some h_cur where res_rank(r, h_cur) > rr (h is better)
        
        # h would accept r if:
        # - h has a free slot (some slot == -1), OR
        # - h prefers r over at least one current assignee
        
        # Blocking condition: r prefers h AND h would accept r
        # We forbid this: NOT (r prefers h AND h would accept r)
        
        # r prefers h:
        r_prefers_h_conditions = [match[r] == -1]
        for h_cur in res_prefs[r]:
            if res_rank(r, h_cur) > rr:
                r_prefers_h_conditions.append(match[r] == h_cur)
        r_prefers_h = Or(r_prefers_h_conditions)
        
        # h would accept r:
        h_accepts_r_conditions = []
        # h has free slot
        h_accepts_r_conditions.append(Or([slot[h][k] == -1 for k in range(cap[h])]))
        # h prefers r over at least one current assignee
        for k in range(cap[h]):
            for r_cur in hosp_prefs[h]:
                if hosp_rank(h, r_cur) > hr:  # r_cur is worse than r
                    h_accepts_r_conditions.append(slot[h][k] == r_cur)
        h_accepts_r = Or(h_accepts_r_conditions)
        
        # No blocking pair
        solver.add(Not(And(r_prefers_h, h_accepts_r)))

# ============================================================
# Solve and enumerate all stable matchings
# ============================================================
BENCHMARK_MODE = True

all_matchings = []
decision_vars = match[:]  # match variables define the matching

while True:
    result = solver.check()
    if result == sat:
        m = solver.model()
        # Extract this matching
        matching = []
        for r in range(R):
            mv = m.eval(match[r], model_completion=True)
            if mv is not None:
                try:
                    h_val = mv.as_long()
                except:
                    h_val = -1
            else:
                h_val = -1
            if h_val >= 0:
                matching.append([r, h_val])
        all_matchings.append(matching)
        
        # Block this solution
        solver.add(Or([match[r] != m.eval(match[r], model_completion=True).as_long() for r in range(R)]))
    else:
        break

print(f"STATUS: sat")
print(f"Total stable matchings found: {len(all_matchings)}")
for i, matching in enumerate(all_matchings):
    print(f"Matching {i+1}:")
    for pair in matching:
        r, h = pair
        print(f"  r{r+1} -> h{h+1}")
    print()