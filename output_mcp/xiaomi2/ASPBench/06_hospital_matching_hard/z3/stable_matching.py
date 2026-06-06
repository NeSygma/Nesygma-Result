from z3 import *
from itertools import product as iter_product

def find_block_matchings(block_name, res_list, hosp_list, cap, res_prefs_block, hosp_prefs_block):
    """Find all stable matchings for an independent block."""
    solver = Solver()
    
    # Decision variables: match[r] = hospital assigned to resident r (0 = unmatched)
    match = {}
    for r in res_list:
        match[r] = Int(f'match_{block_name}_{r}')
        acceptable = res_prefs_block.get(r, [])
        if acceptable:
            solver.add(Or([match[r] == 0] + [match[r] == h for h in acceptable]))
        else:
            solver.add(match[r] == 0)
    
    # Capacity constraints
    for h in hosp_list:
        acceptable_res = hosp_prefs_block.get(h, [])
        if acceptable_res:
            solver.add(Sum([If(match[r] == h, 1, 0) for r in acceptable_res]) <= cap[h])
    
    # Compute preference ranks (lower = more preferred)
    res_rank = {}
    for r in res_list:
        for i, h in enumerate(res_prefs_block.get(r, [])):
            res_rank[(r, h)] = i
    
    hosp_rank = {}
    for h in hosp_list:
        for i, r in enumerate(hosp_prefs_block.get(h, [])):
            hosp_rank[(h, r)] = i
    
    # Build mutually acceptable pairs
    acceptable_pairs = set()
    for r in res_list:
        for h in res_prefs_block.get(r, []):
            if h in hosp_prefs_block and r in hosp_prefs_block[h]:
                acceptable_pairs.add((r, h))
    
    # Stability constraints: no blocking pairs
    for (r, h) in acceptable_pairs:
        # Condition 1: r prefers h over current match OR r is unmatched
        r_prefers_parts = []
        for hp in res_prefs_block.get(r, []):
            if res_rank[(r, h)] < res_rank.get((r, hp), 999):
                r_prefers_parts.append(match[r] == hp)
        r_prefers_h = Or([match[r] == 0] + r_prefers_parts)
        
        # Condition 2: h would accept r (free capacity OR prefers r over some assignee)
        h_acceptable_res = hosp_prefs_block.get(h, [])
        h_has_capacity = Sum([If(match[rp] == h, 1, 0) for rp in h_acceptable_res]) < cap[h]
        
        h_prefers_parts = []
        for rp in hosp_prefs_block.get(h, []):
            if hosp_rank[(h, r)] < hosp_rank.get((h, rp), 999):
                h_prefers_parts.append(match[rp] == h)
        
        if h_prefers_parts:
            h_would_accept = Or(h_has_capacity, Or(h_prefers_parts))
        else:
            h_would_accept = h_has_capacity
        
        # Not a blocking pair: ~(r_prefers_h AND h_would_accept)
        solver.add(Or(Not(r_prefers_h), Not(h_would_accept)))
    
    # Enumerate all solutions
    solutions = []
    while solver.check() == sat:
        m = solver.model()
        sol = {}
        for r in res_list:
            val = m.evaluate(match[r], model_completion=True)
            sol[r] = int(str(val))
        solutions.append(sol)
        # Block this solution
        solver.add(Or([match[r] != sol[r] for r in res_list]))
    
    return solutions

# Hospital capacities
capacity = {
    1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2,
    7: 4, 8: 3, 9: 1,
    10: 3, 11: 3, 12: 2,
    13: 3, 14: 3, 15: 2,
    16: 2, 17: 2,
    18: 1, 19: 1, 20: 1
}

# Independent blocks
blocks = {
    'A1': {
        'res': [1, 2, 3, 4],
        'hosp': [1, 2],
        'res_prefs': {1: [1, 2], 2: [1, 2], 3: [2, 1], 4: [2, 1]},
        'hosp_prefs': {1: [3, 4, 1, 2], 2: [1, 2, 3, 4]}
    },
    'A2': {
        'res': [5, 6, 7, 8],
        'hosp': [3, 4],
        'res_prefs': {5: [3, 4], 6: [3, 4], 7: [4, 3], 8: [4, 3]},
        'hosp_prefs': {3: [7, 8, 5, 6], 4: [5, 6, 7, 8]}
    },
    'A3': {
        'res': [9, 10, 11, 12],
        'hosp': [5, 6],
        'res_prefs': {9: [5, 6], 10: [5, 6], 11: [6, 5], 12: [6, 5]},
        'hosp_prefs': {5: [11, 12, 9, 10], 6: [9, 10, 11, 12]}
    },
    'A4': {
        'res': [37, 38, 39, 40],
        'hosp': [16, 17],
        'res_prefs': {37: [16, 17], 38: [16, 17], 39: [17, 16], 40: [17, 16]},
        'hosp_prefs': {16: [39, 40, 37, 38], 17: [37, 38, 39, 40]}
    },
    'B1': {
        'res': [13, 14, 15, 16, 17, 18, 19, 20],
        'hosp': [7, 8, 9],
        'res_prefs': {
            13: [7, 8, 9], 14: [7, 8, 9], 15: [8, 7, 9], 16: [8, 7, 9],
            17: [7, 8, 9], 18: [7, 9, 8], 19: [8, 9, 7], 20: [9, 8, 7]
        },
        'hosp_prefs': {
            7: [13, 14, 17, 18, 15, 16, 19, 20],
            8: [15, 16, 19, 13, 14, 17, 18, 20],
            9: [20, 19, 18, 17, 16, 15, 14, 13]
        }
    },
    'B2': {
        'res': [21, 22, 23, 24, 25, 26, 27, 28],
        'hosp': [10, 11, 12],
        'res_prefs': {
            21: [10, 11, 12], 22: [10, 12, 11], 23: [11, 10, 12], 24: [11, 12, 10],
            25: [10, 11, 12], 26: [11, 10, 12], 27: [12, 11, 10], 28: [12, 10, 11]
        },
        'hosp_prefs': {
            10: [21, 22, 25, 23, 24, 26, 27, 28],
            11: [23, 24, 26, 21, 22, 25, 27, 28],
            12: [27, 28, 23, 24, 21, 22, 25, 26]
        }
    },
    'B3': {
        'res': [29, 30, 31, 32, 33, 34, 35, 36],
        'hosp': [13, 14, 15],
        'res_prefs': {
            29: [13, 14, 15], 30: [13, 15, 14], 31: [14, 13, 15], 32: [14, 15, 13],
            33: [13, 14, 15], 34: [14, 13, 15], 35: [15, 14, 13], 36: [15, 13, 14]
        },
        'hosp_prefs': {
            13: [29, 30, 33, 31, 32, 34, 35, 36],
            14: [31, 32, 34, 29, 30, 33, 35, 36],
            15: [35, 36, 31, 32, 29, 30, 33, 34]
        }
    }
}

# Solve each block independently
all_block_matchings = {}
for block_name, block_data in blocks.items():
    matchings = find_block_matchings(
        block_name,
        block_data['res'],
        block_data['hosp'],
        capacity,
        block_data['res_prefs'],
        block_data['hosp_prefs']
    )
    all_block_matchings[block_name] = matchings
    print(f"Block {block_name}: {len(matchings)} stable matchings")
    for i, m in enumerate(matchings):
        matched = {r: h for r, h in m.items() if h != 0}
        print(f"  Matching {i+1}: {matched}")

# Combine all blocks
block_names = list(blocks.keys())
block_matching_lists = [all_block_matchings[b] for b in block_names]

total = 1
for m in block_matching_lists:
    total *= len(m)

print(f"\nTotal stable matchings: {total}")
print(f"STATUS: sat")

# Print all combined matchings
print(f"\n--- All {total} Stable Matchings ---")
for idx, combo in enumerate(iter_product(*block_matching_lists)):
    matching = {}
    for block_match in combo:
        matching.update(block_match)
    pairs = sorted([[r, matching[r]] for r in matching if matching[r] != 0])
    print(f"Matching {idx+1}: {pairs}")

print(f"\ncount: {total}")