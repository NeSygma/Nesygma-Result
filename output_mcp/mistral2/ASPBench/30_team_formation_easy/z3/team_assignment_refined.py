from z3 import *

# People and their skills
people = {
    "Alice": ["Programming", "Design"],
    "Bob": ["Programming", "Testing"],
    "Carol": ["Design", "Management"],
    "Dave": ["Testing", "Management"],
    "Eve": ["Programming", "Documentation"],
    "Frank": ["Design", "Documentation"],
    "Grace": ["Testing", "Documentation"],
    "Henry": ["Management", "Documentation"]
}

required_skills = ["Programming", "Design", "Testing", "Management"]

# Initialize optimizer (not Solver) for minimization
opt = Optimize()

# Assign each person to a team (0 or 1)
team_assignments = [Int(f"team_{i}") for i in range(8)]
for i in range(8):
    opt.add(team_assignments[i] >= 0, team_assignments[i] <= 1)

# Each team must have exactly 4 people
opt.add(PbEq([(team_assignments[i] == 0, 1) for i in range(8)], 4))
opt.add(PbEq([(team_assignments[i] == 1, 1) for i in range(8)], 4))

# List of people in order
person_list = list(people.keys())

# Function to check if a team has a required skill
def team_has_skill(team_id, skill):
    return Or([And(team_assignments[i] == team_id, skill in people[person_list[i]]) for i in range(8)])

# Each team must have at least one person with each required skill
for team_id in [0, 1]:
    for skill in required_skills:
        opt.add(team_has_skill(team_id, skill))

# Objective: Minimize skill overlap within teams
# For each team, count the number of people with each skill and minimize overlaps
# We will minimize the maximum number of people with the same skill in a team
max_skill_count = Int("max_skill_count")
opt.add(max_skill_count >= 0)

# For each team, for each skill, count the number of people with that skill
skill_counts = {}
for skill in required_skills:
    skill_counts[skill] = [Int(f"count_{skill}_team_{team_id}") for team_id in [0, 1]]
    for team_id in [0, 1]:
        # Count the number of people in the team with this skill
        opt.add(skill_counts[skill][team_id] == Sum([If(And(team_assignments[i] == team_id, skill in people[person_list[i]]), 1, 0) for i in range(8)]))

# Constrain max_skill_count to be the maximum skill count in either team
for team_id in [0, 1]:
    for skill in required_skills:
        opt.add(max_skill_count >= skill_counts[skill][team_id])

# Set the objective to minimize max_skill_count
opt.minimize(max_skill_count)

# Check if a solution exists
BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")

    # Extract team assignments
    team0 = [person_list[i] for i in range(8) if model[team_assignments[i]] == 0]
    team1 = [person_list[i] for i in range(8) if model[team_assignments[i]] == 1]

    print("Team 0:", team0)
    print("Team 1:", team1)

    # Print skill coverage for each team
    for team_id, team in enumerate([team0, team1]):
        print(f"Team {team_id} skills:")
        for skill in required_skills:
            has_skill = any(skill in people[person] for person in team)
            print(f"  {skill}: {'Yes' if has_skill else 'No'}")

    # Print max skill count
    print("Max skill count in any team:", model[max_skill_count])

elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")