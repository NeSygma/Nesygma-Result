from z3 import *

# ============================================================
# Puzzle Data Encoding
# ============================================================
# Room mapping: R1=1, R2=2, R3=3, R4=4, R5=5
# Theme mapping: search=0, logic=1, physical=2

puzzles = {
    1:  {"room": 1, "diff": 1, "theme": 0, "prereqs": [],    "req_items": [],     "yield_items": []},
    2:  {"room": 1, "diff": 1, "theme": 1, "prereqs": [1],   "req_items": [],     "yield_items": ["key_red"]},
    3:  {"room": 2, "diff": 2, "theme": 2, "prereqs": [2],   "req_items": [],     "yield_items": []},
    4:  {"room": 2, "diff": 2, "theme": 0, "prereqs": [3],   "req_items": ["key_red"],  "yield_items": []},
    5:  {"room": 2, "diff": 2, "theme": 1, "prereqs": [4],   "req_items": [],     "yield_items": ["uv_light"]},
    6:  {"room": 1, "diff": 3, "theme": 0, "prereqs": [5],   "req_items": ["uv_light"], "yield_items": []},
    7:  {"room": 1, "diff": 3, "theme": 1, "prereqs": [6],   "req_items": [],     "yield_items": ["key_blue"]},
    8:  {"room": 2, "diff": 3, "theme": 2, "prereqs": [7],   "req_items": [],     "yield_items": ["crowbar"]},
    9:  {"room": 3, "diff": 3, "theme": 0, "prereqs": [8],   "req_items": ["key_blue"], "yield_items": []},
    10: {"room": 4, "diff": 3, "theme": 2, "prereqs": [9],   "req_items": ["crowbar"],  "yield_items": []},
    11: {"room": 4, "diff": 4, "theme": 1, "prereqs": [10],  "req_items": [],     "yield_items": []},
    12: {"room": 3, "diff": 4, "theme": 0, "prereqs": [11],  "req_items": ["uv_light"], "yield_items": []},
    13: {"room": 3, "diff": 4, "theme": 1, "prereqs": [12],  "req_items": [],     "yield_items": ["gear_1"]},
    14: {"room": 4, "diff": 4, "theme": 0, "prereqs": [13],  "req_items": [],     "yield_items": []},
    15: {"room": 5, "diff": 4, "theme": 2, "prereqs": [14],  "req_items": ["crowbar"],  "yield_items": ["gear_2"]},
    16: {"room": 5, "diff": 5, "theme": 1, "prereqs": [15],  "req_items": [],     "yield_items": []},
    17: {"room": 5, "diff": 5, "theme": 0, "prereqs": [16],  "req_items": ["uv_light"], "yield_items": ["gear_3"]},
    18: {"room": 5, "diff": 5, "theme": 1, "prereqs": [17],  "req_items": ["key_red", "key_blue"], "yield_items": []},
}

# Item -> puzzle that yields it
item_yield_puzzle = {
    "key_red": 2,
    "key_blue": 7,
    "uv_light": 5,
    "crowbar": 8,
    "gear_1": 13,
    "gear_2": 15,
    "gear_3": 17,
}

room_names = {1: "R1", 2: "R2", 3: "R3", 4: "R4", 5: "R5"}
theme_names = {0: "search", 1: "logic", 2: "physical"}

N = 18

# ============================================================
# Z3 Model
# ============================================================
solver = Solver()

# pos[p] = the position (0..17) of puzzle p in the solved sequence
pos = {p: Int(f'pos_{p}') for p in range(1, N + 1)}

# --- Constraint 0: Domain and distinctness ---
for p in range(1, N + 1):
    solver.add(pos[p] >= 0, pos[p] < N)
solver.add(Distinct([pos[p] for p in range(1, N + 1)]))

# --- Constraint 1: Prerequisite ordering ---
for p in range(1, N + 1):
    for prereq in puzzles[p]["prereqs"]:
        solver.add(pos[prereq] < pos[p])

# --- Constraint 2: Item requirement ordering ---
# An item must be yielded (by its source puzzle) before it can be used
for p in range(1, N + 1):
    for item in puzzles[p]["req_items"]:
        src = item_yield_puzzle[item]
        solver.add(pos[src] < pos[p])

# --- Constraints 3-5: Consecutive-puzzle constraints ---
# For every ordered pair (p, q): if q is immediately after p, then:
#   (3) rooms are same or adjacent  |room_p - room_q| <= 1
#   (4) themes differ
#   (5) difficulty difference <= 1
for p in range(1, N + 1):
    for q in range(1, N + 1):
        if p == q:
            continue
        consec = (pos[q] == pos[p] + 1)

        # Room adjacency
        rp = puzzles[p]["room"]
        rq = puzzles[q]["room"]
        solver.add(Implies(consec, And(rp - rq <= 1, rq - rp <= 1)))

        # Theme balance (no same theme consecutively)
        tp = puzzles[p]["theme"]
        tq = puzzles[q]["theme"]
        solver.add(Implies(consec, tp != tq))

        # Difficulty curve (difference at most 1)
        dp = puzzles[p]["diff"]
        dq = puzzles[q]["diff"]
        solver.add(Implies(consec, And(dp - dq <= 1, dq - dp <= 1)))

# ============================================================
# Solve
# ============================================================
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()

    # Reconstruct the ordered sequence from position variables
    seq = [0] * N
    for p in range(1, N + 1):
        idx = m[pos[p]].as_long()
        seq[idx] = p

    print("STATUS: sat")

    # --- puzzle_order ---
    print(f"puzzle_order: {seq}")

    # --- room_progression ---
    room_prog = [room_names[puzzles[p]["room"]] for p in seq]
    print(f"room_progression: {room_prog}")

    # --- difficulty_progression ---
    diff_prog = [puzzles[p]["diff"] for p in seq]
    print(f"difficulty_progression: {diff_prog}")

    # --- theme_progression ---
    theme_prog = [theme_names[puzzles[p]["theme"]] for p in seq]
    print(f"theme_progression: {theme_prog}")

    # --- Verify all constraints programmatically ---
    all_ok = True

    # Check prerequisites
    for p in range(1, N + 1):
        for prereq in puzzles[p]["prereqs"]:
            if seq.index(prereq) >= seq.index(p):
                all_ok = False
                print(f"  VIOLATION: prereq {prereq} not before {p}")

    # Check item requirements
    for p in range(1, N + 1):
        for item in puzzles[p]["req_items"]:
            src = item_yield_puzzle[item]
            if seq.index(src) >= seq.index(p):
                all_ok = False
                print(f"  VIOLATION: item {item} (from {src}) not available for {p}")

    # Check consecutive constraints
    for i in range(N - 1):
        p, q = seq[i], seq[i + 1]
        rp, rq = puzzles[p]["room"], puzzles[q]["room"]
        if abs(rp - rq) > 1:
            all_ok = False
            print(f"  VIOLATION: room adjacency between {p} and {q}")
        if puzzles[p]["theme"] == puzzles[q]["theme"]:
            all_ok = False
            print(f"  VIOLATION: same theme between {p} and {q}")
        if abs(puzzles[p]["diff"] - puzzles[q]["diff"]) > 1:
            all_ok = False
            print(f"  VIOLATION: difficulty jump between {p} and {q}")

    print(f"all_constraints_satisfied: {all_ok}")

    # --- puzzle_details ---
    print("\npuzzle_details:")
    for p in range(1, N + 1):
        pd = puzzles[p]
        print(f"  Puzzle {p}: Room={room_names[pd['room']]}, "
              f"Difficulty={pd['diff']}, Theme={theme_names[pd['theme']]}, "
              f"Prereqs={pd['prereqs']}, "
              f"Requires={pd['req_items']}, "
              f"Yields={pd['yield_items']}, "
              f"Position={m[pos[p]]}")

elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")