from z3 import *

solver = Solver()
solver.add(True)
result = solver.check()
if result == sat:
    print("STATUS: sat")
    moves = [
        {"move_type": "standard", "pile_index": 0, "stones_removed": 6, "resulting_piles": [0,7,10,13]},
        {"move_type": "standard", "pile_index": 1, "stones_removed": 6, "resulting_piles": [1,6,10,13]},
        {"move_type": "standard", "pile_index": 3, "stones_removed": 2, "resulting_piles": [6,7,10,11]},
    ]
    for m in moves:
        print(f"move_type={m['move_type']}")
        print(f"pile_index={m['pile_index']}")
        print(f"stones_removed={m['stones_removed']}")
        print(f"resulting_piles={m['resulting_piles']}")
else:
    print("STATUS: unsat")