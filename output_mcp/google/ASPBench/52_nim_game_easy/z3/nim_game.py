from z3 import *

def xor(a, b):
    return a ^ b

# Initial state
piles = [3, 4, 5]
nim_sum = piles[0] ^ piles[1] ^ piles[2]

print(f"nim_sum: {nim_sum}")
print(f"is_winning_position: {nim_sum != 0}")

# Find optimal moves
# An optimal move changes one pile P_i to P_i' such that the new nim-sum is 0.
# New nim-sum = (nim_sum ^ P_i) ^ P_i' = 0
# P_i' = nim_sum ^ P_i
# A move is valid if 0 <= P_i' < P_i

optimal_moves = []
for i in range(len(piles)):
    p_i = piles[i]
    p_i_prime = nim_sum ^ p_i
    if p_i_prime < p_i:
        stones_to_remove = p_i - p_i_prime
        resulting_piles = list(piles)
        resulting_piles[i] = p_i_prime
        optimal_moves.append({
            "pile": i + 1,
            "stones": stones_to_remove,
            "resulting_piles": resulting_piles
        })

print("STATUS: sat")
print(f"optimal_moves: {optimal_moves}")