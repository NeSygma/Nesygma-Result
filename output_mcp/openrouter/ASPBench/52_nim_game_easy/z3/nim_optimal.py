from z3 import *

# Initial data
piles = [3, 4, 5]

solver = Solver()

# Decision variables
i = Int('i')  # pile index 0..2
r = Int('r')  # stones to remove

# Domain constraints
solver.add(i >= 0, i <= 2)
solver.add(r >= 1)
# r <= selected pile size
solver.add(Or(And(i == 0, r <= piles[0]),
              And(i == 1, r <= piles[1]),
              And(i == 2, r <= piles[2])))

# Resulting piles as BitVec (8 bits sufficient)
rp0 = BitVec('rp0', 8)
rp1 = BitVec('rp1', 8)
rp2 = BitVec('rp2', 8)

# Helper to convert Int expression to BitVec of size 8
def int2bv(expr):
    return Int2BV(expr, 8)

# Define resulting piles constraints
solver.add(rp0 == If(i == 0, int2bv(piles[0] - r), BitVecVal(piles[0], 8)))
solver.add(rp1 == If(i == 1, int2bv(piles[1] - r), BitVecVal(piles[1], 8)))
solver.add(rp2 == If(i == 2, int2bv(piles[2] - r), BitVecVal(piles[2], 8)))

# Optimal move condition: resulting nim-sum (xor) is zero
solver.add((rp0 ^ rp1 ^ rp2) == BitVecVal(0, 8))

# Compute current nim-sum (pure Python)
nim_sum = piles[0] ^ piles[1] ^ piles[2]
is_winning = nim_sum != 0

optimal_moves = []

while solver.check() == sat:
    m = solver.model()
    idx = m[i].as_long()
    stones = m[r].as_long()
    # compute resulting piles
    res = []
    for j, val in enumerate(piles):
        if j == idx:
            res.append(val - stones)
        else:
            res.append(val)
    optimal_moves.append((idx+1, stones, res))  # 1-indexed pile
    # block this move
    solver.add(Or(i != idx, r != stones))

# Output
print("STATUS: sat")
print(f"nim_sum = {nim_sum}")
print(f"is_winning_position = {is_winning}")
print(f"optimal_moves_count = {len(optimal_moves)}")
for idx, (pile, stones, res) in enumerate(optimal_moves, start=1):
    print(f"move{idx}_pile = {pile}")
    print(f"move{idx}_stones = {stones}")
    print(f"move{idx}_resulting_piles = {res}")