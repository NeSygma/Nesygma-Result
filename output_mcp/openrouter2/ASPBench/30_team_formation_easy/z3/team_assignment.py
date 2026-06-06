from z3 import *

# Problem data
people = ['Alice', 'Bob', 'Carol', 'Dave', 'Eve', 'Frank', 'Grace', 'Henry']
skills = {
    'Alice': ['Programming', 'Design'],
    'Bob': ['Programming', 'Testing'],
    'Carol': ['Design', 'Management'],
    'Dave': ['Testing', 'Management'],
    'Eve': ['Programming', 'Documentation'],
    'Frank': ['Design', 'Documentation'],
    'Grace': ['Testing', 'Documentation'],
    'Henry': ['Management', 'Documentation']
}
required_skills = ['Programming', 'Design', 'Testing', 'Management']

# All unique skills (including optional)
all_skills = set()
for s_list in skills.values():
    all_skills.update(s_list)

# Solver
opt = Optimize()

# Team assignment variables: 0 or 1
team_of = {p: Int(f"team_{p}") for p in people}
for p in people:
    opt.add(team_of[p] >= 0, team_of[p] <= 1)

# Team size constraints
opt.add(Sum([If(team_of[p] == 0, 1, 0) for p in people]) == 4)
opt.add(Sum([If(team_of[p] == 1, 1, 0) for p in people]) == 4)

# Skill coverage constraints
for t in [0, 1]:
    for skill in required_skills:
        opt.add(Sum([If(skill in skills[p] and team_of[p] == t, 1, 0) for p in people]) >= 1)

# Objective: minimize skill overlap within teams
overlap_terms = []
for t in [0, 1]:
    for skill in all_skills:
        count = Sum([If(skill in skills[p] and team_of[p] == t, 1, 0) for p in people])
        overlap_terms.append(If(count > 1, count - 1, 0))
opt.minimize(Sum(overlap_terms))

# Solve
result = opt.check()
if result == sat:
    m = opt.model()
    team0 = [p for p in people if m[team_of[p]].as_long() == 0]
    team1 = [p for p in people if m[team_of[p]].as_long() == 1]
    print("STATUS: sat")
    print("teams = [", team0, ",", team1, "]", sep='')
else:
    print("STATUS: unsat")