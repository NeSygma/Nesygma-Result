from z3 import *

# ============================================================
# DATA
# ============================================================
personnel = ["Alex", "Ben", "Chloe", "David", "Grace", "Harry",
             "Eva", "Frank", "Ivy", "Jack", "Kate", "Leo"]

seniors = ["Alex", "Ben", "Chloe", "David", "Grace", "Harry"]
juniors = ["Eva", "Frank", "Ivy", "Jack", "Kate", "Leo"]

# Skills per person
skills = {
    "Alex":   {"Programming", "Security"},
    "Ben":    {"Programming", "DevOps"},
    "Chloe":  {"Design", "Management"},
    "David":  {"Testing", "DataScience"},
    "Grace":  {"Management", "DataScience"},
    "Harry":  {"DevOps", "Security"},
    "Eva":    {"Programming", "Cloud"},
    "Frank":  {"Design", "Testing"},
    "Ivy":    {"Design", "Cloud"},
    "Jack":   {"Testing", "Programming"},
    "Kate":   {"Management", "DevOps"},
    "Leo":    {"DataScience", "Security"}
}

# Primary skills (mutually exclusive for leaders)
primary_skills = ["Programming", "Design", "Testing", "Management", "DataScience", "DevOps"]

# Incompatibilities
incompat = [("Alex","Ben"), ("Chloe","Grace"), ("David","Harry")]

# Synergy pairs
synergy_pairs = [("Programming","DevOps"), ("Design","DataScience"),
                 ("Management","Testing"), ("Security","Cloud")]

# Projects
projects = ["Alpha", "Beta", "Gamma"]
# Project skill requirements
project_req = {
    "Alpha": {"Security"},
    "Beta":  {"Cloud"},
    "Gamma": set()
}

N = len(personnel)  # 12
T = 3  # teams

# ============================================================
# DECISION VARIABLES
# ============================================================
# team_of[p] = 0,1,2 (which team each person is assigned to)
team_of = [Int(f"team_{p}") for p in range(N)]

# project_of[t] = 0,1,2 (which project team t gets)
project_of = [Int(f"proj_{t}") for t in range(T)]

# leader_of[t] = person index (0..N-1) who is leader of team t
leader_of = [Int(f"leader_{t}") for t in range(T)]

# synergy[t] = integer synergy score for team t
synergy = [Int(f"synergy_{t}") for t in range(T)]

solver = Optimize()

# ============================================================
# DOMAIN CONSTRAINTS
# ============================================================
# Team assignments: each person to team 0,1,2
for p in range(N):
    solver.add(team_of[p] >= 0, team_of[p] <= 2)

# Project assignments: each team to project 0,1,2 (all different)
for t in range(T):
    solver.add(project_of[t] >= 0, project_of[t] <= 2)
solver.add(Distinct(project_of))

# Leaders: each leader is a person index 0..N-1
for t in range(T):
    solver.add(leader_of[t] >= 0, leader_of[t] <= N-1)

# ============================================================
# CONSTRAINT 1: Team Size = 4
# ============================================================
for t in range(T):
    solver.add(Sum([If(team_of[p] == t, 1, 0) for p in range(N)]) == 4)

# ============================================================
# CONSTRAINT 4: Leadership - each team has exactly one leader who is Senior
# ============================================================
# The leader must be on the team
for t in range(T):
    solver.add(Or([And(leader_of[t] == p, team_of[p] == t) for p in range(N)]))

# The leader must be a Senior
for t in range(T):
    solver.add(Or([leader_of[t] == p for p in range(N) if personnel[p] in seniors]))

# No two teams share the same leader (each leader unique)
solver.add(Distinct(leader_of))

# ============================================================
# CONSTRAINT 5: Leader Skills - mutually exclusive primary skills
# ============================================================
# For each team, the leader must have a primary skill.
# We encode: for each team t, for each primary skill idx, 
# if leader_primary[t] == idx then the leader has that skill.
# Use a fresh integer variable for each team's leader primary skill index.
leader_primary = [Int(f"leader_primary_{t}") for t in range(T)]
for t in range(T):
    solver.add(leader_primary[t] >= 0, leader_primary[t] <= len(primary_skills)-1)
    # The leader must have the skill at that index
    # For each possible person p, if leader_of[t] == p, then 
    # the person must have primary_skills[leader_primary[t]] in their skills.
    # Use Or-loop to avoid indexing Python list with Z3 variable.
    for p in range(N):
        p_skills = skills[personnel[p]]
        solver.add(Implies(leader_of[t] == p,
                           Or([leader_primary[t] == idx for idx in range(len(primary_skills))
                               if primary_skills[idx] in p_skills])))

# All leaders have different primary skills
solver.add(Distinct(leader_primary))

# ============================================================
# CONSTRAINT 6: Incompatibilities
# ============================================================
for (p1_name, p2_name) in incompat:
    p1_idx = personnel.index(p1_name)
    p2_idx = personnel.index(p2_name)
    solver.add(team_of[p1_idx] != team_of[p2_idx])

# ============================================================
# CONSTRAINT 7: Project Requirements
# ============================================================
for t in range(T):
    for proj_idx, proj_name in enumerate(projects):
        req_skills = project_req[proj_name]
        for skill in req_skills:
            # If team t gets project proj_idx, then some member of team t has the required skill
            solver.add(Implies(project_of[t] == proj_idx,
                               Or([And(team_of[p] == t, Or([skill == s for s in skills[personnel[p]]])) 
                                   for p in range(N)])))

# ============================================================
# SYNERGY SCORE CALCULATION
# ============================================================
for t in range(T):
    synergy_terms = []
    for (sk1, sk2) in synergy_pairs:
        has_sk1 = Or([And(team_of[p] == t, Or([sk1 == s for s in skills[personnel[p]]])) for p in range(N)])
        has_sk2 = Or([And(team_of[p] == t, Or([sk2 == s for s in skills[personnel[p]]])) for p in range(N)])
        synergy_terms.append(If(And(has_sk1, has_sk2), 1, 0))
    solver.add(synergy[t] == Sum(synergy_terms))

total_synergy = Sum(synergy)

# ============================================================
# OBJECTIVE: Maximize total synergy
# ============================================================
solver.maximize(total_synergy)

# ============================================================
# SOLVE
# ============================================================
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    
    # Extract team assignments
    teams_data = {0: [], 1: [], 2: []}
    for p in range(N):
        t = m[team_of[p]].as_long()
        teams_data[t].append(personnel[p])
    
    # Extract project assignments
    proj_names = {0: "Alpha", 1: "Beta", 2: "Gamma"}
    team_projects = {}
    for t in range(T):
        pj = m[project_of[t]].as_long()
        team_projects[t] = proj_names[pj]
    
    # Extract leaders
    team_leaders = {}
    for t in range(T):
        l = m[leader_of[t]].as_long()
        team_leaders[t] = personnel[l]
    
    # Extract synergy scores
    team_synergies = {}
    for t in range(T):
        team_synergies[t] = m[synergy[t]].as_long()
    
    total_syn = sum(team_synergies.values())
    
    print(f"total_synergy = {total_syn}")
    for t in range(T):
        members_sorted = sorted(teams_data[t])
        print(f"Team {t+1}: project={team_projects[t]}, leader={team_leaders[t]}, members={members_sorted}, synergy={team_synergies[t]}")
    
    if total_syn == 11:
        print("Optimal synergy 11 achieved!")
    else:
        print(f"Synergy is {total_syn}, expected 11")
        
elif result == unsat:
    print("STATUS: unsat")
    print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")