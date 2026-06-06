from z3 import *

# People and required skills (excluding Documentation)
people = ['Alice','Bob','Carol','Dave','Eve','Frank','Grace','Henry']
person_skills = {
    'Alice': {'Programming','Design'},
    'Bob': {'Programming','Testing'},
    'Carol': {'Design','Management'},
    'Dave': {'Testing','Management'},
    'Eve': {'Programming'},
    'Frank': {'Design'},
    'Grace': {'Testing'},
    'Henry': {'Management'}
}
required_skills = ['Programming','Design','Testing','Management']

# Map each skill to people who have it
skill_to_people = {s: [p for p in people if s in person_skills[p]] for s in required_skills}

# Create Optimize
opt = Optimize()

# Boolean var: person in team0?
t0 = {p: Bool(f'{p}_team0') for p in people}

# Exactly 4 people in team0
opt.add(Sum([If(t0[p], 1, 0) for p in people]) == 4)

# Each required skill must be covered in each team
for s in required_skills:
    # team0 must have at least one person with skill s
    opt.add(Or([t0[p] for p in skill_to_people[s]]))
    # team1 (i.e., not in team0) must also have at least one person with skill s
    opt.add(Or([Not(t0[p]) for p in skill_to_people[s]]))

# Minimize skill overlap within teams
# First, find all unordered pairs that share at least one required skill
overlap_terms = []
for i in range(len(people)):
    for j in range(i+1, len(people)):
        pi, pj = people[i], people[j]
        if person_skills[pi].intersection(person_skills[pj]):
            # they share a skill, count 1 if both in same team
            both_team0 = And(t0[pi], t0[pj])
            both_team1 = And(Not(t0[pi]), Not(t0[pj]))
            overlap_terms.append(If(both_team0, 1, If(both_team1, 1, 0)))
overlap = Sum(overlap_terms)
opt.minimize(overlap)

# Solve
result = opt.check()
if result == sat:
    m = opt.model()
    print("STATUS: sat")
    team0 = [p for p in people if m[t0[p]] == True]
    team1 = [p for p in people if m[t0[p]] != True]
    print("team_0 =", team0)
    print("team_1 =", team1)
elif result == unsat:
    print("STATUS: unsat")
    # In benchmark mode, unsat is a refinement trigger
    print("RAW_RESULT: unsat (semantic/modeling error; refine required)")
else:
    print("STATUS: unknown")