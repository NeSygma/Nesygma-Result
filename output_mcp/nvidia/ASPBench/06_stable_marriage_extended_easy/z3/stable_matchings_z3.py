from z3 import *

# -------------------------------------------------
# 1. Define allowed pairs (both find each other acceptable)
# -------------------------------------------------
allowed_pairs = [
    ('m1','w1'), ('m1','w2'), ('m1','w3'),
    ('m2','w2'), ('m2','w3'), ('m2','w4'),
    ('m3','w1'), ('m3','w3'), ('m3','w4'),
    ('m4','w1'), ('m4','w2'), ('m4','w4')
]

# -------------------------------------------------
# 2. Preference ranks (lower = higher preference)
# -------------------------------------------------
# Men's ranks
man_rank = {
    ('m1','w1'): 0, ('m1','w2'): 1, ('m1','w3'): 2,
    ('m2','w2'): 0, ('m2','w3'): 1, ('m2','w4'): 2,
    ('m3','w3'): 0, ('m3','w4'): 1, ('m3','w1'): 2,
    ('m4','w4'): 0, ('m4','w1'): 1, ('m4','w2'): 2
}
# Women's ranks
woman_rank = {
    ('w1','m4'): 0, ('w1','m1'): 1, ('w1','m3'): 2,
    ('w2','m1'): 0, ('w2','m2'): 1, ('w2','m4'): 2,
    ('w3','m2'): 0, ('w3','m3'): 1, ('w3','m1'): 2,
    ('w4','m3'): 0, ('w4','m4'): 1, ('w4','m2'): 2
}

# -------------------------------------------------
# 3. Boolean variables for each allowed pair
# -------------------------------------------------
match = {}
for (man, woman) in allowed_pairs:
    match[(man, woman)] = Bool(f"match_{man}_{woman}")

solver = Solver()

# -------------------------------------------------
# 4. At most one partner per man and per woman
# -------------------------------------------------
men = ['m1','m2','m3','m4']
women = ['w1','w2','w3','w4']

# each man: sum of his match vars <= 1
for man in men:
    man_vars = [match[(man, w)] for w in women if (man, w) in match]
    solver.add(Sum([If(v, 1, 0) for v in man_vars]) <= 1)

# each woman: sum of her match vars <= 1
for woman in women:
    woman_vars = [match[(m, woman)] for m in men if (m, woman) in match]
    solver.add(Sum([If(v, 1, 0) for v in woman_vars]) <= 1)

# -------------------------------------------------
# 5. Current partner rank for each person
#    (100 represents "unmatched")
# -------------------------------------------------
def rank_current_man(m):
    # chain of Ifs: if matched to w, return rank; else keep searching
    expr = 100
    for (mm, ww) in allowed_pairs:
        if mm == m:
            expr = If(match[(mm, ww)], IntVal(man_rank[(mm, ww)]), expr)
    return expr

def rank_current_woman(w):
    expr = 100
    for (mm, ww) in allowed_pairs:
        if ww == w:
            expr = If(match[(mm, ww)], IntVal(woman_rank[(ww, mm)]), expr)
    return expr

rank_m = {m: rank_current_man(m) for m in men}
rank_w = {w: rank_current_woman(w) for w in women}

# -------------------------------------------------
# 6. Blocking pair constraints
# -------------------------------------------------
for (man, woman) in allowed_pairs:
    # clause: either they are matched, or man does NOT prefer her over current,
    # or woman does NOT prefer him over current
    solver.add(
        Or(
            match[(man, woman)],
            rank_m[man] <= IntVal(man_rank[(man, woman)]),
            rank_w[woman] <= IntVal(woman_rank[(woman, man)])
        )
    )

# -------------------------------------------------
# 7. Enumerate all stable matchings
# -------------------------------------------------
solutions = []
while solver.check() == sat:
    m = solver.model()
    # collect pairs for this solution
    pairs = []
    for (man, woman), var in match.items():
        if m.eval(var, model_completion=True).is_true():
            pairs.append([man, woman])
    solutions.append(pairs)
    # block this exact solution
    solver.add(Or([var != m.eval(var, model_completion=True).is_true() for var in match.values()]))

# -------------------------------------------------
# 8. Output results
# -------------------------------------------------
if len(solutions) > 0:
    print("STATUS: sat")
    print(f"count: {len(solutions)}")
    print(f"stable_matchings: {solutions}")
else:
    print("STATUS: unsat")