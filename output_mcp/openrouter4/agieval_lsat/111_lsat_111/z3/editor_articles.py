from z3 import *

solver = Solver()

# Articles
G, H, J = Ints('G H J')
Q, R, S = Ints('Q R S')
Y = Int('Y')

articles = [G, H, J, Q, R, S, Y]

# Domain constraints: each position is from 1 to 7
for a in articles:
    solver.add(a >= 1, a <= 7)

# All distinct positions
solver.add(Distinct(articles))

# Topic constants: finance = 0, nutrition = 1, wildlife = 2
topic = {
    G: 0, H: 0, J: 0,  # finance
    Q: 1, R: 1, S: 1,  # nutrition
    Y: 2               # wildlife
}

# Consecutive articles cannot cover the same topic
# For each pair of positions i and i+1, we need that for any two articles a,b:
# If a is at position i and b is at position i+1, then topic[a] != topic[b]
# We can encode this by saying: for each article a, for each article b != a,
# if a is at position p and b is at position p+1, then topics differ.
# Better: use an array of position->topic mapping and enforce constraints.

# Approach: define an array pos_to_article where pos_to_article[p] is the article at position p.
# Then topic_of_pos[p] = topic[pos_to_article[p]].
# Constraint: For p in 1..6, topic_of_pos[p] != topic_of_pos[p+1].

# We can use Z3 Array for pos_to_article.
pos_to_article = Array('pos_to_article', IntSort(), IntSort())
# Map each position to an article value (we'll encode articles as integers 1..7)
article_vals = list(range(7))  # 0..6 representing G=0, H=1, J=2, Q=3, R=4, S=5, Y=6
# Actually let's use a function or just use the Or-loop pattern.

# Alternative: Use an array art_at_pos where art_at_pos[p] is the article variable.
# Simpler: Use a function representation.

# Let's use the approach: for each position p (1..7), art_at_pos[p] is an integer variable from 0..6 (article index).
art_at_pos = [Int(f'art_at_pos_{p}') for p in range(1, 8)]

for p in range(1, 8):
    solver.add(art_at_pos[p-1] >= 0, art_at_pos[p-1] <= 6)

# All distinct articles at positions
solver.add(Distinct(art_at_pos))

# Link article position variables to art_at_pos
# For each article a (0..6), we want that art_at_pos[position_of_a - 1] == a
# Actually we need consistency: the integer variable for each article represents its position.
# So we need: For each article index a (0..6), the position of that article (pos_var[a]) must
# be consistent with art_at_pos.
# Let's create a list of position variables: pos_vars = [G, H, J, Q, R, S, Y]
pos_vars = [G, H, J, Q, R, S, Y]
article_indices = list(range(7))  # 0=G, 1=H, 2=J, 3=Q, 4=R, 5=S, 6=Y

# For each article index i and position p: (pos_vars[i] == p) implies (art_at_pos[p-1] == i)
for i in range(7):
    for p in range(1, 8):
        solver.add(Implies(pos_vars[i] == p, art_at_pos[p-1] == i))

# Now topic of position p is topic[article_index]
# topic mapping: article index -> topic
topic_of_article = [0, 0, 0, 1, 1, 1, 2]  # G=0,H=0,J=0,Q=1,R=1,S=1,Y=2

# Consecutive: topic_of_article[art_at_pos[p-1]] != topic_of_article[art_at_pos[p]]
for p in range(1, 7):
    idx_p = art_at_pos[p-1]
    idx_p1 = art_at_pos[p]
    # We need: topic[idx_p] != topic[idx_p1]
    # Use Or-loop to express this.
    # topic[idx] is a symbolic expression: we can use a function.
    # Actually we can define a Z3 function for topic.
    pass

# Let's take a different approach. Instead of art_at_pos, let's use the original position variables
# and enforce constraints using Or-loops for consecutive topic constraint.

# Actually simpler: For each pair of consecutive positions (p, p+1), we can assert:
# NOT( (any finance article at p AND any finance article at p+1) OR
#      (any nutrition article at p AND any nutrition article at p+1) OR
#      (any wildlife article at p AND any wildlife article at p+1) )
# This is complex.

# Alternative encoding: For each article a, for each article b (b != a), 
# if topic[a] == topic[b], then not (position_of_a == p and position_of_b == p+1) for any p.
# That is: For each pair a,b with same topic, a and b cannot be adjacent.
# But also: a and b could be same topic but if there's only 1 wildlife article Y, it can't be adjacent to itself.
# Let's do this.

# finance articles: G, H, J
finance = [G, H, J]
nutrition = [Q, R, S]
wildlife = [Y]

# For each pair in the same topic, they cannot be consecutive
def not_adjacent(a, b):
    # a and b cannot be at positions p and p+1 (in either order)
    conds = []
    for p in range(1, 7):  # p from 1 to 6
        conds.append(Not(And(a == p, b == p+1)))
        conds.append(Not(And(b == p, a == p+1)))
    return And(conds)

# Finance pairs
for i in range(len(finance)):
    for j in range(i+1, len(finance)):
        solver.add(not_adjacent(finance[i], finance[j]))

# Nutrition pairs
for i in range(len(nutrition)):
    for j in range(i+1, len(nutrition)):
        solver.add(not_adjacent(nutrition[i], nutrition[j]))

# Wildlife: only Y, no pair.

# Also, articles from same topic cannot be adjacent. But what about adjacent but different topics? That's fine.

# But also, we need to ensure that ANY two articles with the same topic cannot be adjacent.
# The above covers all pairs within each topic.

# Condition: S can be earlier than Q only if Q is third.
# (S < Q) implies (Q == 3)
solver.add(Implies(S < Q, Q == 3))

# S must be earlier than Y
solver.add(S < Y)

# J must be earlier than G, and G must be earlier than R
solver.add(J < G)
solver.add(G < R)

# G is fourth
solver.add(G == 4)

# Now let's evaluate each option.

# Option A: H is fifth
opt_a = (H == 5)
# Option B: J is first
opt_b = (J == 1)
# Option C: Q is second
opt_c = (Q == 2)
# Option D: S is fifth
opt_d = (S == 5)
# Option E: Y is sixth
opt_e = (Y == 6)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")