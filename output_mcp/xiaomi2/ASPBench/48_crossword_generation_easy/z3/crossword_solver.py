from z3 import *

# Word data: (word, clue)
words_data = [
    ("CODE", "Programming instructions"),
    ("DATA", "Information"),
    ("TECH", "Technology short"),
    ("CHIP", "Computer component"),
    ("BYTE", "Data unit"),
    ("NET", "Internet short"),
]

GRID_SIZE = 5
NUM_WORDS = len(words_data)

# Convert words to letter indices (A=0, B=1, ...)
words_letters = [[ord(c) - ord('A') for c in w] for w, _ in words_data]

# Generate all valid placements for each word
# Each placement: (direction, start_row, start_col, [(row, col, letter_index), ...])
placements = []
for w_idx in range(NUM_WORDS):
    wps = []
    n = len(words_letters[w_idx])
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if c + n <= GRID_SIZE:  # horizontal fits
                cells = [(r, c + k, words_letters[w_idx][k]) for k in range(n)]
                wps.append(('horizontal', r, c, cells))
            if r + n <= GRID_SIZE:  # vertical fits
                cells = [(r + k, c, words_letters[w_idx][k]) for k in range(n)]
                wps.append(('vertical', r, c, cells))
    placements.append(wps)

print(f"Placement counts per word: {[len(p) for p in placements]}")

# Boolean selection variables: sel[w][p] = True iff word w uses placement p
sel = [[Bool(f"s{w}_{p}") for p in range(len(placements[w]))] for w in range(NUM_WORDS)]

opt = Optimize()
opt.set("timeout", 60000)

# Constraint 1: Exactly one placement per word
for w in range(NUM_WORDS):
    opt.add(Sum([If(sel[w][p], 1, 0) for p in range(len(placements[w]))]) == 1)

# Constraint 2: No letter conflicts between overlapping placements of different words
conflict_count = 0
for w1 in range(NUM_WORDS):
    for p1 in range(len(placements[w1])):
        c1 = {(r, c): l for r, c, l in placements[w1][p1][3]}
        for w2 in range(w1 + 1, NUM_WORDS):
            for p2 in range(len(placements[w2])):
                c2 = {(r, c): l for r, c, l in placements[w2][p2][3]}
                # Check if any shared cell has different letters
                if any(rc in c2 and c1[rc] != c2[rc] for rc in c1):
                    opt.add(Not(And(sel[w1][p1], sel[w2][p2])))
                    conflict_count += 1

print(f"Conflict constraints added: {conflict_count}")

# Objective: Maximize intersections (pairs of words sharing a cell with matching letter)
ints = []
for w1 in range(NUM_WORDS):
    for p1 in range(len(placements[w1])):
        c1 = {(r, c): l for r, c, l in placements[w1][p1][3]}
        for w2 in range(w1 + 1, NUM_WORDS):
            for p2 in range(len(placements[w2])):
                c2 = {(r, c): l for r, c, l in placements[w2][p2][3]}
                # Check if placements share at least one cell with same letter
                if any(rc in c2 and c1[rc] == c2[rc] for rc in c1):
                    ind = Bool(f"i{w1}_{p1}_{w2}_{p2}")
                    # ind is True iff both placements are selected
                    opt.add(ind == And(sel[w1][p1], sel[w2][p2]))
                    ints.append(ind)

print(f"Intersection indicators: {len(ints)}")

if ints:
    opt.maximize(Sum([If(i, 1, 0) for i in ints]))

BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    m = opt.model()
    print("STATUS: sat")
    
    # Reconstruct grid
    grid = [['.' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    placed = []
    
    for w in range(NUM_WORDS):
        for p in range(len(placements[w])):
            if is_true(m.evaluate(sel[w][p])):
                d, r, c, cells = placements[w][p]
                for cr, cc, cl in cells:
                    grid[cr][cc] = chr(cl + ord('A'))
                placed.append((w, d, r, c, cells))
                break
    
    # Print grid
    print("\nGrid:")
    for i, row in enumerate(grid):
        print(f"  {' '.join(row)}")
    
    # Print word placements
    print("\nWord Placements:")
    for w, d, r, c, cells in placed:
        print(f"  {words_data[w][0]}: position=[{r},{c}], direction={d}, clue=\"{words_data[w][1]}\"")
    
    # Find and print intersections
    print("\nIntersections:")
    ic = 0
    for i in range(len(placed)):
        for j in range(i + 1, len(placed)):
            w1, _, _, _, cells1 = placed[i]
            w2, _, _, _, cells2 = placed[j]
            d1 = {(r, c): (l, k) for k, (r, c, l) in enumerate(cells1)}
            d2 = {(r, c): (l, k) for k, (r, c, l) in enumerate(cells2)}
            for rc in d1:
                if rc in d2 and d1[rc][0] == d2[rc][0]:
                    letter = chr(d1[rc][0] + ord('A'))
                    print(f"  {words_data[w1][0]}[{d1[rc][1]}] x {words_data[w2][0]}[{d2[rc][1]}] at ({rc[0]},{rc[1]}) = '{letter}'")
                    ic += 1
    
    print(f"\nTotal intersections: {ic}")
    print(f"Theme: Technology")

elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")