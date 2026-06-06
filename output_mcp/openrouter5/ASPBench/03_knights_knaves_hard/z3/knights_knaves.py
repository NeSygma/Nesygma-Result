from z3 import *

# Create boolean variables: True = Knight, False = Knave
# Group A
Alice, Bob, Charlie, Diana, Ethan, Fiona, George, Hannah = Bools('Alice Bob Charlie Diana Ethan Fiona George Hannah')
# Group B
Ian, Julia, Kevin, Lily, Mason, Nina, Oliver, Paula = Bools('Ian Julia Kevin Lily Mason Nina Oliver Paula')
# Group C
Quentin, Rachel, Sam, Tina, Ursula, Victor, Wendy, Xavier = Bools('Quentin Rachel Sam Tina Ursula Victor Wendy Xavier')

# All inhabitants
all_inhabitants = [Alice, Bob, Charlie, Diana, Ethan, Fiona, George, Hannah,
                   Ian, Julia, Kevin, Lily, Mason, Nina, Oliver, Paula,
                   Quentin, Rachel, Sam, Tina, Ursula, Victor, Wendy, Xavier]

groupA = [Alice, Bob, Charlie, Diana, Ethan, Fiona, George, Hannah]
groupB = [Ian, Julia, Kevin, Lily, Mason, Nina, Oliver, Paula]
groupC = [Quentin, Rachel, Sam, Tina, Ursula, Victor, Wendy, Xavier]

solver = Solver()

# Helper: statement is true iff speaker is a knight
# We'll add constraints: speaker_is_knight == statement_content

# --- Group A ---

# Alice says: "Hannah is a knave, and (Bob is a knave or Charlie is a knight), and exactly four of us in Group A are knights."
# Hannah is a knave = Not(Hannah)
# Bob is a knave = Not(Bob)
# Charlie is a knight = Charlie
# exactly four of Group A are knights = Sum(If(p,1,0) for p in groupA) == 4
alice_stmt = And(Not(Hannah), Or(Not(Bob), Charlie), Sum([If(p,1,0) for p in groupA]) == 4)
solver.add(Alice == alice_stmt)

# Bob says: "Diana is the same type as me."
# Diana same type as Bob = (Bob == Diana)
bob_stmt = (Bob == Diana)
solver.add(Bob == bob_stmt)

# Charlie says: "Exactly twelve of us are knights."
charlie_stmt = (Sum([If(p,1,0) for p in all_inhabitants]) == 12)
solver.add(Charlie == charlie_stmt)

# Diana says: "Ethan and Fiona are of different types, and Hannah is a knave."
# different types = Ethan != Fiona
diana_stmt = And(Ethan != Fiona, Not(Hannah))
solver.add(Diana == diana_stmt)

# Ethan says: "George is a knight if and only if Alice is a knight."
ethan_stmt = (George == Alice)
solver.add(Ethan == ethan_stmt)

# Fiona says: "Bob and Charlie are of different types, and I am a knight."
fiona_stmt = And(Bob != Charlie, Fiona)
solver.add(Fiona == fiona_stmt)

# George says: "Alice and Hannah are of the same type."
george_stmt = (Alice == Hannah)
solver.add(George == george_stmt)

# Hannah says: "Exactly one of Bob, Charlie, and Diana is a knight."
hannah_stmt = (Sum([If(Bob,1,0), If(Charlie,1,0), If(Diana,1,0)]) == 1)
solver.add(Hannah == hannah_stmt)

# --- Group B ---

# Ian says: "Alice and Paula are of the same type, and Julia is a knave."
ian_stmt = And(Alice == Paula, Not(Julia))
solver.add(Ian == ian_stmt)

# Julia says: "Kevin is a knight and Nina is a knight."
julia_stmt = And(Kevin, Nina)
solver.add(Julia == julia_stmt)

# Kevin says: "Either Oliver is a knight or Lily is a knave."
kevin_stmt = Or(Oliver, Not(Lily))
solver.add(Kevin == kevin_stmt)

# Lily says: "Exactly four of us in Group B are knights, and Oliver is a knave."
lily_stmt = And(Sum([If(p,1,0) for p in groupB]) == 4, Not(Oliver))
solver.add(Lily == lily_stmt)

# Mason says: "Bob and Ethan are of the same type, and Julia is a knave."
mason_stmt = And(Bob == Ethan, Not(Julia))
solver.add(Mason == mason_stmt)

# Nina says: "Ian and Paula are of different types."
nina_stmt = (Ian != Paula)
solver.add(Nina == nina_stmt)

# Oliver says: "Exactly two of George, Hannah, Ian, and Julia are knights."
oliver_stmt = (Sum([If(George,1,0), If(Hannah,1,0), If(Ian,1,0), If(Julia,1,0)]) == 2)
solver.add(Oliver == oliver_stmt)

# Paula says: "Rachel is a knight if and only if Quentin is a knave."
paula_stmt = (Rachel == Not(Quentin))
solver.add(Paula == paula_stmt)

# --- Group C ---

# Quentin says: "At least five of us in Group C are knights."
quentin_stmt = (Sum([If(p,1,0) for p in groupC]) >= 5)
solver.add(Quentin == quentin_stmt)

# Rachel says: "Charlie is a knight, Lily is a knight, and Victor is a knave."
rachel_stmt = And(Charlie, Lily, Not(Victor))
solver.add(Rachel == rachel_stmt)

# Sam says: "Tina is a knave, Oliver is a knave, and Ursula is a knave."
sam_stmt = And(Not(Tina), Not(Oliver), Not(Ursula))
solver.add(Sam == sam_stmt)

# Tina says: "Rachel is a knave or Mason is a knave."
tina_stmt = Or(Not(Rachel), Not(Mason))
solver.add(Tina == tina_stmt)

# Ursula says: "Ian and Julia are both knights."
ursula_stmt = And(Ian, Julia)
solver.add(Ursula == ursula_stmt)

# Victor says: "Exactly two of Alice, Bob, Charlie, and Diana are knaves."
# knave = Not(knight)
victor_stmt = (Sum([If(Not(Alice),1,0), If(Not(Bob),1,0), If(Not(Charlie),1,0), If(Not(Diana),1,0)]) == 2)
solver.add(Victor == victor_stmt)

# Wendy says: "Victor is a knave, Ursula is a knave, and Xavier is a knight."
wendy_stmt = And(Not(Victor), Not(Ursula), Xavier)
solver.add(Wendy == wendy_stmt)

# Xavier says: "Exactly four of us in Group C are knights, and Sam is a knight."
xavier_stmt = And(Sum([If(p,1,0) for p in groupC]) == 4, Sam)
solver.add(Xavier == xavier_stmt)

# Solve
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("Solution found:")
    for name, var in [
        ("Alice", Alice), ("Bob", Bob), ("Charlie", Charlie), ("Diana", Diana),
        ("Ethan", Ethan), ("Fiona", Fiona), ("George", George), ("Hannah", Hannah),
        ("Ian", Ian), ("Julia", Julia), ("Kevin", Kevin), ("Lily", Lily),
        ("Mason", Mason), ("Nina", Nina), ("Oliver", Oliver), ("Paula", Paula),
        ("Quentin", Quentin), ("Rachel", Rachel), ("Sam", Sam), ("Tina", Tina),
        ("Ursula", Ursula), ("Victor", Victor), ("Wendy", Wendy), ("Xavier", Xavier)
    ]:
        val = m.eval(var)
        typ = "knight" if val else "knave"
        print(f"  {name}: {typ}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")