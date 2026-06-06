from z3 import *

# Define inhabitants
names = [
    "Alice", "Bob", "Charlie", "Diana", "Ethan", "Fiona", "George", "Hannah",
    "Ian", "Julia", "Kevin", "Lily", "Mason", "Nina", "Oliver", "Paula",
    "Quentin", "Rachel", "Sam", "Tina", "Ursula", "Victor", "Wendy", "Xavier"
]

# Map names to indices
name_to_idx = {name: i for i, name in enumerate(names)}

# Variables: True for Knight, False for Knave
is_knight = [Bool(name) for name in names]

solver = Solver()

# Helper functions
def is_k(name):
    return is_knight[name_to_idx[name]]

def count_knights(group_names):
    return Sum([If(is_k(name), 1, 0) for name in group_names])

# Group definitions
group_a = ["Alice", "Bob", "Charlie", "Diana", "Ethan", "Fiona", "George", "Hannah"]
group_b = ["Ian", "Julia", "Kevin", "Lily", "Mason", "Nina", "Oliver", "Paula"]
group_c = ["Quentin", "Rachel", "Sam", "Tina", "Ursula", "Victor", "Wendy", "Xavier"]

# Statements
# Group A
# Alice: "Hannah is a knave, and (Bob is a knave or Charlie is a knight), and exactly four of us in Group A are knights."
solver.add(is_k("Alice") == And(
    Not(is_k("Hannah")),
    Or(Not(is_k("Bob")), is_k("Charlie")),
    count_knights(group_a) == 4
))

# Bob: "Diana is the same type as me."
solver.add(is_k("Bob") == (is_k("Diana") == is_k("Bob")))

# Charlie: "Exactly twelve of us are knights."
solver.add(is_k("Charlie") == (Sum([If(is_k(n), 1, 0) for n in names]) == 12))

# Diana: "Ethan and Fiona are of different types, and Hannah is a knave."
solver.add(is_k("Diana") == And(
    is_k("Ethan") != is_k("Fiona"),
    Not(is_k("Hannah"))
))

# Ethan: "George is a knight if and only if Alice is a knight."
solver.add(is_k("Ethan") == (is_k("George") == is_k("Alice")))

# Fiona: "Bob and Charlie are of different types, and I am a knight."
solver.add(is_k("Fiona") == And(
    is_k("Bob") != is_k("Charlie"),
    is_k("Fiona")
))

# George: "Alice and Hannah are of the same type."
solver.add(is_k("George") == (is_k("Alice") == is_k("Hannah")))

# Hannah: "Exactly one of Bob, Charlie, and Diana is a knight."
solver.add(is_k("Hannah") == (Sum([If(is_k(n), 1, 0) for n in ["Bob", "Charlie", "Diana"]]) == 1))

# Group B
# Ian: "Alice and Paula are of the same type, and Julia is a knave."
solver.add(is_k("Ian") == And(
    is_k("Alice") == is_k("Paula"),
    Not(is_k("Julia"))
))

# Julia: "Kevin is a knight and Nina is a knight."
solver.add(is_k("Julia") == And(is_k("Kevin"), is_k("Nina")))

# Kevin: "Either Oliver is a knight or Lily is a knave."
solver.add(is_k("Kevin") == Or(is_k("Oliver"), Not(is_k("Lily"))))

# Lily: "Exactly four of us in Group B are knights, and Oliver is a knave."
solver.add(is_k("Lily") == And(
    count_knights(group_b) == 4,
    Not(is_k("Oliver"))
))

# Mason: "Bob and Ethan are of the same type, and Julia is a knave."
solver.add(is_k("Mason") == And(
    is_k("Bob") == is_k("Ethan"),
    Not(is_k("Julia"))
))

# Nina: "Ian and Paula are of different types."
solver.add(is_k("Nina") == (is_k("Ian") != is_k("Paula")))

# Oliver: "Exactly two of George, Hannah, Ian, and Julia are knights."
solver.add(is_k("Oliver") == (Sum([If(is_k(n), 1, 0) for n in ["George", "Hannah", "Ian", "Julia"]]) == 2))

# Paula: "Rachel is a knight if and only if Quentin is a knave."
solver.add(is_k("Paula") == (is_k("Rachel") == Not(is_k("Quentin"))))

# Group C
# Quentin: "At least five of us in Group C are knights."
solver.add(is_k("Quentin") == (count_knights(group_c) >= 5))

# Rachel: "Charlie is a knight, Lily is a knight, and Victor is a knave."
solver.add(is_k("Rachel") == And(is_k("Charlie"), is_k("Lily"), Not(is_k("Victor"))))

# Sam: "Tina is a knave, Oliver is a knave, and Ursula is a knave."
solver.add(is_k("Sam") == And(Not(is_k("Tina")), Not(is_k("Oliver")), Not(is_k("Ursula"))))

# Tina: "Rachel is a knave or Mason is a knave."
solver.add(is_k("Tina") == Or(Not(is_k("Rachel")), Not(is_k("Mason"))))

# Ursula: "Ian and Julia are both knights."
solver.add(is_k("Ursula") == And(is_k("Ian"), is_k("Julia")))

# Victor: "Exactly two of Alice, Bob, Charlie, and Diana are knaves."
solver.add(is_k("Victor") == (Sum([If(Not(is_k(n)), 1, 0) for n in ["Alice", "Bob", "Charlie", "Diana"]]) == 2))

# Wendy: "Victor is a knave, Ursula is a knave, and Xavier is a knight."
solver.add(is_k("Wendy") == And(Not(is_k("Victor")), Not(is_k("Ursula")), is_k("Xavier")))

# Xavier: "Exactly four of us in Group C are knights, and Sam is a knight."
solver.add(is_k("Xavier") == And(
    count_knights(group_c) == 4,
    is_k("Sam")
))

# Solve
result = solver.check()
if result == sat:
    print("STATUS: sat")
    m = solver.model()
    for name in names:
        print(f"{name}: {'knight' if m.eval(is_k(name)) else 'knave'}")
else:
    print("STATUS: unsat")