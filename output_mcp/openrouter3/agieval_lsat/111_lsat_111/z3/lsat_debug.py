from z3 import *

# Articles and their topics
finance = ['G', 'H', 'J']
nutrition = ['Q', 'R', 'S']
wildlife = ['Y']

# Create position variables for each article
positions = {article: Int(f'pos_{article}') for article in finance + nutrition + wildlife}

solver = Solver()

# Domain constraints: positions are between 1 and 7
for article in positions:
    solver.add(positions[article] >= 1)
    solver.add(positions[article] <= 7)

# All articles must be in distinct positions
solver.add(Distinct(list(positions.values())))

# Constraint 1: Consecutive articles cannot cover the same topic
# For each pair of articles with same topic, ensure they're not adjacent
for topic in [finance, nutrition]:
    for i in range(len(topic)):
        for j in range(i+1, len(topic)):
            solver.add(Or(
                positions[topic[i]] != positions[topic[j]] - 1,
                positions[topic[i]] != positions[topic[j]] + 1
            ))

# Constraint 2: S can be earlier than Q only if Q is third
solver.add(Or(positions['S'] >= positions['Q'], positions['Q'] == 3))

# Constraint 3: S must be earlier than Y
solver.add(positions['S'] < positions['Y'])

# Constraint 4: J < G < R
solver.add(positions['J'] < positions['G'])
solver.add(positions['G'] < positions['R'])

# Additional constraint from question: G is fourth
solver.add(positions['G'] == 4)

# Test each option and print the model
for letter, constr in [
    ('A', positions['H'] == 5),
    ('B', positions['J'] == 1),
    ('C', positions['Q'] == 2),
    ('D', positions['S'] == 5),
    ('E', positions['Y'] == 6)
]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        m = solver.model()
        print(f"Option {letter}: SAT")
        # Print the positions
        for article in sorted(positions.keys()):
            print(f"  {article}: {m[positions[article]]}")
    else:
        print(f"Option {letter}: UNSAT")
    solver.pop()