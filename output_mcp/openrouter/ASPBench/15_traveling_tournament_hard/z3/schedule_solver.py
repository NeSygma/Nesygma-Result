from z3 import *

BENCHMARK_MODE = True

teams = ['A','B','C','D','E','F']
team_idx = {t:i for i,t in enumerate(teams)}
N = len(teams)
R = 10

home_coords = [(0,0), (10,0), (5,8), (0,15), (10,15), (15,8)]
home_x_vals = [c[0] for c in home_coords]
home_y_vals = [c[1] for c in home_coords]

solver = Solver()

# round variables for ordered pairs
round_var = {}
for i in range(N):
    for j in range(N):
        if i==j: continue
        v = Int(f'round_{i}_{j}')
        round_var[(i,j)] = v
        solver.add(v >= 0, v < R)

# home flag and opponent per team per round
home = [[Bool(f'home_{t}_{r}') for r in range(R)] for t in range(N)]
opp = [[Int(f'opp_{t}_{r}') for r in range(R)] for t in range(N)]
for t in range(N):
    for r in range(R):
        solver.add(opp[t][r] >= 0, opp[t][r] < N)
        solver.add(opp[t][r] != t)

# linking constraints
for i in range(N):
    for r in range(R):
        for k in range(N):
            if k==i: continue
            # forward implication
            solver.add(Implies(round_var[(i,k)] == r,
                               And(home[i][r], opp[i][r] == k)))
            solver.add(Implies(round_var[(k,i)] == r,
                               And(Not(home[i][r]), opp[i][r] == k)))
            # converse
            solver.add(Implies(And(home[i][r], opp[i][r] == k), round_var[(i,k)] == r))
            solver.add(Implies(And(Not(home[i][r]), opp[i][r] == k), round_var[(k,i)] == r))

# each team exactly once per round
for t in range(N):
    for r in range(R):
        exprs = []
        for j in range(N):
            if j==t: continue
            exprs.append(If(round_var[(t,j)] == r, 1, 0))
            exprs.append(If(round_var[(j,t)] == r, 1, 0))
        solver.add(Sum(exprs) == 1)

# consecutive home/away limit (no 4 in a row)
for t in range(N):
    for s in range(R-3):
        solver.add(Not(And([home[t][s+i] for i in range(4)])))
        solver.add(Not(And([Not(home[t][s+i]) for i in range(4)])))

# mandatory break: at least one pair of consecutive home games
for t in range(N):
    opts = []
    for r in range(R-1):
        opts.append(And(home[t][r], home[t][r+1]))
    solver.add(Or(opts))

# rivalry constraints round 0
A = team_idx['A']; B = team_idx['B']; C = team_idx['C']; D = team_idx['D']
solver.add(round_var[(A,B)] != 0)
solver.add(round_var[(B,A)] != 0)
solver.add(round_var[(C,D)] != 0)
solver.add(round_var[(D,C)] != 0)

# helper to get home coordinate based on opponent index expression
def coord_of(idx_expr, coord_list):
    # returns Sum([If(idx_expr == k, coord_list[k], 0) for k])
    return Sum([If(idx_expr == k, coord_list[k], 0) for k in range(N)])

# location after each round
loc_x = [[Int(f'locx_{t}_{r}') for r in range(R)] for t in range(N)]
loc_y = [[Int(f'locy_{t}_{r}') for r in range(R)] for t in range(N)]
for t in range(N):
    for r in range(R):
        opp_home_x = coord_of(opp[t][r], home_x_vals)
        opp_home_y = coord_of(opp[t][r], home_y_vals)
        solver.add(loc_x[t][r] == If(home[t][r], home_x_vals[t], opp_home_x))
        solver.add(loc_y[t][r] == If(home[t][r], home_y_vals[t], opp_home_y))

# travel fatigue constraint
MAX_DIST2 = 140*140  # 19600
for t in range(N):
    for r in range(R-1):
        # previous location after round r-1 (or home city if r==0)
        prev_x = If(r == 0, home_x_vals[t], loc_x[t][r-1])
        prev_y = If(r == 0, home_y_vals[t], loc_y[t][r-1])
        # opponent home coordinates for round r
        opp_home_x = coord_of(opp[t][r], home_x_vals)
        opp_home_y = coord_of(opp[t][r], home_y_vals)
        dx = prev_x - opp_home_x
        dy = prev_y - opp_home_y
        dist2 = dx*dx + dy*dy
        solver.add(Implies(And(Not(home[t][r]), dist2 > MAX_DIST2), home[t][r+1]))

# solve
res = solver.check()
if res == sat:
    m = solver.model()
    print("STATUS: sat")
    # build schedule
    schedule = [[] for _ in range(R)]
    for i in range(N):
        for j in range(N):
            if i==j: continue
            r = m.eval(round_var[(i,j)]).as_long()
            schedule[r].append((teams[i], teams[j]))
    for r in range(R):
        print(f"Round {r+1}:")
        for h,a in schedule[r]:
            print(f"  {h} vs {a}")
elif res == unsat:
    print("STATUS: unsat")
else:
    print("STATUS: unknown")