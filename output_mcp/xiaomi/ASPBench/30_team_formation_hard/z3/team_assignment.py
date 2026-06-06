from z3 import *

# Define personnel
personnel = ['Alex', 'Ben', 'Chloe', 'David', 'Grace', 'Harry', 'Eva', 'Frank', 'Ivy', 'Jack', 'Kate', 'Leo']
seniors = ['Alex', 'Ben', 'Chloe', 'David', 'Grace', 'Harry']
juniors = ['Eva', 'Frank', 'Ivy', 'Jack', 'Kate', 'Leo']

# Skills for each person
skills = {
    'Alex': ['Programming', 'Security'],
    'Ben': ['Programming', 'DevOps'],
    'Chloe': ['Design', 'Management'],
    'David': ['Testing', 'DataScience'],
    'Grace': ['Management', 'DataScience'],
    'Harry': ['DevOps', 'Security'],
    'Eva': ['Programming', 'Cloud'],
    'Frank': ['Design', 'Testing'],
    'Ivy': ['Design', 'Cloud'],
    'Jack': ['Testing', 'Programming'],
    'Kate': ['Management', 'DevOps'],
    'Leo': ['DataScience', 'Security']
}

# Primary skills
primary_skills = ['Programming', 'Design', 'Testing', 'Management', 'DataScience', 'DevOps']

# Projects
projects = ['Alpha', 'Beta', 'Gamma']
project_requirements = {
    'Alpha': ['Security'],
    'Beta': ['Cloud'],
    'Gamma': []
}

# Incompatibilities
incompatible_pairs = [('Alex', 'Ben'), ('Chloe', 'Grace'), ('David', 'Harry')]

# Synergy pairs
synergy_pairs = [('Programming', 'DevOps'), ('Design', 'DataScience'), ('Management', 'Testing'), ('Security', 'Cloud')]

# Create Z3 variables
# team_assignment[p][t] = True if person p is assigned to team t
team_assignment = {}
for p in personnel:
    for t in range(3):
        team_assignment[(p, t)] = Bool(f'{p}_team_{t}')

# project_assignment[t][proj] = True if team t is assigned to project proj
project_assignment = {}
for t in range(3):
    for proj in projects:
        project_assignment[(t, proj)] = Bool(f'team_{t}_proj_{proj}')

# leader[p][t] = True if person p is the leader of team t
leader = {}
for p in personnel:
    for t in range(3):
        leader[(p, t)] = Bool(f'{p}_leader_{t}')

# Synergy variables
# synergy[t][pair] = True if team t has synergy pair
synergy = {}
for t in range(3):
    for i, pair in enumerate(synergy_pairs):
        synergy[(t, i)] = Bool(f'synergy_{t}_{i}')

# Create solver
solver = Optimize()

# Helper: ExactlyOne constraint
def exactly_one(bool_list):
    # At least one is true
    solver.add(Or(bool_list))
    # At most one is true (pairwise)
    for i in range(len(bool_list)):
        for j in range(i+1, len(bool_list)):
            solver.add(Not(And(bool_list[i], bool_list[j])))

# Constraint 1: Each person assigned to exactly one team
for p in personnel:
    exactly_one([team_assignment[(p, t)] for t in range(3)])

# Constraint 2: Each team has exactly 4 members
for t in range(3):
    solver.add(Sum([If(team_assignment[(p, t)], 1, 0) for p in personnel]) == 4)

# Constraint 3: Each team assigned to exactly one project
for t in range(3):
    exactly_one([project_assignment[(t, proj)] for proj in projects])

# Constraint 4: Each project assigned to exactly one team
for proj in projects:
    exactly_one([project_assignment[(t, proj)] for t in range(3)])

# Constraint 5: Each team has exactly one leader who must be Senior
for t in range(3):
    # Exactly one leader per team
    exactly_one([leader[(p, t)] for p in personnel])
    # Leader must be Senior and on the team
    for p in personnel:
        solver.add(Implies(leader[(p, t)], And(p in seniors, team_assignment[(p, t)])))

# Constraint 6: Leader skills must be mutually exclusive primary skills
# For each pair of teams, their leaders must not share any primary skill
for t1 in range(3):
    for t2 in range(t1+1, 3):
        for s in primary_skills:
            # Collect leaders of t1 who have skill s
            leaders_t1_with_s = [leader[(p, t1)] for p in personnel if s in skills[p]]
            # Collect leaders of t2 who have skill s
            leaders_t2_with_s = [leader[(p, t2)] for p in personnel if s in skills[p]]
            # Cannot both have a leader with skill s
            if leaders_t1_with_s and leaders_t2_with_s:
                solver.add(Not(And(Or(leaders_t1_with_s), Or(leaders_t2_with_s))))

# Constraint 7: Incompatibilities - incompatible pairs cannot be on same team
for p1, p2 in incompatible_pairs:
    for t in range(3):
        solver.add(Not(And(team_assignment[(p1, t)], team_assignment[(p2, t)])))

# Constraint 8: Project requirements
for t in range(3):
    for proj in projects:
        for req_skill in project_requirements[proj]:
            # If team t is assigned to project proj, then at least one member must have req_skill
            solver.add(Implies(project_assignment[(t, proj)], 
                              Or([And(team_assignment[(p, t)], req_skill in skills[p]) for p in personnel])))

# Synergy calculation
for t in range(3):
    for i, (s1, s2) in enumerate(synergy_pairs):
        # Team has synergy if at least one member has s1 and at least one member has s2
        has_s1 = Or([And(team_assignment[(p, t)], s1 in skills[p]) for p in personnel])
        has_s2 = Or([And(team_assignment[(p, t)], s2 in skills[p]) for p in personnel])
        solver.add(synergy[(t, i)] == And(has_s1, has_s2))

# Objective: maximize total synergy
total_synergy = Sum([If(synergy[(t, i)], 1, 0) for t in range(3) for i in range(len(synergy_pairs))])
solver.maximize(total_synergy)

# Check and print results
result = solver.check()
if result == sat:
    model = solver.model()
    print("STATUS: sat")
    
    # Extract team assignments
    teams = []
    for t in range(3):
        members = []
        for p in personnel:
            if is_true(model.evaluate(team_assignment[(p, t)])):
                members.append(p)
        members.sort()
        
        # Find leader
        team_leader = None
        for p in personnel:
            if is_true(model.evaluate(leader[(p, t)])):
                team_leader = p
                break
        
        # Find project
        team_project = None
        for proj in projects:
            if is_true(model.evaluate(project_assignment[(t, proj)])):
                team_project = proj
                break
        
        # Calculate synergy score
        team_synergy = 0
        for i in range(len(synergy_pairs)):
            if is_true(model.evaluate(synergy[(t, i)])):
                team_synergy += 1
        
        teams.append({
            'team_id': t+1,
            'project': team_project,
            'leader': team_leader,
            'members': members,
            'synergy_score': team_synergy
        })
    
    # Print results
    for team in teams:
        print(f"Team {team['team_id']}: Project={team['project']}, Leader={team['leader']}, Members={team['members']}, Synergy={team['synergy_score']}")
    
    total = sum(t['synergy_score'] for t in teams)
    print(f"Total Synergy: {total}")
    
    # Verify constraints
    print("\nVerification:")
    print(f"Total members across teams: {sum(len(t['members']) for t in teams)}")
    print(f"All personnel assigned: {sorted([p for team in teams for p in team['members']]) == sorted(personnel)}")
    
    # Check incompatibilities
    for p1, p2 in incompatible_pairs:
        for team in teams:
            if p1 in team['members'] and p2 in team['members']:
                print(f"WARNING: Incompatible pair {p1}-{p2} in same team!")
    
    # Check project requirements
    for team in teams:
        proj = team['project']
        req_skills = project_requirements[proj]
        team_skills = set()
        for p in team['members']:
            team_skills.update(skills[p])
        for req in req_skills:
            if req not in team_skills:
                print(f"WARNING: Team {team['team_id']} missing required skill {req} for project {proj}")
    
    # Check leader constraints
    for team in teams:
        leader_name = team['leader']
        if leader_name not in seniors:
            print(f"WARNING: Team {team['team_id']} leader {leader_name} is not Senior!")
        if leader_name not in team['members']:
            print(f"WARNING: Team {team['team_id']} leader {leader_name} not in team!")
    
    # Check leader skill exclusivity
    leader_skills = []
    for team in teams:
        leader_name = team['leader']
        leader_skills.append(set(skills[leader_name]))
    for i in range(len(leader_skills)):
        for j in range(i+1, len(leader_skills)):
            common = leader_skills[i].intersection(leader_skills[j])
            if common:
                print(f"WARNING: Leaders share skill(s): {common}")
    
elif result == unsat:
    print("STATUS: unsat")
    print("No solution found")
else:
    print("STATUS: unknown")