from z3 import *

# Problem data
words = ["CODE", "DATA", "TECH", "CHIP", "BYTE", "NET"]
clues = {
    "CODE": "Programming instructions",
    "DATA": "Information",
    "TECH": "Technology short",
    "CHIP": "Computer component",
    "BYTE": "Data unit",
    "NET": "Internet short"
}

solver = Solver()

# Variables for each word: start row, start col, direction (0=horizontal,1=vertical)
start_rows = []
start_cols = []
dirs = []
for i, w in enumerate(words):
    r = Int(f'r_{i}')
    c = Int(f'c_{i}')
    d = Int(f'd_{i}')
    solver.add(r >= 0, r <= 4)
    solver.add(c >= 0, c <= 4)
    solver.add(d >= 0, d <= 1)
    # Length constraints
    L = len(w)
    solver.add(If(d == 0, c <= 5 - L, r <= 5 - L))
    start_rows.append(r)
    start_cols.append(c)
    dirs.append(d)

# Helper: letter codes
letter_codes = {ch: ord(ch) - ord('A') for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}

# Pairwise constraints: if two words overlap, letters must match
for i in range(len(words)):
    for j in range(i+1, len(words)):
        wi = words[i]
        wj = words[j]
        Li = len(wi)
        Lj = len(wj)
        for ki in range(Li):
            for kj in range(Lj):
                # Compute coordinates of letter ki in word i
                ri = start_rows[i]
                ci = start_cols[i]
                di = dirs[i]
                r_i_k = ri + If(di == 1, ki, 0)
                c_i_k = ci + If(di == 0, ki, 0)
                # Compute coordinates of letter kj in word j
                rj = start_rows[j]
                cj = start_cols[j]
                dj = dirs[j]
                r_j_k = rj + If(dj == 1, kj, 0)
                c_j_k = cj + If(dj == 0, kj, 0)
                # If coordinates equal, letters must match
                cond = And(r_i_k == r_j_k, c_i_k == c_j_k)
                solver.add(Implies(cond, letter_codes[wi[ki]] == letter_codes[wj[kj]]))

# Solve
result = solver.check()
if result == sat:
    m = solver.model()
    # Build grid
    grid = [[' ' for _ in range(5)] for _ in range(5)]
    word_placements = []
    for idx, w in enumerate(words):
        r = m[start_rows[idx]].as_long()
        c = m[start_cols[idx]].as_long()
        d = m[dirs[idx]].as_long()
        direction_str = 'horizontal' if d == 0 else 'vertical'
        word_placements.append({
            'word': w,
            'position': [r, c],
            'direction': direction_str,
            'clue': clues[w]
        })
        for k, ch in enumerate(w):
            rr = r + (k if d == 1 else 0)
            cc = c + (k if d == 0 else 0)
            grid[rr][cc] = ch
    # Compute intersections
    intersections = []
    for i in range(len(words)):
        for j in range(i+1, len(words)):
            wi = words[i]
            wj = words[j]
            Li = len(wi)
            Lj = len(wj)
            for ki in range(Li):
                for kj in range(Lj):
                    # coordinates
                    r_i_k = m[start_rows[i]].as_long() + (ki if m[dirs[i]].as_long() == 1 else 0)
                    c_i_k = m[start_cols[i]].as_long() + (ki if m[dirs[i]].as_long() == 0 else 0)
                    r_j_k = m[start_rows[j]].as_long() + (kj if m[dirs[j]].as_long() == 1 else 0)
                    c_j_k = m[start_cols[j]].as_long() + (kj if m[dirs[j]].as_long() == 0 else 0)
                    if r_i_k == r_j_k and c_i_k == c_j_k and wi[ki] == wj[kj]:
                        intersections.append({
                            'word1': i,
                            'word2': j,
                            'position1': ki,
                            'position2': kj,
                            'letter': wi[ki]
                        })
    # Print solution
    print("STATUS: sat")
    print("grid:")
    for row in grid:
        print(''.join(row))
    print("words:")
    for w in word_placements:
        print(w)
    print("theme: Technology")
    print("intersections:")
    for inter in intersections:
        print(inter)
else:
    print("STATUS: unsat")
    if result == unsat:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
    else:
        print("STATUS: unknown")