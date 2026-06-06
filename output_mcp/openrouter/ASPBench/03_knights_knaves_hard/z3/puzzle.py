from z3 import *

# Define Bool variables for each person (True = knight)
names = [
    'Alice','Bob','Charlie','Diana','Ethan','Fiona','George','Hannah',
    'Ian','Julia','Kevin','Lily','Mason','Nina','Oliver','Paula',
    'Quentin','Rachel','Sam','Tina','Ursula','Victor','Wendy','Xavier'
]
vars = {n: Bool(n) for n in names}

# Helper to sum Bool list as Int
def bool_sum(bool_list):
    return Sum([If(b, 1, 0) for b in bool_list])

# Group lists
A = [vars[n] for n in ['Alice','Bob','Charlie','Diana','Ethan','Fiona','George','Hannah']]
B = [vars[n] for n in ['Ian','Julia','Kevin','Lily','Mason','Nina','Oliver','Paula']]
C = [vars[n] for n in ['Quentin','Rachel','Sam','Tina','Ursula','Victor','Wendy','Xavier']]
All = A + B + C

solver = Solver()

# Statements
# 1 Alice
alice_stmt = And(Not(vars['Hannah']), Or(Not(vars['Bob']), vars['Charlie']), bool_sum(A) == 4)
solver.add(vars['Alice'] == alice_stmt)
# 2 Bob
bob_stmt = (vars['Diana'] == vars['Bob'])
solver.add(vars['Bob'] == bob_stmt)
# 3 Charlie
charlie_stmt = (bool_sum(All) == 12)
solver.add(vars['Charlie'] == charlie_stmt)
# 4 Diana
diana_stmt = And(vars['Ethan'] != vars['Fiona'], Not(vars['Hannah']))
solver.add(vars['Diana'] == diana_stmt)
# 5 Ethan
ethan_stmt = (vars['George'] == vars['Alice'])
solver.add(vars['Ethan'] == ethan_stmt)
# 6 Fiona
fiona_stmt = And(vars['Bob'] != vars['Charlie'], vars['Fiona'])
solver.add(vars['Fiona'] == fiona_stmt)
# 7 George
george_stmt = (vars['Alice'] == vars['Hannah'])
solver.add(vars['George'] == george_stmt)
# 8 Hannah
hannah_stmt = (bool_sum([vars['Bob'], vars['Charlie'], vars['Diana']]) == 1)
solver.add(vars['Hannah'] == hannah_stmt)
# 9 Ian
ian_stmt = And(vars['Alice'] == vars['Paula'], Not(vars['Julia']))
solver.add(vars['Ian'] == ian_stmt)
# 10 Julia
julia_stmt = And(vars['Kevin'], vars['Nina'])
solver.add(vars['Julia'] == julia_stmt)
# 11 Kevin
kevin_stmt = Or(vars['Oliver'], Not(vars['Lily']))
solver.add(vars['Kevin'] == kevin_stmt)
# 12 Lily
lily_stmt = And(bool_sum(B) == 4, Not(vars['Oliver']))
solver.add(vars['Lily'] == lily_stmt)
# 13 Mason
mason_stmt = And(vars['Bob'] == vars['Ethan'], Not(vars['Julia']))
solver.add(vars['Mason'] == mason_stmt)
# 14 Nina
nina_stmt = (vars['Ian'] != vars['Paula'])
solver.add(vars['Nina'] == nina_stmt)
# 15 Oliver
oliver_stmt = (bool_sum([vars['George'], vars['Hannah'], vars['Ian'], vars['Julia']]) == 2)
solver.add(vars['Oliver'] == oliver_stmt)
# 16 Paula
paula_stmt = (vars['Rachel'] == Not(vars['Quentin']))
solver.add(vars['Paula'] == paula_stmt)
# 17 Quentin
quentin_stmt = (bool_sum(C) >= 5)
solver.add(vars['Quentin'] == quentin_stmt)
# 18 Rachel
rachel_stmt = And(vars['Charlie'], vars['Lily'], Not(vars['Victor']))
solver.add(vars['Rachel'] == rachel_stmt)
# 19 Sam
sam_stmt = And(Not(vars['Tina']), Not(vars['Oliver']), Not(vars['Ursula']))
solver.add(vars['Sam'] == sam_stmt)
# 20 Tina
tina_stmt = Or(Not(vars['Rachel']), Not(vars['Mason']))
solver.add(vars['Tina'] == tina_stmt)
# 21 Ursula
ursula_stmt = And(vars['Ian'], vars['Julia'])
solver.add(vars['Ursula'] == ursula_stmt)
# 22 Victor
# exactly two knaves among Alice,Bob,Charlie,Diana
knaves = [Not(vars['Alice']), Not(vars['Bob']), Not(vars['Charlie']), Not(vars['Diana'])]
victor_stmt = (bool_sum(knaves) == 2)
solver.add(vars['Victor'] == victor_stmt)
# 23 Wendy
wendy_stmt = And(Not(vars['Victor']), Not(vars['Ursula']), vars['Xavier'])
solver.add(vars['Wendy'] == wendy_stmt)
# 24 Xavier
xavier_stmt = And(bool_sum(C) == 4, vars['Sam'])
solver.add(vars['Xavier'] == xavier_stmt)

# Solve
result = solver.check()
if result == sat:
    m = solver.model()
    print('STATUS: sat')
    for n in names:
        val = m[vars[n]]
        # model may leave some uninterpreted if not needed, use model_completion
        if val is None:
            val = m.eval(vars[n], model_completion=True)
        print(f"{n} =", 'knight' if is_true(val) else 'knave')
elif result == unsat:
    print('STATUS: unsat')
else:
    print('STATUS: unknown')