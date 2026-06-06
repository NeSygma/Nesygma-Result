from z3 import *

# Data definitions
names = ["Alex", "Ben", "Chloe", "David", "Grace", "Harry", "Eva", "Frank", "Ivy", "Jack", "Kate", "Leo"]
# indices 0-11
senior_set = {0,1,2,3,4,5}  # first six are seniors
# Skills per person (list of strings)
skills = [
    ["Programming", "Security"],   # Alex
    ["Programming", "DevOps"],    # Ben
    ["Design", "Management"],     # Chloe
    ["Testing", "DataScience"],   # David
    ["Management", "DataScience"],# Grace
    ["DevOps", "Security"],       # Harry
    ["Programming", "Cloud"],     # Eva
    ["Design", "Testing"],        # Frank
    ["Design", "Cloud"],          # Ivy
    ["Testing", "Programming"],   # Jack
    ["Management", "DevOps"],     # Kate
    ["DataScience", "Security"]   # Leo
]
# Primary skill mapping (first listed skill for seniors)
primary_skill = {0:"Programming", 1:"Programming", 2:"Design", 3:"Testing", 4:"Management", 5:"DevOps"}
# Incompatibility pairs (indices)
incompat = [(0,1), (2,4), (3,5)]
# Projects mapping
proj_names = ["Alpha", "Beta", "Gamma"]
proj_req = {0:"Security", 1:"Cloud", 2:None}  # requirement skill per project index
# Synergy pairs
synergy_pairs = [("Programming","DevOps"), ("Design","DataScience"), ("Management","Testing"), ("Security","Cloud")]

# Helper to check if a person has a skill
def has_skill(person_idx, skill):
    return skill in skills[person_idx]

# Z3 variables
team_of = [Int(f"team_{i}") for i in range(12)]  # each person assigned to team 1..3
project_of = [Int(f"proj_{t}") for t in range(3)]   # project assigned to team t (0..2 index into proj_names)
leader_of = [Int(f"leader_{t}") for t in range(3)]   # leader person index for team t

opt = Optimize()

# Domain constraints
for tvar in team_of:
    opt.add(tvar >= 1, tvar <= 3)
for pvar in project_of:
    opt.add(pvar >= 0, pvar <= 2)
# each project assigned to distinct team
opt.add(Distinct(project_of))

# Team size constraints (exactly 4 members per team)
for t in range(1,4):
    opt.add(Sum([If(team_of[p]==t, 1, 0) for p in range(12)]) == 4)

# Leader constraints: senior and belongs to the team
for t in range(3):
    # senior
    opt.add(Or([leader_of[t] == s for s in senior_set]))
    # belongs to team t+1
    # Encode: for each possible person i, if leader_of[t]==i then team_of[i]==t+1
    for i in range(12):
        opt.add(Implies(leader_of[t] == i, team_of[i] == t+1))

# Distinct primary skills among leaders
for t1 in range(3):
    for t2 in range(t1+1,3):
        l1 = leader_of[t1]
        l2 = leader_of[t2]
        # For all senior i,j with different primary skills, allow those combos
        combos = []
        for i in senior_set:
            for j in senior_set:
                if i != j and primary_skill[i] != primary_skill[j]:
                    combos.append(And(l1 == i, l2 == j))
        opt.add(Or(combos))

# Incompatibility constraints: cannot be on same team
for (a,b) in incompat:
    opt.add(team_of[a] != team_of[b])

# Precompute boolean expressions for team_has_skill[t][skill]
team_has_skill = {}
all_skills = ["Programming","Design","Testing","Management","DataScience","DevOps","Security","Cloud"]
for t in range(1,4):
    for skill in all_skills:
        persons_with = [p for p in range(12) if has_skill(p, skill)]
        if persons_with:
            team_has_skill[(t,skill)] = Or([team_of[p]==t for p in persons_with])
        else:
            team_has_skill[(t,skill)] = BoolVal(False)

# Project requirement constraints
for t in range(1,4):
    proj = project_of[t-1]
    # Alpha (0) requires Security
    opt.add(Implies(proj == 0, team_has_skill[(t, "Security")]))
    # Beta (1) requires Cloud
    opt.add(Implies(proj == 1, team_has_skill[(t, "Cloud")]))
    # Gamma (2) no requirement (nothing to add)

# Synergy calculation per team
synergy_team = []
for t in range(1,4):
    pair_counts = []
    for (a,b) in synergy_pairs:
        a_present = team_has_skill[(t,a)]
        b_present = team_has_skill[(t,b)]
        pair_counts.append(If(And(a_present, b_present), 1, 0))
    synergy = Sum(pair_counts)
    synergy_team.append(synergy)

total_synergy = Sum(synergy_team)
opt.maximize(total_synergy)

# Solve
if opt.check() == sat:
    m = opt.model()
    print("STATUS: sat")
    total = m.eval(total_synergy).as_long()
    print("total_synergy =", total)
    for t in range(1,4):
        proj_idx = m.eval(project_of[t-1]).as_long()
        proj_name = proj_names[proj_idx]
        leader_idx = m.eval(leader_of[t-1]).as_long()
        leader_name = names[leader_idx]
        members = [names[p] for p in range(12) if m.eval(team_of[p]).as_long() == t]
        members.sort()
        synergy_val = m.eval(synergy_team[t-1]).as_long()
        print(f"Team {t}:")
        print("  project =", proj_name)
        print("  leader =", leader_name)
        print("  members =", members)
        print("  synergy_score =", synergy_val)
else:
    print("STATUS: unsat")