from z3 import *

# Data
personnel = [
    ("Alex", "Senior", ["Programming", "Security"]),
    ("Ben", "Senior", ["Programming", "DevOps"]),
    ("Chloe", "Senior", ["Design", "Management"]),
    ("David", "Senior", ["Testing", "DataScience"]),
    ("Grace", "Senior", ["Management", "DataScience"]),
    ("Harry", "Senior", ["DevOps", "Security"]),
    ("Eva", "Junior", ["Programming", "Cloud"]),
    ("Frank", "Junior", ["Design", "Testing"]),
    ("Ivy", "Junior", ["Design", "Cloud"]),
    ("Jack", "Junior", ["Testing", "Programming"]),
    ("Kate", "Junior", ["Management", "DevOps"]),
    ("Leo", "Junior", ["DataScience", "Security"]),
]

projects = [
    ("Alpha", ["Security"]),
    ("Beta", ["Cloud"]),
    ("Gamma", []),
]

synergy_pairs = [
    ("Programming", "DevOps"),
    ("Design", "DataScience"),
    ("Management", "Testing"),
    ("Security", "Cloud"),
]

incompatibilities = [("Alex", "Ben"), ("Chloe", "Grace"), ("David", "Harry")]

# Z3 Model
solver = Optimize()

# Decision variables
# Team assignment: person -> team_id (1,2,3)
team_assignment = {p[0]: Int(f"team_{p[0]}") for p in personnel}

# Project assignment: team_id -> project_name
project_assignment = {f"team_{i+1}": String(f"project_team_{i+1}") for i in range(3)}

# Leader assignment: team_id -> leader_name
leader_assignment = {f"team_{i+1}": String(f"leader_team_{i+1}") for i in range(3)}

# Synergy score per team
synergy_score = {f"team_{i+1}": Int(f"synergy_team_{i+1}") for i in range(3)}

# Total synergy
total_synergy = Int("total_synergy")

# Helper: skill presence per person
skill_presence = {p[0]: {s: Bool(f"{p[0]}_has_{s}") for s in ["Programming", "Design", "Testing", "Management", "DataScience", "DevOps", "Security", "Cloud"]} for p in personnel}

# Helper: person is Senior
is_senior = {p[0]: Bool(f"{p[0]}_is_senior") for p in personnel}

# Initialize skill presence and senior status
for p in personnel:
    name, level, skills = p
    for s in ["Programming", "Design", "Testing", "Management", "DataScience", "DevOps", "Security", "Cloud"]:
        solver.add(skill_presence[name][s] == (s in skills))
    solver.add(is_senior[name] == (level == "Senior"))

# Each person assigned to exactly one team
for p in personnel:
    solver.add(team_assignment[p[0]] >= 1, team_assignment[p[0]] <= 3)

# All team assignments are distinct (each person to exactly one team)
solver.add(Distinct(list(team_assignment.values())))

# Each team has exactly 4 members
for t in range(1, 4):
    solver.add(Sum([If(team_assignment[p[0]] == t, 1, 0) for p in personnel]) == 4)

# Each team has exactly one Senior leader
for t in range(1, 4):
    team_members = [p[0] for p in personnel]
    leader_candidates = [
        And(
            team_assignment[p[0]] == t,
            is_senior[p[0]],
            leader_assignment[f"team_{t}"] == p[0]
        ) for p in personnel
    ]
    solver.add(Or(leader_candidates))
    solver.add(Sum([If(And(team_assignment[p[0]] == t, is_senior[p[0]]), 1, 0) for p in personnel]) == 1)

# Leaders have mutually exclusive primary skills
leader_skills = []
for t in range(1, 4):
    leader_name = leader_assignment[f"team_{t}"]
    # Get the leader's skills
    leader_skill_exprs = []
    for s in ["Programming", "Design", "Testing", "Management", "DataScience", "DevOps", "Security", "Cloud"]:
        leader_skill_exprs.append(If(leader_name == personnel[i][0], skill_presence[personnel[i][0]][s], False) for i in range(len(personnel)))
    # Simplify: use a single skill per leader (the first one present)
    # Instead, we enforce that for any two leaders, their skill sets are disjoint
    for t2 in range(t + 1, 4):
        for s in ["Programming", "Design", "Testing", "Management", "DataScience", "DevOps", "Security", "Cloud"]:
            solver.add(Not(And(
                Or([And(leader_assignment[f"team_{t}"] == personnel[i][0], skill_presence[personnel[i][0]][s]) for i in range(len(personnel))]),
                Or([And(leader_assignment[f"team_{t2}"] == personnel[i][0], skill_presence[personnel[i][0]][s]) for i in range(len(personnel))])
            )))

# Incompatibilities: Alex-Ben, Chloe-Grace, David-Harry cannot be on the same team
for (p1, p2) in incompatibilities:
    solver.add(Not(And(team_assignment[p1] == team_assignment[p2])))

# Project requirements
for i, (proj_name, required_skills) in enumerate(projects):
    team_id = i + 1
    for s in required_skills:
        solver.add(Sum([If(And(team_assignment[p[0]] == team_id, skill_presence[p[0]][s]), 1, 0) for p in personnel]) >= 1)

# Synergy score per team
for t in range(1, 4):
    team_members = [p[0] for p in personnel if p[0] in team_assignment and team_assignment[p[0]] == t]
    # For each synergy pair, check if both skills are present in the team
    synergy_exprs = []
    for (s1, s2) in synergy_pairs:
        # Check if at least one member has s1 and at least one (possibly same) member has s2
        has_s1 = Or([skill_presence[m][s1] for m in team_members])
        has_s2 = Or([skill_presence[m][s2] for m in team_members])
        synergy_exprs.append(If(And(has_s1, has_s2), 1, 0))
    solver.add(synergy_score[f"team_{t}"] == Sum(synergy_exprs))

# Total synergy
solver.add(total_synergy == Sum([synergy_score[f"team_{t}"] for t in range(1, 4)]))

# Maximize total synergy
solver.maximize(total_synergy)

# Check and print results
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print("Total synergy:", model[total_synergy])
    
    # Print team assignments
    for t in range(1, 4):
        team_id = f"team_{t}"
        project = model[project_assignment[team_id]]
        leader = model[leader_assignment[team_id]]
        members = sorted([p[0] for p in personnel if model[team_assignment[p[0]]] == t])
        synergy = model[synergy_score[team_id]]
        print(f"Team {t}: project={project}, leader={leader}, members={members}, synergy={synergy}")
    
    # Assert expected synergy
    if model[total_synergy].as_long() == 11:
        print("Expected optimal synergy achieved.")
    else:
        print(f"WARNING: Expected synergy 11, got {model[total_synergy]}.")
        
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")