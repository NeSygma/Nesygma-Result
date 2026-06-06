from z3 import *

# Meetings: 1, 2, 3, 4, 5
meetings = [1, 2, 3, 4, 5]
days = [1, 2, 3]
slots = [1, 2, 3]
rooms = [1, 2] # 1: r1, 2: r2

# Required attendees
required = {
    1: [1, 2, 3],
    2: [1, 5],
    3: [2, 3],
    4: [1, 4],
    5: [1, 2, 3]
}

# Preferences
preferences = {
    1: (1, 1),
    2: (1, 2),
    4: (3, 3)
}

opt = Optimize()

# Variables
m_day = {m: Int(f'm_day_{m}') for m in meetings}
m_slot = {m: Int(f'm_slot_{m}') for m in meetings}
m_room = {m: Int(f'm_room_{m}') for m in meetings}

# Domain constraints
for m in meetings:
    opt.add(m_day[m] >= 1, m_day[m] <= 3)
    opt.add(m_slot[m] >= 1, m_slot[m] <= 3)
    opt.add(m_room[m] >= 1, m_room[m] <= 2)

# Constraint 2: No person can attend two meetings at the same time slot
# For each person, find all meetings they are required for
people = [1, 2, 3, 4, 5]
for p in people:
    p_meetings = [m for m in meetings if p in required[m]]
    for i in range(len(p_meetings)):
        for j in range(i + 1, len(p_meetings)):
            m1, m2 = p_meetings[i], p_meetings[j]
            opt.add(Not(And(m_day[m1] == m_day[m2], m_slot[m1] == m_slot[m2])))

# Constraint 3: Only one meeting per room per time slot
for i in range(len(meetings)):
    for j in range(i + 1, len(meetings)):
        m1, m2 = meetings[i], meetings[j]
        opt.add(Not(And(m_day[m1] == m_day[m2], m_slot[m1] == m_slot[m2], m_room[m1] == m_room[m2])))

# Objective: Minimize preference violations
violations = []
for m, (pref_day, pref_slot) in preferences.items():
    violations.append(If(And(m_day[m] == pref_day, m_slot[m] == pref_slot), 0, 1))

total_violations = Sum(violations)
opt.minimize(total_violations)

result = opt.check()
if result == sat:
    model = opt.model()
    print("STATUS: sat")
    print(f"preference_violations: {model.evaluate(total_violations)}")
    for m in meetings:
        print(f"m{m}: day={model[m_day[m]]}, slot={model[m_slot[m]]}, room=r{model[m_room[m]]}")
else:
    print("STATUS: unsat")