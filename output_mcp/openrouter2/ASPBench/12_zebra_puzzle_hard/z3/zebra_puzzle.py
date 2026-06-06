from z3 import *

# Define attribute lists
nationalities = ["American","Brazilian","Canadian","Dutch","Egyptian","French","German","Hungarian"]
professions = ["Architect","Biologist","Chemist","Doctor","Engineer","Lawyer","Musician","Pilot"]
cars = ["Audi","BMW","Ford","Honda","Mercedes","Nissan","Toyota","Volvo"]
drinks = ["Coffee","Juice","Milk","Soda","Tea","Water","Wine","Whiskey"]
music = ["Blues","Classical","Folk","Jazz","Pop","Rap","Reggae","Rock"]
pets = ["Cat","Dog","Fish","Hamster","Lizard","Parrot","Rabbit","Snake"]
destinations = ["Bali","Dubai","London","New York","Paris","Rome","Sydney","Tokyo"]

# Create mapping from name to index
nat_idx = {name:i for i,name in enumerate(nationalities)}
prof_idx = {name:i for i,name in enumerate(professions)}
car_idx = {name:i for i,name in enumerate(cars)}
drink_idx = {name:i for i,name in enumerate(drinks)}
music_idx = {name:i for i,name in enumerate(music)}
pet_idx = {name:i for i,name in enumerate(pets)}
dest_idx = {name:i for i,name in enumerate(destinations)}

# Create position variables for each attribute value
nat_pos = [Int(f'nat_{name}') for name in nationalities]
prof_pos = [Int(f'prof_{name}') for name in professions]
car_pos = [Int(f'car_{name}') for name in cars]
drink_pos = [Int(f'drink_{name}') for name in drinks]
music_pos = [Int(f'music_{name}') for name in music]
pet_pos = [Int(f'pet_{name}') for name in pets]
dest_pos = [Int(f'dest_{name}') for name in destinations]

solver = Solver()

# Domain constraints: positions 0..7
for lst in [nat_pos, prof_pos, car_pos, drink_pos, music_pos, pet_pos, dest_pos]:
    for v in lst:
        solver.add(v >= 0, v <= 7)

# Distinctness constraints
solver.add(Distinct(nat_pos))
solver.add(Distinct(prof_pos))
solver.add(Distinct(car_pos))
solver.add(Distinct(drink_pos))
solver.add(Distinct(music_pos))
solver.add(Distinct(pet_pos))
solver.add(Distinct(dest_pos))

# Constraints
# 1. The person in suite #4 drinks Milk
solver.add(drink_pos[drink_idx['Milk']] == 3)
# 2. The Hungarian lives in suite #4
solver.add(nat_pos[nat_idx['Hungarian']] == 3)
# 3. The American is a Lawyer
solver.add(nat_pos[nat_idx['American']] == prof_pos[prof_idx['Lawyer']])
# 4. The person who drives a BMW is a Biologist
solver.add(car_pos[car_idx['BMW']] == prof_pos[prof_idx['Biologist']])
# 5. The Canadian owns a Snake
solver.add(nat_pos[nat_idx['Canadian']] == pet_pos[pet_idx['Snake']])
# 6. The person who listens to Classical music drives an Audi
solver.add(music_pos[music_idx['Classical']] == car_pos[car_idx['Audi']])
# 7. The German drinks Coffee
solver.add(nat_pos[nat_idx['German']] == drink_pos[drink_idx['Coffee']])
# 8. The person going to Tokyo is a Chemist
solver.add(dest_pos[dest_idx['Tokyo']] == prof_pos[prof_idx['Chemist']])
# 9. The Engineer's suite is immediately to the left of the Lawyer's suite
solver.add(prof_pos[prof_idx['Engineer']] + 1 == prof_pos[prof_idx['Lawyer']])
# 10. The Dog owner lives next to the Volvo driver
solver.add(Or(abs(pet_pos[pet_idx['Dog']] - car_pos[car_idx['Volvo']]) == 1))
# 11. The Rock music listener lives next to the Pop music listener
solver.add(Or(abs(music_pos[music_idx['Rock']] - music_pos[music_idx['Pop']]) == 1))
# 12. The person going to Paris lives next to the Fish owner
solver.add(Or(abs(dest_pos[dest_idx['Paris']] - pet_pos[pet_idx['Fish']]) == 1))
# 13. The Pilot lives in an even-numbered suite (2,4,6,8) -> indices 1,3,5,7
solver.add(Or(prof_pos[prof_idx['Pilot']] == 1,
              prof_pos[prof_idx['Pilot']] == 3,
              prof_pos[prof_idx['Pilot']] == 5,
              prof_pos[prof_idx['Pilot']] == 7))
# 14. The Wine drinker's suite is to the right of the Coffee drinker's suite
solver.add(drink_pos[drink_idx['Wine']] > drink_pos[drink_idx['Coffee']])
# 15. The Ford driver has a neighbor who drinks Tea
solver.add(Or(abs(car_pos[car_idx['Ford']] - drink_pos[drink_idx['Tea']]) == 1))
# 16. The Nissan driver does not live in suite #1 or #8
solver.add(car_pos[car_idx['Nissan']] != 0)
solver.add(car_pos[car_idx['Nissan']] != 7)
# 17. The Jazz listener's suite number is less than the Blues listener's suite number
solver.add(music_pos[music_idx['Jazz']] < music_pos[music_idx['Blues']])
# 18. The Dutch person lives in suite #1
solver.add(nat_pos[nat_idx['Dutch']] == 0)

# Solve
result = solver.check()

if result == sat:
    m = solver.model()
    # Build mapping from position to attribute value
    pos_to_nat = {m[nat_pos[i]].as_long(): nationalities[i] for i in range(len(nationalities))}
    pos_to_prof = {m[prof_pos[i]].as_long(): professions[i] for i in range(len(professions))}
    pos_to_car = {m[car_pos[i]].as_long(): cars[i] for i in range(len(cars))}
    pos_to_drink = {m[drink_pos[i]].as_long(): drinks[i] for i in range(len(drinks))}
    pos_to_music = {m[music_pos[i]].as_long(): music[i] for i in range(len(music))}
    pos_to_pet = {m[pet_pos[i]].as_long(): pets[i] for i in range(len(pets))}
    pos_to_dest = {m[dest_pos[i]].as_long(): destinations[i] for i in range(len(destinations))}

    solution = []
    for i in range(8):
        solution.append({
            'suite': i+1,
            'nationality': pos_to_nat[i],
            'profession': pos_to_prof[i],
            'car': pos_to_car[i],
            'drink': pos_to_drink[i],
            'music': pos_to_music[i],
            'pet': pos_to_pet[i],
            'destination': pos_to_dest[i]
        })
    # Find lizard owner nationality
    lizard_pos = m[pet_pos[pet_idx['Lizard']]].as_long()
    lizard_nat = pos_to_nat[lizard_pos]
    print("STATUS: sat")
    print("solution:", solution)
    print("lizard_owner:", lizard_nat)
elif result == unsat:
    print("STATUS: unsat")
    print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")