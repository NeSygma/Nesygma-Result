from z3 import *
import itertools
from copy import deepcopy

# ============================================================
# DATA DEFINITIONS
# ============================================================

# All hospitals and capacities
hospital_capacities = {
    'h1': 2, 'h2': 2, 'h3': 2, 'h4': 2, 'h5': 2, 'h6': 2,
    'h7': 4, 'h8': 3, 'h9': 1,
    'h10': 3, 'h11': 3, 'h12': 2,
    'h13': 3, 'h14': 3, 'h15': 2,
    'h16': 2, 'h17': 2,
    'h18': 1, 'h19': 1, 'h20': 1
}

# Resident preferences (only acceptable hospitals listed)
res_prefs = {
    # Block A1
    'r1': ['h1', 'h2'],
    'r2': ['h1', 'h2'],
    'r3': ['h2', 'h1'],
    'r4': ['h2', 'h1'],
    # Block A2
    'r5': ['h3', 'h4'],
    'r6': ['h3', 'h4'],
    'r7': ['h4', 'h3'],
    'r8': ['h4', 'h3'],
    # Block A3
    'r9': ['h5', 'h6'],
    'r10': ['h5', 'h6'],
    'r11': ['h6', 'h5'],
    'r12': ['h6', 'h5'],
    # Block B1
    'r13': ['h7', 'h8', 'h9'],
    'r14': ['h7', 'h8', 'h9'],
    'r15': ['h8', 'h7', 'h9'],
    'r16': ['h8', 'h7', 'h9'],
    'r17': ['h7', 'h8', 'h9'],
    'r18': ['h7', 'h9', 'h8'],
    'r19': ['h8', 'h9', 'h7'],
    'r20': ['h9', 'h8', 'h7'],
    # Block B2
    'r21': ['h10', 'h11', 'h12'],
    'r22': ['h10', 'h12', 'h11'],
    'r23': ['h11', 'h10', 'h12'],
    'r24': ['h11', 'h12', 'h10'],
    'r25': ['h10', 'h11', 'h12'],
    'r26': ['h11', 'h10', 'h12'],
    'r27': ['h12', 'h11', 'h10'],
    'r28': ['h12', 'h10', 'h11'],
    # Block B3
    'r29': ['h13', 'h14', 'h15'],
    'r30': ['h13', 'h15', 'h14'],
    'r31': ['h14', 'h13', 'h15'],
    'r32': ['h14', 'h15', 'h13'],
    'r33': ['h13', 'h14', 'h15'],
    'r34': ['h14', 'h13', 'h15'],
    'r35': ['h15', 'h14', 'h13'],
    'r36': ['h15', 'h13', 'h14'],
    # Block A4
    'r37': ['h16', 'h17'],
    'r38': ['h16', 'h17'],
    'r39': ['h17', 'h16'],
    'r40': ['h17', 'h16'],
}

# Hospital preferences (only acceptable residents listed)
hos_prefs = {
    # Block A1
    'h1': ['r3', 'r4', 'r1', 'r2'],
    'h2': ['r1', 'r2', 'r3', 'r4'],
    # Block A2
    'h3': ['r7', 'r8', 'r5', 'r6'],
    'h4': ['r5', 'r6', 'r7', 'r8'],
    # Block A3
    'h5': ['r11', 'r12', 'r9', 'r10'],
    'h6': ['r9', 'r10', 'r11', 'r12'],
    # Block B1
    'h7': ['r13', 'r14', 'r17', 'r18', 'r15', 'r16', 'r19', 'r20'],
    'h8': ['r15', 'r16', 'r19', 'r13', 'r14', 'r17', 'r18', 'r20'],
    'h9': ['r20', 'r19', 'r18', 'r17', 'r16', 'r15', 'r14', 'r13'],
    # Block B2
    'h10': ['r21', 'r22', 'r25', 'r23', 'r24', 'r26', 'r27', 'r28'],
    'h11': ['r23', 'r24', 'r26', 'r21', 'r22', 'r25', 'r27', 'r28'],
    'h12': ['r27', 'r28', 'r23', 'r24', 'r21', 'r22', 'r25', 'r26'],
    # Block B3
    'h13': ['r29', 'r30', 'r33', 'r31', 'r32', 'r34', 'r35', 'r36'],
    'h14': ['r31', 'r32', 'r34', 'r29', 'r30', 'r33', 'r35', 'r36'],
    'h15': ['r35', 'r36', 'r31', 'r32', 'r29', 'r30', 'r33', 'r34'],
    # Block A4
    'h16': ['r39', 'r40', 'r37', 'r38'],
    'h17': ['r37', 'r38', 'r39', 'r40'],
}

# ============================================================
# BLOCK DEFINITIONS
# ============================================================
blocks = [
    ('A1', ['r1', 'r2', 'r3', 'r4'], ['h1', 'h2']),
    ('A2', ['r5', 'r6', 'r7', 'r8'], ['h3', 'h4']),
    ('A3', ['r9', 'r10', 'r11', 'r12'], ['h5', 'h6']),
    ('B1', ['r13', 'r14', 'r15', 'r16', 'r17', 'r18', 'r19', 'r20'], ['h7', 'h8', 'h9']),
    ('B2', ['r21', 'r22', 'r23', 'r24', 'r25', 'r26', 'r27', 'r28'], ['h10', 'h11', 'h12']),
    ('B3', ['r29', 'r30', 'r31', 'r32', 'r33', 'r34', 'r35', 'r36'], ['h13', 'h14', 'h15']),
    ('A4', ['r37', 'r38', 'r39', 'r40'], ['h16', 'h17']),
]

# ============================================================
# Z3 SOLVER FUNCTION FOR A SINGLE BLOCK
# ============================================================
def solve_block(res_list, hos_list, block_name):
    """Find all stable matchings for a single block."""
    
    # Build acceptable pairs (all pairs within the block are mutually acceptable)
    acceptable_pairs = []
    for r in res_list:
        for h in hos_list:
            if r in res_prefs and h in res_prefs[r]:
                if h in hos_prefs and r in hos_prefs[h]:
                    acceptable_pairs.append((r, h))
    
    # Z3 Bool variables for each pair
    X = {}
    for r, h in acceptable_pairs:
        X[(r, h)] = Bool(f'X_{block_name}_{r}_{h}')
    
    solver = Solver()
    
    # Constraint 1: Each resident matched to at most one hospital
    for r in res_list:
        if r in res_prefs:
            vars_for_r = [X[(r, h)] for h in res_prefs[r] if (r, h) in X]
            if vars_for_r:
                solver.add(Sum([If(v, 1, 0) for v in vars_for_r]) <= 1)
    
    # Constraint 2: Each hospital at most capacity
    for h in hos_list:
        if h in hospital_capacities:
            vars_for_h = [X[(r, h)] for r in res_list if (r, h) in X]
            if vars_for_h:
                solver.add(Sum([If(v, 1, 0) for v in vars_for_h]) <= hospital_capacities[h])
    
    # Constraint 3: Stability - No blocking pair
    for r, h in acceptable_pairs:
        pref_r = res_prefs[r]
        h_idx = pref_r.index(h)
        
        # r_prefers_h_over_current = r is unmatched OR r is matched to a worse hospital
        # r is matched to a hospital worse than h
        worse_hos = pref_r[h_idx+1:]  # hospitals worse than h
        
        # r is unmatched
        r_vars = [X[(r, h2)] for h2 in pref_r if (r, h2) in X]
        r_unmatched = And([Not(v) for v in r_vars])
        
        # r is matched to a worse hospital
        if worse_hos:
            r_matched_worse = Or([X[(r, h2)] for h2 in worse_hos if (r, h2) in X])
        else:
            r_matched_worse = False
        
        if r_matched_worse == False:
            r_prefers_h = r_unmatched
        else:
            r_prefers_h = Or(r_unmatched, r_matched_worse)
        
        # h_would_accept_r = h has free capacity OR h prefers r over some current resident
        h_cap = hospital_capacities[h]
        h_vars = [X[(r2, h)] for r2 in res_list if (r2, h) in X]
        
        # h has free capacity
        h_free = Sum([If(v, 1, 0) for v in h_vars]) < h_cap
        
        # h prefers r over some current resident
        pref_h = hos_prefs[h]
        r_idx_in_h = pref_h.index(r)
        worse_res = pref_h[r_idx_in_h+1:]  # residents worse than r
        if worse_res:
            h_prefers_r = Or([X[(r2, h)] for r2 in worse_res if (r2, h) in X])
        else:
            h_prefers_r = False
        
        if h_prefers_r == False:
            h_would_accept = h_free
        else:
            h_would_accept = Or(h_free, h_prefers_r)
        
        # No blocking pair (r, h): NOT( X[r][h]=False AND r_prefers_h AND h_would_accept )
        solver.add(Not(And(Not(X[(r, h)]), r_prefers_h, h_would_accept)))
    
    # Enumerate all solutions
    solutions = []
    while solver.check() == sat:
        m = solver.model()
        matching = {}
        for r in res_list:
            matched_h = None
            for h in res_prefs.get(r, []):
                if (r, h) in X and is_true(m[X[(r, h)]]):
                    matched_h = h
                    break
            matching[r] = matched_h  # None if unmatched
        solutions.append(matching)
        
        # Block this solution
        blocking_clause = []
        for (r, h), var in X.items():
            if is_true(m[var]):
                blocking_clause.append(Not(var))
            else:
                blocking_clause.append(var)
        solver.add(Or(blocking_clause))
    
    return solutions

# ============================================================
# SOLVE EACH BLOCK
# ============================================================
all_block_solutions = {}
total_combinations = 1

for block_name, res_list, hos_list in blocks:
    print(f"Solving block {block_name}...")
    solutions = solve_block(res_list, hos_list, block_name)
    all_block_solutions[block_name] = solutions
    count = len(solutions)
    total_combinations *= count
    print(f"  Found {count} stable matchings")
    for i, sol in enumerate(solutions):
        pairs = [(r, h) for r, h in sol.items() if h is not None]
        print(f"    Matching {i+1}: {pairs}")

print(f"\nTotal combinations across all blocks: {total_combinations}")

# ============================================================
# COMBINE ALL BLOCK SOLUTIONS TO GET GLOBAL MATCHINGS
# ============================================================
print(f"\nGenerating all {total_combinations} global stable matchings...")

all_solutions = []
block_names = [b[0] for b in blocks]
solution_lists = [all_block_solutions[name] for name in block_names]

for combo in itertools.product(*solution_lists):
    global_matching = []
    for block_sol in combo:
        for r, h in block_sol.items():
            if h is not None:
                global_matching.append([r, h])
    # Sort for consistency
    global_matching.sort(key=lambda x: int(x[0][1:]))
    all_solutions.append(global_matching)

print(f"\nTotal stable matchings: {len(all_solutions)}")

# Print first 10 and last 10 for inspection
print("\nFirst 10 stable matchings:")
for i, m in enumerate(all_solutions[:10]):
    print(f"  {i+1}: {m}")

if len(all_solutions) > 20:
    print("  ...")
    print(f"\nLast 10 stable matchings:")
    for i, m in enumerate(all_solutions[-10:]):
        print(f"  {len(all_solutions)-9+i}: {m}")

print("\nSTATUS: sat")