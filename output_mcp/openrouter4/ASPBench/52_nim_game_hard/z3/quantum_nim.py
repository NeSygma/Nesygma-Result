from z3 import *

# ============================================================
# QUANTUM NIM - Optimal Move Finder
# ============================================================
# Initial game state
initial_piles = [6, 7, 10, 13]
num_piles = len(initial_piles)

# Compute initial nim-sum
initial_nim_sum = 0
for p in initial_piles:
    initial_nim_sum ^= p
is_winning = initial_nim_sum != 0

print(f"Initial piles: {initial_piles}")
print(f"Initial nim-sum: {initial_nim_sum}")
print(f"Is winning position: {is_winning}")
print()

# Collect ALL optimal moves
optimal_moves = []

# ============================================================
# STANDARD MOVES: Remove N stones (1 <= N <= pile_size) from any pile
# After move: if pile becomes size 0, it disappears
# ============================================================
for pile_idx in range(num_piles):
    pile_size = initial_piles[pile_idx]
    for remove_cnt in range(1, pile_size + 1):
        new_pile_size = pile_size - remove_cnt

        # Build resulting pile list
        if new_pile_size == 0:
            # Pile removed entirely
            result_piles = [initial_piles[j] for j in range(num_piles) if j != pile_idx]
        else:
            result_piles = [initial_piles[j] if j != pile_idx else new_pile_size
                           for j in range(num_piles)]

        result_piles_sorted = sorted(result_piles)

        # CONSTRAINT: No two piles may have the same size
        if len(set(result_piles_sorted)) != len(result_piles_sorted):
            continue

        # Compute nim-sum of resulting state using Z3 BitVec XOR
        solver = Solver()
        num_result = len(result_piles_sorted)
        pvars = [BitVec(f'rp_{i}', 16) for i in range(num_result)]
        for i, val in enumerate(result_piles_sorted):
            solver.add(pvars[i] == val)

        # XOR all pile sizes
        xor_result = pvars[0]
        for i in range(1, num_result):
            xor_result = xor_result ^ pvars[i]
        solver.add(xor_result == 0)

        if solver.check() == sat:
            optimal_moves.append({
                "move_type": "standard",
                "pile_index": pile_idx,
                "stones_removed": remove_cnt,
                "resulting_piles": result_piles_sorted
            })

# ============================================================
# SPLIT POWER (Player 1): Split any even-sized pile into two
# non-empty piles (one-time use)
# ============================================================
for pile_idx in range(num_piles):
    pile_size = initial_piles[pile_idx]
    if pile_size % 2 != 0:
        continue  # Only even piles can be split

    for a in range(1, pile_size):
        b = pile_size - a
        if b <= 0:
            continue
        # Split must produce two non-empty piles; they CAN be equal
        # (the distinctness check later will catch duplicates with existing piles)

        # Build resulting pile list: remove original pile, add a and b
        result_piles = [initial_piles[j] for j in range(num_piles) if j != pile_idx] + [a, b]
        result_piles_sorted = sorted(result_piles)

        # CONSTRAINT: No two piles may have the same size
        if len(set(result_piles_sorted)) != len(result_piles_sorted):
            continue

        # Compute nim-sum of resulting state using Z3 BitVec XOR
        solver = Solver()
        num_result = len(result_piles_sorted)
        pvars = [BitVec(f'sp_{i}', 16) for i in range(num_result)]
        for i, val in enumerate(result_piles_sorted):
            solver.add(pvars[i] == val)

        xor_result = pvars[0]
        for i in range(1, num_result):
            xor_result = xor_result ^ pvars[i]
        solver.add(xor_result == 0)

        if solver.check() == sat:
            optimal_moves.append({
                "move_type": "power_split",
                "pile_index": pile_idx,
                "split_into": [a, b],
                "resulting_piles": result_piles_sorted
            })

# ============================================================
# OUTPUT
# ============================================================
print(f"Total optimal moves found: {len(optimal_moves)}")
print()

std_moves = [m for m in optimal_moves if m["move_type"] == "standard"]
split_moves = [m for m in optimal_moves if m["move_type"] == "power_split"]

print(f"Optimal standard moves: {len(std_moves)}")
for m in std_moves:
    print(f"  Remove {m['stones_removed']} stone(s) from pile {m['pile_index']} (size {initial_piles[m['pile_index']]})")
    print(f"    -> Resulting piles: {m['resulting_piles']}")

print()
print(f"Optimal split moves: {len(split_moves)}")
for m in split_moves:
    print(f"  Split pile {m['pile_index']} (size {initial_piles[m['pile_index']]}) into {m['split_into']}")
    print(f"    -> Resulting piles: {m['resulting_piles']}")

print()
print("STATUS: sat")