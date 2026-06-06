from z3 import *

# Teams: A=0, B=1, C=2, D=3
N_TEAMS = 4
N_ROUNDS = 6

# Distance matrix (symmetric)
dist = [
    [0, 5, 6, 8.2],
    [5, 0, 5, 5.7],
    [6, 5, 0, 10],
    [8.2, 5.7, 10, 0]
]

solver = Optimize()

# match[r][i][j] = True if team i hosts team j in round r (i != j)
match = [[[Bool(f'm_{r}_{i}_{j}') for j in range(N_TEAMS)] for i in range(N_TEAMS)] for r in range(N_ROUNDS)]

# Constraint 0: No self-match
for r in range(N_ROUNDS):
    for i in range(N_TEAMS):
        solver.add(Not(match[r][i][i]))

# Constraint 1: Double round-robin - each ordered pair (i,j), i!=j, appears exactly once
for i in range(N_TEAMS):
    for j in range(N_TEAMS):
        if i != j:
            # Sum over rounds of match[r][i][j] == 1
            solver.add(Sum([If(match[r][i][j], 1, 0) for r in range(N_ROUNDS)]) == 1)

# Constraint 2 & 3: Each round, each team plays exactly once (and exactly 2 matches per round)
for r in range(N_ROUNDS):
    for i in range(N_TEAMS):
        # Team i either hosts someone or is hosted by someone, exactly once
        solver.add(
            Sum([If(match[r][i][j], 1, 0) for j in range(N_TEAMS) if j != i]) +
            Sum([If(match[r][j][i], 1, 0) for j in range(N_TEAMS) if j != i])
            == 1
        )
    # Exactly 2 matches per round (implied by above but add explicit)
    solver.add(
        Sum([If(match[r][i][j], 1, 0) for i in range(N_TEAMS) for j in range(N_TEAMS) if i != j]) == 2
    )

# Constraint: No mutual hosting in same round (i hosts j and j hosts i in same round)
for r in range(N_ROUNDS):
    for i in range(N_TEAMS):
        for j in range(N_TEAMS):
            if i < j:
                solver.add(Not(And(match[r][i][j], match[r][j][i])))

# Constraint 4: No team plays more than 2 consecutive home games
for i in range(N_TEAMS):
    for r in range(N_ROUNDS - 2):
        # Sum of home games in rounds r, r+1, r+2 <= 2
        home_expr = Sum([
            If(match[r+k][i][j], 1, 0)
            for k in range(3)
            for j in range(N_TEAMS) if j != i
        ])
        solver.add(home_expr <= 2)

# Constraint 5: No team plays more than 2 consecutive away games
for i in range(N_TEAMS):
    for r in range(N_ROUNDS - 2):
        away_expr = Sum([
            If(match[r+k][j][i], 1, 0)
            for k in range(3)
            for j in range(N_TEAMS) if j != i
        ])
        solver.add(away_expr <= 2)

# Objective: Minimize total travel distance
# Travel for match[r][i][j] (i hosts j) = dist[i][j] (one-way from j's home to i's home)
# Since teams return home after each round, it's round-trip: 2 * dist[i][j]
# Let's use one-way first, then see
total_travel = Sum([
    If(match[r][i][j], 2 * dist[i][j], 0)
    for r in range(N_ROUNDS)
    for i in range(N_TEAMS)
    for j in range(N_TEAMS) if i != j
])

solver.minimize(total_travel)

print("Solving...")
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print(f"Total travel (round-trip) = {m.eval(total_travel)}")
    print()
    print("Schedule:")
    team_names = ['A', 'B', 'C', 'D']
    for r in range(N_ROUNDS):
        matches_in_round = []
        for i in range(N_TEAMS):
            for j in range(N_TEAMS):
                if i != j and is_true(m.eval(match[r][i][j])):
                    matches_in_round.append(f"{team_names[i]} vs {team_names[j]} (home: {team_names[i]})")
        print(f"Round {r+1}: {', '.join(matches_in_round)}")
    print()
    # Also print home/away sequences
    print("Home/Away sequences per team (H=home, A=away):")
    for i in range(N_TEAMS):
        seq = ""
        for r in range(N_ROUNDS):
            is_home = False
            for j in range(N_TEAMS):
                if i != j and is_true(m.eval(match[r][i][j])):
                    is_home = True
                    break
            seq += "H" if is_home else "A"
        print(f"  {team_names[i]}: {seq}")
elif result == unsat:
    print("STATUS: unsat")
    print("No feasible schedule exists.")
else:
    print("STATUS: unknown")