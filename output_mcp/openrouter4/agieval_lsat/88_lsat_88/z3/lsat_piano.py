from z3 import *

def solve():
    solver = Solver()
    
    # 5 solos, indices 0-4 (1-indexed: 1-5)
    pianist = [Bool(f'pianist_{i}') for i in range(5)]  # True=Wayne, False=Zara
    piece_type = [Bool(f'type_{i}') for i in range(5)]   # True=Traditional, False=Modern
    
    # Constraint 1: The third solo (index 2) is a traditional piece.
    solver.add(piece_type[2] == True)
    
    # Constraint 2: Exactly two of the traditional pieces are performed consecutively.
    # Count consecutive traditional pairs
    pairs = [And(piece_type[i], piece_type[i+1]) for i in range(4)]
    solver.add(Sum([If(p, 1, 0) for p in pairs]) == 1)
    
    # Constraint 3: In the fourth solo (index 3), either Wayne performs a traditional piece
    # or Zara performs a modern piece.
    # (pianist[3]==W AND type[3]==T) OR (pianist[3]==Z AND type[3]==M)
    solver.add(Or(
        And(pianist[3] == True, piece_type[3] == True),
        And(pianist[3] == False, piece_type[3] == False)
    ))
    
    # Constraint 4: The pianist who performs the second solo (index 1) does not perform the fifth solo (index 4).
    solver.add(pianist[1] != pianist[4])
    
    # Constraint 5: No traditional piece is performed until Wayne performs at least one modern piece.
    # For each solo i, if piece_type[i] is Traditional, there must exist some j < i with pianist[j]==W and piece_type[j]==M.
    for i in range(5):
        # Build the condition: there exists j < i such that Wayne did modern
        if i == 0:
            # No j < 0, so first solo cannot be traditional
            solver.add(piece_type[0] == False)
        else:
            earlier_wayne_modern = Or([And(pianist[j] == True, piece_type[j] == False) for j in range(i)])
            solver.add(Implies(piece_type[i] == True, earlier_wayne_modern))
    
    # Now test each option
    # Options define which positions are traditional (True) and which are modern (False)
    # A: first(1), third(3), fourth(4) -> indices 0,2,3 are T; 1,4 are M
    # B: second(2), third(3), fourth(4) -> indices 1,2,3 are T; 0,4 are M
    # C: third(3) and fourth(4) -> indices 2,3 are T; 0,1,4 are M
    # D: third(3) and fifth(5) -> indices 2,4 are T; 0,1,3 are M
    # E: fourth(4) and fifth(5) -> indices 3,4 are T; 0,1,2 are M
    
    options = [
        ("A", [True, False, True, True, False]),   # T, M, T, T, M
        ("B", [False, True, True, True, False]),   # M, T, T, T, M
        ("C", [False, False, True, True, False]),  # M, M, T, T, M
        ("D", [False, False, True, False, True]),  # M, M, T, M, T
        ("E", [False, False, False, True, True])   # M, M, M, T, T
    ]
    
    found_options = []
    for letter, trad_pattern in options:
        solver.push()
        # Add constraint that piece_type matches this pattern exactly
        for i in range(5):
            solver.add(piece_type[i] == trad_pattern[i])
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

if __name__ == "__main__":
    solve()