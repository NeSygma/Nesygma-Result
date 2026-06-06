from z3 import *

# Data
persons = ["Alex","Ben","Chloe","David","Grace","Harry","Eva","Frank","Ivy","Jack","Kate","Leo"]
levels = ["Senior","Senior","Senior","Senior","Senior","Senior","Junior","Junior","Junior","Junior","Junior","Junior"]
skills_dict = {
    "Alex": ["Programming","Security"],
    "Ben": ["Programming","DevOps"],
    "Chloe": ["Design","Management"],
    "David": ["Testing","DataScience"],
    "Grace": ["Management","DataScience"],
    "Harry": ["DevOps","Security"],
    "Eva": ["Programming","Cloud"],
    "Frank": ["Design","Testing"],
    "Ivy": ["Design","Cloud"],
    "Jack": ["Testing","Programming"],
    "Kate": ["Management","DevOps"],
    "Leo": ["DataScience","Security"],
}
primary_skills = ["Programming","Design","Testing","Management","DataScience","DevOps"]
synergy_pairs = [("Programming","DevOps"),("Design","DataScience"),("Management","Testing"),("Security","Cloud")]

incompat_pairs = [("Alex","Ben"),("Chloe","Grace"),("David","Harry")]
project_names = ["Alpha","Beta","Gamma"]

person_index = {name:i for i,name in enumerate(persons)}
senior_indices = [i for i,lvl in enumerate(levels) if lvl=="Senior"]
# skill presence map
has_skill_map = {}
for i,name in enumerate(persons):
    for skill in primary_skills:
        has_skill_map[(i,skill)] = skill in skills_dict[name]

solver = Optimize()

# Variables
team_of_person = [Int(f"team_of_person_{i}") for i in range(len(persons))]
for i in range(len(persons)):
    solver.add(team_of_person[i] >= 1, team_of_person[i] <= 3)

leader_of_team = [Int(f"leader_of_team_{t}") for t in range(3)]
project_of_team = [Int(f"project_of_team_{t}") for t in range(3)]
for t in range(3):
    solver.add(project_of_team[t] >= 0, project_of_team[t] <= 2)

# Distinct projects
solver.add(Distinct(project_of_team))

# Team size constraints
for t in range(3):
    solver.add(Sum([If(team_of_person[i] == t+1, 1, 0) for i in range(len(persons))]) == 4)

# Leader constraints
for t in range(3):
    # Leader must be senior
    solver.add(Or([leader_of_team[t] == i for i in senior_indices]))
    # Leader must be member of the team
    solver.add(Or([And(leader_of_team[t] == i, team_of_person[i] == t+1) for i in range(len(persons))]))

# Each person leads at most one team
for i in range(len(persons)):
    solver.add(Sum([If(leader_of_team[t] == i, 1, 0) for t in range(3)]) <= 1)

# Helper functions for skill presence in a team

def team_has_skill_expr(t, skill):
    return Or([And(team_of_person[i] == t+1, BoolVal(has_skill_map[(i,skill)])) for i in range(len(persons))])

# Helper for leader skill presence

def leader_has_skill_expr(t, skill):
    return Or([And(leader_of_team[t] == i, BoolVal(has_skill_map[(i,skill)])) for i in range(len(persons))])

# Leader skill exclusivity
for skill in primary_skills:
    solver.add(Sum([If(leader_has_skill_expr(t, skill), 1, 0) for t in range(3)]) <= 1)

# Incompatibilities
for (p1,p2) in incompat_pairs:
    i1 = person_index[p1]
    i2 = person_index[p2]
    for t in range(3):
        solver.add(Or(team_of_person[i1] != t+1, team_of_person[i2] != t+1))

# Project requirements
# Alpha requires Security, Beta requires Cloud
for t in range(3):
    solver.add(Implies(project_of_team[t] == 0, team_has_skill_expr(t, "Security")))
    solver.add(Implies(project_of_team[t] == 1, team_has_skill_expr(t, "Cloud")))

# Synergy score per team
synergy_score_vars = [Int(f"synergy_score_{t}") for t in range(3)]
for t in range(3):
    exprs = []
    for (s1,s2) in synergy_pairs:
        exprs.append(If(And(team_has_skill_expr(t, s1), team_has_skill_expr(t, s2)), 1, 0))
    solver.add(synergy_score_vars[t] == Sum(exprs))

# Total synergy
total_synergy = Int("total_synergy")
solver.add(total_synergy == Sum(synergy_score_vars))

# Objective
solver.maximize(total_synergy)

# Solve
result = solver.check()
if result == sat:
    model = solver.model()
    print("STATUS: sat")
    for t in range(3):
        proj_idx = model[project_of_team[t]].as_long()
        proj_name = project_names[proj_idx]
        leader_idx = model[leader_of_team[t]].as_long()
        leader_name = persons[leader_idx]
        members = [persons[i] for i in range(len(persons)) if model[team_of_person[i]].as_long() == t+1]
        members.sort()
        synergy_val = model[synergy_score_vars[t]].as_long()
        print(f"team_id = {t+1}")
        print(f"project = {proj_name}")
        print(f"leader = {leader_name}")
        print("members = " + ", ".join(members))
        print(f"synergy_score = {synergy_val}")
    total_val = model[total_synergy].as_long()
    print(f"total_synergy = {total_val}")
elif result == unsat:
    print("STATUS: unsat")
else:
    print("STATUS: unknown")