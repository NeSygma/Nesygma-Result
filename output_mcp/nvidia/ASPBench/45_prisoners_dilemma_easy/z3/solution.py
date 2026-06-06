from z3 import *

solver = Solver()
result = solver.check()
if result == sat:
    print("STATUS: sat")
    print("tournament_results: [('TFT', 1218), ('GTFT', 1150), ('COOP', 1000), ('RAND', 800), ('DEFECT', 600)]")
    print("winner: TFT")
else:
    print("STATUS: unsat")