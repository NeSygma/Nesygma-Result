from z3 import *

def solve():
    solver = Solver()
    
    students = ['J', 'K', 'L', 'M', 'O']
    plays = ['S', 'T', 'U']
    
    # R[s][p] is True if student s reviews play p
    R = [[Bool(f'R_{s}_{p}') for p in plays] for s in range(5)]
    
    # Helper to get index
    def get_idx(s):
        return {'J': 0, 'K': 1, 'L': 2, 'M': 3, 'O': 4}[s]
    
    # Each student reviews at least one play
    for i in range(5):
        solver.add(Or([R[i][j] for j in range(3)]))
        
    # Condition 1: Kramer and Lopez each review fewer plays than Megregian
    def count_plays(i):
        return Sum([If(R[i][j], 1, 0) for j in range(3)])
    
    solver.add(count_plays(get_idx('K')) < count_plays(get_idx('M')))
    solver.add(count_plays(get_idx('L')) < count_plays(get_idx('M')))
    
    # Condition 2: Neither Lopez nor Megregian reviews any play Jiang reviews
    for p in range(3):
        solver.add(Implies(R[get_idx('J')][p], Not(R[get_idx('L')][p])))
        solver.add(Implies(R[get_idx('J')][p], Not(R[get_idx('M')][p])))
        
    # Condition 3: Kramer and O'Neill both review Tamerlane (index 1)
    solver.add(R[get_idx('K')][1] == True)
    solver.add(R[get_idx('O')][1] == True)
    
    # Condition 4: Exactly two of the students review exactly the same play or plays
    # Define equality of sets for two students
    def same_set(i, j):
        return And([R[i][p] == R[j][p] for p in range(3)])
    
    # Count pairs (i, j) with i < j that have the same set
    pairs = []
    for i in range(5):
        for j in range(i + 1, 5):
            pairs.append(same_set(i, j))
            
    solver.add(Sum([If(p, 1, 0) for p in pairs]) == 1)
    
    # Helper for "only Sunset" (index 0)
    def only_sunset(i):
        return And(R[i][0], Not(R[i][1]), Not(R[i][2]))
    
    # Options
    options = {
        "A": ["L"],
        "B": ["O"],
        "C": ["J", "L"],
        "D": ["K", "O"],
        "E": ["L", "M"]
    }
    
    found_options = []
    for letter, student_list in options.items():
        solver.push()
        # Add constraint: exactly the students in student_list review only Sunset
        for s in students:
            if s in student_list:
                solver.add(only_sunset(get_idx(s)))
            else:
                solver.add(Not(only_sunset(get_idx(s))))
        
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

solve()