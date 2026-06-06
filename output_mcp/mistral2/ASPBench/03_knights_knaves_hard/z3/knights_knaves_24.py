from z3 import *

# Declare boolean variables for each person's type
# Group A
A = [Bool(f"{name}_is_knight") for name in ["Alice", "Bob", "Charlie", "Diana", "Ethan", "Fiona", "George", "Hannah"]]

# Group B
B = [Bool(f"{name}_is_knight") for name in ["Ian", "Julia", "Kevin", "Lily", "Mason", "Nina", "Oliver", "Paula"]]

# Group C
C = [Bool(f"{name}_is_knight") for name in ["Quentin", "Rachel", "Sam", "Tina", "Ursula", "Victor", "Wendy", "Xavier"]]

# Combine all groups for convenience
all_people = A + B + C

solver = Solver()

# Helper function to count the number of knights in a group
def count_knights(group):
    return Sum([If(p, 1, 0) for p in group])

# Group A statements
# Alice: "Hannah is a knave, and (Bob is a knave or Charlie is a knight), and exactly four of us in Group A are knights."
solver.add(Implies(A[0], And(
    Not(A[7]),  # Hannah is a knave
    Or(Not(A[1]), A[2]),  # Bob is a knave or Charlie is a knight
    count_knights(A) == 4  # Exactly four knights in Group A
)))
solver.add(Implies(Not(A[0]), Not(And(
    Not(A[7]),
    Or(Not(A[1]), A[2]),
    count_knights(A) == 4
))))

# Bob: "Diana is the same type as me."
solver.add(Implies(A[1], A[3] == A[1]))
solver.add(Implies(Not(A[1]), A[3] != A[1]))

# Charlie: "Exactly twelve of us are knights."
# Note: This refers to all 24 inhabitants
solver.add(Implies(A[2], count_knights(all_people) == 12))
solver.add(Implies(Not(A[2]), count_knights(all_people) != 12))

# Diana: "Ethan and Fiona are of different types, and Hannah is a knave."
solver.add(Implies(A[3], And(
    A[4] != A[5],  # Ethan and Fiona are of different types
    Not(A[7])  # Hannah is a knave
)))
solver.add(Implies(Not(A[3]), Not(And(
    A[4] != A[5],
    Not(A[7])
))))

# Ethan: "George is a knight if and only if Alice is a knight."
solver.add(Implies(A[4], A[6] == A[0]))
solver.add(Implies(Not(A[4]), A[6] != A[0]))

# Fiona: "Bob and Charlie are of different types, and I am a knight."
solver.add(Implies(A[5], And(
    A[1] != A[2],  # Bob and Charlie are of different types
    A[5]  # I am a knight
)))
solver.add(Implies(Not(A[5]), Not(And(
    A[1] != A[2],
    A[5]
))))

# George: "Alice and Hannah are of the same type."
solver.add(Implies(A[6], A[0] == A[7]))
solver.add(Implies(Not(A[6]), A[0] != A[7]))

# Hannah: "Exactly one of Bob, Charlie, and Diana is a knight."
solver.add(Implies(A[7], count_knights([A[1], A[2], A[3]]) == 1))
solver.add(Implies(Not(A[7]), count_knights([A[1], A[2], A[3]]) != 1))

# Group B statements
# Ian: "Alice and Paula are of the same type, and Julia is a knave."
solver.add(Implies(B[0], And(
    A[0] == B[7],  # Alice and Paula are of the same type
    Not(B[1])  # Julia is a knave
)))
solver.add(Implies(Not(B[0]), Not(And(
    A[0] == B[7],
    Not(B[1])
))))

# Julia: "Kevin is a knight and Nina is a knight."
solver.add(Implies(B[1], And(B[2], B[5])))
solver.add(Implies(Not(B[1]), Not(And(B[2], B[5]))))

# Kevin: "Either Oliver is a knight or Lily is a knave."
solver.add(Implies(B[2], Or(B[6], Not(B[3]))))
solver.add(Implies(Not(B[2]), Not(Or(B[6], Not(B[3])))))

# Lily: "Exactly four of us in Group B are knights, and Oliver is a knave."
solver.add(Implies(B[3], And(
    count_knights(B) == 4,
    Not(B[6])  # Oliver is a knave
)))
solver.add(Implies(Not(B[3]), Not(And(
    count_knights(B) == 4,
    Not(B[6])
))))

# Mason: "Bob and Ethan are of the same type, and Julia is a knave."
solver.add(Implies(B[4], And(
    A[1] == A[4],  # Bob and Ethan are of the same type
    Not(B[1])  # Julia is a knave
)))
solver.add(Implies(Not(B[4]), Not(And(
    A[1] == A[4],
    Not(B[1])
))))

# Nina: "Ian and Paula are of different types."
solver.add(Implies(B[5], B[0] != B[7]))
solver.add(Implies(Not(B[5]), B[0] == B[7]))

# Oliver: "Exactly two of George, Hannah, Ian, and Julia are knights."
solver.add(Implies(B[6], count_knights([A[6], A[7], B[0], B[1]]) == 2))
solver.add(Implies(Not(B[6]), count_knights([A[6], A[7], B[0], B[1]]) != 2))

# Paula: "Rachel is a knight if and only if Quentin is a knave."
solver.add(Implies(B[7], C[1] == Not(C[0])))
solver.add(Implies(Not(B[7]), C[1] != Not(C[0])))

# Group C statements
# Quentin: "At least five of us in Group C are knights."
solver.add(Implies(C[0], count_knights(C) >= 5))
solver.add(Implies(Not(C[0]), count_knights(C) < 5))

# Rachel: "Charlie is a knight, Lily is a knight, and Victor is a knave."
solver.add(Implies(C[1], And(A[2], B[3], Not(C[5]))))
solver.add(Implies(Not(C[1]), Not(And(A[2], B[3], Not(C[5])))))

# Sam: "Tina is a knave, Oliver is a knave, and Ursula is a knave."
solver.add(Implies(C[2], And(
    Not(C[3]),  # Tina is a knave
    Not(B[6]),  # Oliver is a knave
    Not(C[4])   # Ursula is a knave
)))
solver.add(Implies(Not(C[2]), Not(And(
    Not(C[3]),
    Not(B[6]),
    Not(C[4])
))))

# Tina: "Rachel is a knave or Mason is a knave."
solver.add(Implies(C[3], Or(Not(C[1]), Not(B[4]))))
solver.add(Implies(Not(C[3]), Not(Or(Not(C[1]), Not(B[4])))))

# Ursula: "Ian and Julia are both knights."
solver.add(Implies(C[4], And(B[0], B[1])))
solver.add(Implies(Not(C[4]), Not(And(B[0], B[1]))))

# Victor: "Exactly two of Alice, Bob, Charlie, and Diana are knaves."
solver.add(Implies(C[5], count_knights([A[0], A[1], A[2], A[3]]) == 2))
solver.add(Implies(Not(C[5]), count_knights([A[0], A[1], A[2], A[3]]) != 2))

# Wendy: "Victor is a knave, Ursula is a knave, and Xavier is a knight."
solver.add(Implies(C[6], And(
    Not(C[5]),  # Victor is a knave
    Not(C[4]),  # Ursula is a knave
    C[7]        # Xavier is a knight
)))
solver.add(Implies(Not(C[6]), Not(And(
    Not(C[5]),
    Not(C[4]),
    C[7]
))))

# Xavier: "Exactly four of us in Group C are knights, and Sam is a knight."
solver.add(Implies(C[7], And(
    count_knights(C) == 4,
    C[2]  # Sam is a knight
)))
solver.add(Implies(Not(C[7]), Not(And(
    count_knights(C) == 4,
    C[2]
))))

# Check for a solution
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    # Print the assignment for each person
    for i, name in enumerate(["Alice", "Bob", "Charlie", "Diana", "Ethan", "Fiona", "George", "Hannah",
                              "Ian", "Julia", "Kevin", "Lily", "Mason", "Nina", "Oliver", "Paula",
                              "Quentin", "Rachel", "Sam", "Tina", "Ursula", "Victor", "Wendy", "Xavier"]):
        print(f"{name} = {'knight' if model[all_people[i]] else 'knave'}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")