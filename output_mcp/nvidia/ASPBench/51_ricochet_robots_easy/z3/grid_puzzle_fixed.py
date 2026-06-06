from z3 import *

solver = Solver()

# Declare variables
A_row = [Int(f'A_r_{i}') for i in range(4)]
A_col = [Int(f'A_c_{i}') for i in range(4)]
B_row = [Int(f'B_r_{i}') for i in range(4)]
B_col = [Int(f'B_c_{i}') for i in range(4)]
move_robot = [Int(f'mr_{i}') for i in range(3)]
to_A_row = [Int(f'tAR_{i}') for i in range(3)]
to_A_col = [Int(f'tAC_{i}') for i in range(3)]
to_B_row = [Int(f'tBR_{i}') for i in range(3)]
to_B_col = [Int(f'tBC_{i}') for i in range(3)]

# Initial positions
solver.add(A_row[0] == 0)
solver.add(A_col[0] == 1)
solver.add(B_row[0] == 1)
solver.add(B_col[0] == 1)

# Wall constraints: cannot occupy wall cells (0,2) and (1,2)
for i in range(4):
    solver.add(Not(Or(And(A_row[i] == 0, A_col[i] == 2), And(A_row[i] == 1, A_col[i] == 2))))
    solver.add(Not(Or(And(B_row[i] == 0, B_col[i] == 2), And(B_row[i] == 1, B_col[i] == 2))))

# No collision at any time step
for i in range(4):
    solver.add(Not(And(A_row[i] == B_row[i], A_col[i] == B_col[i])))

# Domain bounds
for i in range(4):
    solver.add(A_row[i] >= 0, A_row[i] <= 3, A_col[i] >= 0, A_col[i] <= 3)
    solver.add(B_row[i] >= 0, B_row[i] <= 3, B_col[i] >= 0, B_col[i] <= 3)

# Moves
for i in range(3):
    # move_robot[i] is 0 for A, 1 for B
    solver.add(move_robot[i] >= 0)
    solver.add(move_robot[i] <= 1)
    
    # A moves
    solver.add(A_row[i+1] == If(move_robot[i] == 0, to_A_row[i], A_row[i]))
    solver.add(A_col[i+1] == If(move_robot[i] == 0, to_A_col[i], A_col[i]))
    # B moves
    solver.add(B_row[i+1] == If(move_robot[i] == 1, to_B_row[i], B_row[i]))
    solver.add(B_col[i+1] == If(move_robot[i] == 1, to_B_col[i], B_col[i]))
    
    # A move constraints
    solver.add(If(move_robot[i] == 0,
                 Abs(to_A_row[i] - A_row[i]) + Abs(to_A_col[i] - A_col[i]) == 1,
                 True))
    solver.add(If(move_robot[i] == 0,
                 And(to_A_row[i] >= 0, to_A_row[i] <= 3, to_A_col[i] >= 0, to_A_col[i] <= 3),
                 True))
    solver.add(If(move_robot[i] == 0,
                 Not(Or(And(to_A_row[i] == 0, to_A_col[i] == 2), And(to_A_row[i] == 1, to_A_col[i] == 2))),
                 True))
    solver.add(If(move_robot[i] == 0,
                 Not(And(to_A_row[i] == B_row[i], to_A_col[i] == B_col[i])),
                 True))
    
    # B move constraints
    solver.add(If(move_robot[i] == 1,
                 Abs(to_B_row[i] - B_row[i]) + Abs(to_B_col[i] - B_col[i]) == 1,
                 True))
    solver.add(If(move_robot[i] == 1,
                 And(to_B_row[i] >= 0, to_B_row[i] <= 3, to_B_col[i] >= 0, to_B_col[i] <= 3),
                 True))
    solver.add(If(move_robot[i] == 1,
                 Not(Or(And(to_B_row[i] == 0, to_B_col[i] == 2), And(to_B_row[i] == 1, to_B_col[i] == 2))),
                 True))
    solver.add(If(move_robot[i] == 1,
                 Not(And(to_B_row[i] == A_row[i], to_B_col[i] == A_col[i])),
                 True))

# Goal: A reaches (2,1) after 3 moves
solver.add(A_row[3] == 2)
solver.add(A_col[3] == 1)

# Solve
result = solver.check()
if result == sat:
    print('STATUS: sat')
    m = solver.model()
    # extract sequence
    seq = []
    for i in range(3):
        robot_val = m[move_robot[i]]
        robot = 'A' if robot_val == 0 else 'B'
        if robot == 'A':
            fromr = m[A_row[i]]
            fromc = m[A_col[i]]
            tor = m[to_A_row[i]]
            toc = m[to_A_col[i]]
        else:
            fromr = m[B_row[i]]
            fromc = m[B_col[i]]
            tor = m[to_B_row[i]]
            toc = m[to_B_col[i]]
        seq.append({'robot': robot, 'from': [fromr, fromc], 'to': [tor, toc]})
    final_positions = {'A': [m[A_row[3]], m[A_col[3]]], 'B': [m[B_row[3]], m[B_col[3]]]}
    print('solution_found = True')
    print('moves = 3')
    print('sequence =', seq)
    print('final_positions =', final_positions)
else:
    print('STATUS: unsat')