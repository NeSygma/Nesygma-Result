from z3 import *

# Declare boolean variables for each person (True = knight, False = knave)
# Group A
Alice, Bob, Charlie, Diana, Ethan, Fiona, George, Hannah = Bools('Alice Bob Charlie Diana Ethan Fiona George Hannah')

# Group B
Ian, Julia, Kevin, Lily, Mason, Nina, Oliver, Paula = Bools('Ian Julia Kevin Lily Mason Nina Oliver Paula')

# Group C
Quentin, Rachel, Sam, Tina, Ursula, Victor, Wendy, Xavier = Bools('Quentin Rachel Sam Tina Ursula Victor Wendy Xavier')

solver = Solver()

# Helper function to count knights in a group
def count_knights(group):
    return Sum(group)

# Group A statements
# Alice: "Hannah is a knave, and (Bob is a knave or Charlie is a knight), and exactly four of us in Group A are knights."
alice_statement = And(
    Not(Hannah),  # Hannah is a knave
    Or(Not(Bob), Charlie),  # Bob is a knave or Charlie is a knight
    count_knights([Alice, Bob, Charlie, Diana, Ethan, Fiona, George, Hannah]) == 4  # Exactly four knights in Group A
)
solver.add(If(Alice, alice_statement, Not(alice_statement)))

# Bob: "Diana is the same type as me."
bob_statement = (Diana == Bob)
solver.add(If(Bob, bob_statement, Not(bob_statement)))

# Charlie: "Exactly twelve of us are knights."
# "Us" here refers to all 24 inhabitants
charlie_statement = (count_knights([Alice, Bob, Charlie, Diana, Ethan, Fiona, George, Hannah, 
                                   Ian, Julia, Kevin, Lily, Mason, Nina, Oliver, Paula,
                                   Quentin, Rachel, Sam, Tina, Ursula, Victor, Wendy, Xavier]) == 12)
solver.add(If(Charlie, charlie_statement, Not(charlie_statement)))

# Diana: "Ethan and Fiona are of different types, and Hannah is a knave."
diana_statement = And(
    Ethan != Fiona,  # Different types
    Not(Hannah)  # Hannah is a knave
)
solver.add(If(Diana, diana_statement, Not(diana_statement)))

# Ethan: "George is a knight if and only if Alice is a knight."
ethan_statement = (George == Alice)
solver.add(If(Ethan, ethan_statement, Not(ethan_statement)))

# Fiona: "Bob and Charlie are of different types, and I am a knight."
fiiona_statement = And(
    Bob != Charlie,  # Different types
    Fiona  # I am a knight
)
solver.add(If(Fiona, fiiona_statement, Not(fiiona_statement)))

# George: "Alice and Hannah are of the same type."
george_statement = (Alice == Hannah)
solver.add(If(George, george_statement, Not(george_statement)))

# Hannah: "Exactly one of Bob, Charlie, and Diana is a knight."
hannah_statement = (count_knights([Bob, Charlie, Diana]) == 1)
solver.add(If(Hannah, hannah_statement, Not(hannah_statement)))

# Group B statements
# Ian: "Alice and Paula are of the same type, and Julia is a knave."
ian_statement = And(
    Alice == Paula,
    Not(Julia)
)
solver.add(If(Ian, ian_statement, Not(ian_statement)))

# Julia: "Kevin is a knight and Nina is a knight."
julia_statement = And(Kevin, Nina)
solver.add(If(Julia, julia_statement, Not(julia_statement)))

# Kevin: "Either Oliver is a knight or Lily is a knave."
kevin_statement = Or(Oliver, Not(Lily))
solver.add(If(Kevin, kevin_statement, Not(kevin_statement)))

# Lily: "Exactly four of us in Group B are knights, and Oliver is a knave."
lily_statement = And(
    count_knights([Ian, Julia, Kevin, Lily, Mason, Nina, Oliver, Paula]) == 4,
    Not(Oliver)
)
solver.add(If(Lily, lily_statement, Not(lily_statement)))

# Mason: "Bob and Ethan are of the same type, and Julia is a knave."
mason_statement = And(
    Bob == Ethan,
    Not(Julia)
)
solver.add(If(Mason, mason_statement, Not(mason_statement)))

# Nina: "Ian and Paula are of different types."
nina_statement = (Ian != Paula)
solver.add(If(Nina, nina_statement, Not(nina_statement)))

# Oliver: "Exactly two of George, Hannah, Ian, and Julia are knights."
oliver_statement = (count_knights([George, Hannah, Ian, Julia]) == 2)
solver.add(If(Oliver, oliver_statement, Not(oliver_statement)))

# Paula: "Rachel is a knight if and only if Quentin is a knave."
paula_statement = (Rachel == Not(Quentin))
solver.add(If(Paula, paula_statement, Not(paula_statement)))

# Group C statements
# Quentin: "At least five of us in Group C are knights."
quentin_statement = (count_knights([Quentin, Rachel, Sam, Tina, Ursula, Victor, Wendy, Xavier]) >= 5)
solver.add(If(Quentin, quentin_statement, Not(quentin_statement)))

# Rachel: "Charlie is a knight, Lily is a knight, and Victor is a knave."
rachel_statement = And(
    Charlie,
    Lily,
    Not(Victor)
)
solver.add(If(Rachel, rachel_statement, Not(rachel_statement)))

# Sam: "Tina is a knave, Oliver is a knave, and Ursula is a knave."
sam_statement = And(
    Not(Tina),
    Not(Oliver),
    Not(Ursula)
)
solver.add(If(Sam, sam_statement, Not(sam_statement)))

# Tina: "Rachel is a knave or Mason is a knave."
tina_statement = Or(Not(Rachel), Not(Mason))
solver.add(If(Tina, tina_statement, Not(tina_statement)))

# Ursula: "Ian and Julia are both knights."
ursula_statement = And(Ian, Julia)
solver.add(If(Ursula, ursula_statement, Not(ursula_statement)))

# Victor: "Exactly two of Alice, Bob, Charlie, and Diana are knaves."
# Knaves = not knights, so count of knaves = 4 - count of knights
victor_statement = (count_knights([Alice, Bob, Charlie, Diana]) == 2)
solver.add(If(Victor, victor_statement, Not(victor_statement)))

# Wendy: "Victor is a knave, Ursula is a knave, and Xavier is a knight."
wendy_statement = And(
    Not(Victor),
    Not(Ursula),
    Xavier
)
solver.add(If(Wendy, wendy_statement, Not(wendy_statement)))

# Xavier: "Exactly four of us in Group C are knights, and Sam is a knight."
xavier_statement = And(
    count_knights([Quentin, Rachel, Sam, Tina, Ursula, Victor, Wendy, Xavier]) == 4,
    Sam
)
solver.add(If(Xavier, xavier_statement, Not(xavier_statement)))

# Check for satisfiability
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    # Print the assignment for each person
    people = [
        ("Alice", Alice), ("Bob", Bob), ("Charlie", Charlie), ("Diana", Diana), ("Ethan", Ethan), ("Fiona", Fiona), ("George", George), ("Hannah", Hannah),
        ("Ian", Ian), ("Julia", Julia), ("Kevin", Kevin), ("Lily", Lily), ("Mason", Mason), ("Nina", Nina), ("Oliver", Oliver), ("Paula", Paula),
        ("Quentin", Quentin), ("Rachel", Rachel), ("Sam", Sam), ("Tina", Tina), ("Ursula", Ursula), ("Victor", Victor), ("Wendy", Wendy), ("Xavier", Xavier)
    ]
    for name, var in people:
        print(f"{name} = {'knight' if model[var] else 'knave'}")
elif result == unsat:
    print("STATUS: unsat")
    print("RAW_RESULT: unsat")
else:
    print("STATUS: unknown")