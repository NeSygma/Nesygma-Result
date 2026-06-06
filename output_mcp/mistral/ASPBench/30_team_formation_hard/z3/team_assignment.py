from z3 import *

# BENCHMARK_MODE: ON (problem is guaranteed solvable)
BENCHMARK_MODE = True

# ============================================================================
# DATA DEFINITIONS
# ============================================================================

# Personnel list with their attributes
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

# Senior personnel names
seniors = [name for name, level, _ in personnel if level == "Senior"]

# Project definitions
projects = ["Alpha", "Beta", "Gamma"]
project_requirements = {
    "Alpha": ["Security"],
    "Beta": ["Cloud"],
    "Gamma": []
}

# Synergy pairs (skill1, skill2)
synergy_pairs = [
    ("Programming", "DevOps"),
    ("Design", "DataScience"),
    ("Management", "Testing"),
    ("Security", "Cloud")
]

# Incompatibilities (cannot be on the same team)
incompatibilities = [("Alex", "Ben"), ("Chloe", "Grace"), ("David", "Harry")]

# Extract primary skills for each senior (first skill in the list)
senior_primary_skills = {name: skills[0] for name, level, skills in personnel if level == "Senior"}

# ============================================================================
# Z3 MODEL
# ============================================================================

solver = Solver()

# ----------------------------------------------------------------------------
# Decision Variables
# ----------------------------------------------------------------------------

# team_of[person] = team_id (0, 1, 2)
team_of = {name: Int(f"team_of_{name}") for name, _, _ in personnel}

# project_of[team_id] = project_name (0:Alpha, 1:Beta, 2:Gamma)
project_of = {i: Int(f"project_of_team_{i}") for i in range(3)}

# leader_of[team_id] = person_name (Senior only, as String)
leader_of = {i: String(f"leader_of_team_{i}") for i in range(3)}

# synergy_score[team_id] = synergy score for that team
synergy_score = {i: Int(f"synergy_score_team_{i}") for i in range(3)}

# total_synergy = sum of all team synergy scores
total_synergy = Int("total_synergy")

# ----------------------------------------------------------------------------
# Helper Functions
# ----------------------------------------------------------------------------

# Map project names to integers
project_to_int = {"Alpha": 0, "Beta": 1, "Gamma": 2}
int_to_project = {0: "Alpha", 1: "Beta", 2: "Gamma"}

# ----------------------------------------------------------------------------
# Constraints
# ----------------------------------------------------------------------------

# 1. Each person assigned to exactly one team (0, 1, or 2)
for name in team_of:
    solver.add(team_of[name] >= 0, team_of[name] < 3)

# 2. Each team has exactly 4 members
for team_id in range(3):
    solver.add(Sum([If(team_of[name] == team_id, 1, 0) for name in team_of]) == 4)

# 3. Each team assigned to exactly one project
for team_id in range(3):
    solver.add(project_of[team_id] >= 0, project_of[team_id] < 3)

# 4. Each project assigned to exactly one team (no duplicates)
solver.add(Distinct(list(project_of.values())))

# 5. Leaders are Senior personnel
for team_id in range(3):
    # Leader must be one of the seniors
    solver.add(Or([leader_of[team_id] == name for name in seniors]))

# 6. Leaders must be on their team
for team_id in range(3):
    for name in seniors:
        # If leader_of[team_id] == name, then team_of[name] == team_id
        solver.add(Implies(leader_of[team_id] == name, team_of[name] == team_id))

# 7. Leaders must have mutually exclusive primary skills
# For each pair of teams, their leaders must have different primary skills
for i in range(3):
    for j in range(i + 1, 3):
        # Leaders must be different people
        solver.add(leader_of[i] != leader_of[j])
        # Their primary skills must be different
        for name1 in seniors:
            for name2 in seniors:
                if senior_primary_skills[name1] != senior_primary_skills[name2]:
                    solver.add(Implies(And(leader_of[i] == name1, leader_of[j] == name2), True))
                else:
                    solver.add(Not(And(leader_of[i] == name1, leader_of[j] == name2)))

# 8. Incompatibilities: Alex-Ben, Chloe-Grace, David-Harry cannot be on the same team
for (p1, p2) in incompatibilities:
    solver.add(team_of[p1] != team_of[p2])

# 9. Project requirements: Teams must satisfy the skill requirements of their assigned project
for team_id in range(3):
    project_id = project_of[team_id]
    project = int_to_project[project_id]
    required_skills = project_requirements[project]
    
    # Get all members of this team
    team_members = [name for name in team_of if team_of[name] == team_id]
    
    # For each required skill, at least one team member must have it
    for skill in required_skills:
        solver.add(Sum([If(skill in skills, 1, 0) for _, _, skills in personnel if name in team_members]) >= 1)

# 10. Synergy score calculation for each team
# For each team, count how many synergy pairs are present among its members
for team_id in range(3):
    team_members = [name for name in team_of if team_of[name] == team_id]
    
    # For each synergy pair, check if at least one member has skill1 and at least one has skill2
    synergy_terms = []
    for skill1, skill2 in synergy_pairs:
        # Check if team has at least one member with skill1 and at least one with skill2
        has_skill1 = Sum([If(skill1 in skills, 1, 0) for name, _, skills in personnel if name in team_members])
        has_skill2 = Sum([If(skill2 in skills, 1, 0) for name, _, skills in personnel if name in team_members])
        synergy_terms.append(And(has_skill1 >= 1, has_skill2 >= 1))
    
    # Synergy score is the number of synergy pairs present
    solver.add(synergy_score[team_id] == Sum([If(t, 1, 0) for t in synergy_terms]))

# 11. Total synergy is the sum of all team synergy scores
solver.add(total_synergy == Sum([synergy_score[i] for i in range(3)]))

# ----------------------------------------------------------------------------
# Objective: Maximize total_synergy
# ----------------------------------------------------------------------------

# Use Optimize to maximize total_synergy
opt = Optimize()

# Copy all constraints from solver to opt
for c in solver.assertions():
    opt.add(c)

# Maximize total_synergy
opt.maximize(total_synergy)

# ----------------------------------------------------------------------------
# Check and print result
# ----------------------------------------------------------------------------

result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    print("Optimal total synergy:", model.evaluate(total_synergy))
    
    # Extract team assignments
    teams = []
    for team_id in range(3):
        project_id = model.evaluate(project_of[team_id]).as_long()
        project = int_to_project[project_id]
        leader_name = model.evaluate(leader_of[team_id]).as_string()
        
        # Get team members
        members = []
        for name in team_of:
            if model.evaluate(team_of[name]) == team_id:
                members.append(name)
        members.sort()
        
        # Get synergy score
        synergy_val = model.evaluate(synergy_score[team_id]).as_long()
        
        teams.append({
            "team_id": team_id + 1,
            "project": project,
            "leader": leader_name,
            "members": members,
            "synergy_score": synergy_val
        })
    
    # Print teams
    for team in teams:
        print(f"Team {team['team_id']}: Project {team['project']}, Leader {team['leader']}, Members {team['members']}, Synergy {team['synergy_score']}")
    
    print(f"Total synergy: {model.evaluate(total_synergy)}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")