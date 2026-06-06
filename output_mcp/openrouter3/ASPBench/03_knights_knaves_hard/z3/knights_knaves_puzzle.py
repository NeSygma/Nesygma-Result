from z3 import *

# Create solver
solver = Solver()

# Define all 24 inhabitants as Boolean variables (True = Knight, False = Knave)
# Group A
Alice = Bool('Alice')
Bob = Bool('Bob')
Charlie = Bool('Charlie')
Diana = Bool('Diana')
Ethan = Bool('Ethan')
Fiona = Bool('Fiona')
George = Bool('George')
Hannah = Bool('Hannah')

# Group B
Ian = Bool('Ian')
Julia = Bool('Julia')
Kevin = Bool('Kevin')
Lily = Bool('Lily')
Mason = Bool('Mason')
Nina = Bool('Nina')
Oliver = Bool('Oliver')
Paula = Bool('Paula')

# Group C
Quentin = Bool('Quentin')
Rachel = Bool('Rachel')
Sam = Bool('Sam')
Tina = Bool('Tina')
Ursula = Bool('Ursula')
Victor = Bool('Victor')
Wendy = Bool('Wendy')
Xavier = Bool('Xavier')

# Helper function for "exactly N" conditions
def exactly_n(variables, n):
    """Returns a constraint that exactly n of the variables are True"""
    return Sum([If(v, 1, 0) for v in variables]) == n

# Helper function for "at least N" conditions
def at_least_n(variables, n):
    """Returns a constraint that at least n of the variables are True"""
    return Sum([If(v, 1, 0) for v in variables]) >= n

# Group A statements
# Alice: "Hannah is a knave, and (Bob is a knave or Charlie is a knight), and exactly four of us in Group A are knights."
group_a = [Alice, Bob, Charlie, Diana, Ethan, Fiona, George, Hannah]
alice_statement = And(Not(Hannah), Or(Not(Bob), Charlie), exactly_n(group_a, 4))
solver.add(Implies(Alice, alice_statement))
solver.add(Implies(Not(Alice), Not(alice_statement)))

# Bob: "Diana is the same type as me."
bob_statement = (Diana == Bob)
solver.add(Implies(Bob, bob_statement))
solver.add(Implies(Not(Bob), Not(bob_statement)))

# Charlie: "Exactly twelve of us are knights."
all_people = group_a + [Ian, Julia, Kevin, Lily, Mason, Nina, Oliver, Paula] + [Quentin, Rachel, Sam, Tina, Ursula, Victor, Wendy, Xavier]
charlie_statement = exactly_n(all_people, 12)
solver.add(Implies(Charlie, charlie_statement))
solver.add(Implies(Not(Charlie), Not(charlie_statement)))

# Diana: "Ethan and Fiona are of different types, and Hannah is a knave."
diana_statement = And(Ethan != Fiona, Not(Hannah))
solver.add(Implies(Diana, diana_statement))
solver.add(Implies(Not(Diana), Not(diana_statement)))

# Ethan: "George is a knight if and only if Alice is a knight."
ethan_statement = (George == Alice)
solver.add(Implies(Ethan, ethan_statement))
solver.add(Implies(Not(Ethan), Not(ethan_statement)))

# Fiona: "Bob and Charlie are of different types, and I am a knight."
fiona_statement = And(Bob != Charlie, Fiona)
solver.add(Implies(Fiona, fiona_statement))
solver.add(Implies(Not(Fiona), Not(fiona_statement)))

# George: "Alice and Hannah are of the same type."
george_statement = (Alice == Hannah)
solver.add(Implies(George, george_statement))
solver.add(Implies(Not(George), Not(george_statement)))

# Hannah: "Exactly one of Bob, Charlie, and Diana is a knight."
hannah_statement = exactly_n([Bob, Charlie, Diana], 1)
solver.add(Implies(Hannah, hannah_statement))
solver.add(Implies(Not(Hannah), Not(hannah_statement)))

# Group B statements
# Ian: "Alice and Paula are of the same type, and Julia is a knave."
ian_statement = And(Alice == Paula, Not(Julia))
solver.add(Implies(Ian, ian_statement))
solver.add(Implies(Not(Ian), Not(ian_statement)))

# Julia: "Kevin is a knight and Nina is a knight."
julia_statement = And(Kevin, Nina)
solver.add(Implies(Julia, julia_statement))
solver.add(Implies(Not(Julia), Not(julia_statement)))

# Kevin: "Either Oliver is a knight or Lily is a knave."
kevin_statement = Or(Oliver, Not(Lily))
solver.add(Implies(Kevin, kevin_statement))
solver.add(Implies(Not(Kevin), Not(kevin_statement)))

# Lily: "Exactly four of us in Group B are knights, and Oliver is a knave."
group_b = [Ian, Julia, Kevin, Lily, Mason, Nina, Oliver, Paula]
lily_statement = And(exactly_n(group_b, 4), Not(Oliver))
solver.add(Implies(Lily, lily_statement))
solver.add(Implies(Not(Lily), Not(lily_statement)))

# Mason: "Bob and Ethan are of the same type, and Julia is a knave."
mason_statement = And(Bob == Ethan, Not(Julia))
solver.add(Implies(Mason, mason_statement))
solver.add(Implies(Not(Mason), Not(mason_statement)))

# Nina: "Ian and Paula are of different types."
nina_statement = (Ian != Paula)
solver.add(Implies(Nina, nina_statement))
solver.add(Implies(Not(Nina), Not(nina_statement)))

# Oliver: "Exactly two of George, Hannah, Ian, and Julia are knights."
oliver_statement = exactly_n([George, Hannah, Ian, Julia], 2)
solver.add(Implies(Oliver, oliver_statement))
solver.add(Implies(Not(Oliver), Not(oliver_statement)))

# Paula: "Rachel is a knight if and only if Quentin is a knave."
paula_statement = (Rachel == Not(Quentin))
solver.add(Implies(Paula, paula_statement))
solver.add(Implies(Not(Paula), Not(paula_statement)))

# Group C statements
# Quentin: "At least five of us in Group C are knights."
group_c = [Quentin, Rachel, Sam, Tina, Ursula, Victor, Wendy, Xavier]
quentin_statement = at_least_n(group_c, 5)
solver.add(Implies(Quentin, quentin_statement))
solver.add(Implies(Not(Quentin), Not(quentin_statement)))

# Rachel: "Charlie is a knight, Lily is a knight, and Victor is a knave."
rachel_statement = And(Charlie, Lily, Not(Victor))
solver.add(Implies(Rachel, rachel_statement))
solver.add(Implies(Not(Rachel), Not(rachel_statement)))

# Sam: "Tina is a knave, Oliver is a knave, and Ursula is a knave."
sam_statement = And(Not(Tina), Not(Oliver), Not(Ursula))
solver.add(Implies(Sam, sam_statement))
solver.add(Implies(Not(Sam), Not(sam_statement)))

# Tina: "Rachel is a knave or Mason is a knave."
tina_statement = Or(Not(Rachel), Not(Mason))
solver.add(Implies(Tina, tina_statement))
solver.add(Implies(Not(Tina), Not(tina_statement)))

# Ursula: "Ian and Julia are both knights."
ursula_statement = And(Ian, Julia)
solver.add(Implies(Ursula, ursula_statement))
solver.add(Implies(Not(Ursula), Not(ursula_statement)))

# Victor: "Exactly two of Alice, Bob, Charlie, and Diana are knaves."
# This means exactly two are False (knaves), so exactly two are True (knights)
victor_statement = exactly_n([Alice, Bob, Charlie, Diana], 2)
solver.add(Implies(Victor, victor_statement))
solver.add(Implies(Not(Victor), Not(victor_statement)))

# Wendy: "Victor is a knave, Ursula is a knave, and Xavier is a knight."
wendy_statement = And(Not(Victor), Not(Ursula), Xavier)
solver.add(Implies(Wendy, wendy_statement))
solver.add(Implies(Not(Wendy), Not(wendy_statement)))

# Xavier: "Exactly four of us in Group C are knights, and Sam is a knight."
xavier_statement = And(exactly_n(group_c, 4), Sam)
solver.add(Implies(Xavier, xavier_statement))
solver.add(Implies(Not(Xavier), Not(xavier_statement)))

# Check for solution
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("\nSolution found:")
    print("\nGroup A (Knights/Knaves):")
    for person in [Alice, Bob, Charlie, Diana, Ethan, Fiona, George, Hannah]:
        person_name = str(person)
        type_str = "Knight" if m[person] == True else "Knave"
        print(f"  {person_name}: {type_str}")
    
    print("\nGroup B (Knights/Knaves):")
    for person in [Ian, Julia, Kevin, Lily, Mason, Nina, Oliver, Paula]:
        person_name = str(person)
        type_str = "Knight" if m[person] == True else "Knave"
        print(f"  {person_name}: {type_str}")
    
    print("\nGroup C (Knights/Knaves):")
    for person in [Quentin, Rachel, Sam, Tina, Ursula, Victor, Wendy, Xavier]:
        person_name = str(person)
        type_str = "Knight" if m[person] == True else "Knave"
        print(f"  {person_name}: {type_str}")
    
    # Count total knights
    total_knights = sum(1 for person in all_people if m[person] == True)
    print(f"\nTotal knights: {total_knights}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")