from z3 import *

# Define attributes
nationalities = ['American', 'Brazilian', 'Canadian', 'Dutch', 'Egyptian', 'French', 'German', 'Hungarian']
professions = ['Architect', 'Biologist', 'Chemist', 'Doctor', 'Engineer', 'Lawyer', 'Musician', 'Pilot']
cars = ['Audi', 'BMW', 'Ford', 'Honda', 'Mercedes', 'Nissan', 'Toyota', 'Volvo']
drinks = ['Coffee', 'Juice', 'Milk', 'Soda', 'Tea', 'Water', 'Wine', 'Whiskey']
music = ['Blues', 'Classical', 'Folk', 'Jazz', 'Pop', 'Rap', 'Reggae', 'Rock']
pets = ['Cat', 'Dog', 'Fish', 'Hamster', 'Lizard', 'Parrot', 'Rabbit', 'Snake']
destinations = ['Bali', 'Dubai', 'London', 'New York', 'Paris', 'Rome', 'Sydney', 'Tokyo']

def get_vars(name, count):
    return [Int(f"{name}_{i}") for i in range(count)]

nat = get_vars('nat', 8)
prof = get_vars('prof', 8)
car = get_vars('car', 8)
drink = get_vars('drink', 8)
music_genre = get_vars('music', 8)
pet = get_vars('pet', 8)
dest = get_vars('dest', 8)

solver = Solver()

# Domains: 0-7
for i in range(8):
    solver.add(nat[i] >= 0, nat[i] < 8)
    solver.add(prof[i] >= 0, prof[i] < 8)
    solver.add(car[i] >= 0, car[i] < 8)
    solver.add(drink[i] >= 0, drink[i] < 8)
    solver.add(music_genre[i] >= 0, music_genre[i] < 8)
    solver.add(pet[i] >= 0, pet[i] < 8)
    solver.add(dest[i] >= 0, dest[i] < 8)

# All distinct
solver.add(Distinct(nat))
solver.add(Distinct(prof))
solver.add(Distinct(car))
solver.add(Distinct(drink))
solver.add(Distinct(music_genre))
solver.add(Distinct(pet))
solver.add(Distinct(dest))

def get_idx(attr_list, val):
    return attr_list.index(val)

# Constraints
solver.add(drink[3] == get_idx(drinks, 'Milk'))
solver.add(nat[3] == get_idx(nationalities, 'Hungarian'))
for i in range(8):
    solver.add(Implies(nat[i] == get_idx(nationalities, 'American'), prof[i] == get_idx(professions, 'Lawyer')))
    solver.add(Implies(car[i] == get_idx(cars, 'BMW'), prof[i] == get_idx(professions, 'Biologist')))
    solver.add(Implies(nat[i] == get_idx(nationalities, 'Canadian'), pet[i] == get_idx(pets, 'Snake')))
    solver.add(Implies(music_genre[i] == get_idx(music, 'Classical'), car[i] == get_idx(cars, 'Audi')))
    solver.add(Implies(nat[i] == get_idx(nationalities, 'German'), drink[i] == get_idx(drinks, 'Coffee')))
    solver.add(Implies(dest[i] == get_idx(destinations, 'Tokyo'), prof[i] == get_idx(professions, 'Chemist')))

for i in range(7):
    solver.add(Implies(prof[i] == get_idx(professions, 'Engineer'), prof[i+1] == get_idx(professions, 'Lawyer')))

for i in range(8):
    # 10. The Dog owner lives next to the Volvo driver
    is_dog_owner = (pet[i] == get_idx(pets, 'Dog'))
    has_volvo_neighbor = Or(
        And(i > 0, car[i-1] == get_idx(cars, 'Volvo')),
        And(i < 7, car[i+1] == get_idx(cars, 'Volvo'))
    )
    solver.add(Implies(is_dog_owner, has_volvo_neighbor))
    
    # 11. The Rock music listener lives next to the Pop music listener
    is_rock = (music_genre[i] == get_idx(music, 'Rock'))
    has_pop_neighbor = Or(
        And(i > 0, music_genre[i-1] == get_idx(music, 'Pop')),
        And(i < 7, music_genre[i+1] == get_idx(music, 'Pop'))
    )
    solver.add(Implies(is_rock, has_pop_neighbor))
    
    # 12. The person going to Paris lives next to the Fish owner
    is_paris = (dest[i] == get_idx(destinations, 'Paris'))
    has_fish_neighbor = Or(
        And(i > 0, pet[i-1] == get_idx(pets, 'Fish')),
        And(i < 7, pet[i+1] == get_idx(pets, 'Fish'))
    )
    solver.add(Implies(is_paris, has_fish_neighbor))
    
    # 13. The Pilot lives in an even-numbered suite (2, 4, 6, 8 -> indices 1, 3, 5, 7)
    solver.add(Implies(prof[i] == get_idx(professions, 'Pilot'), Or(i == 1, i == 3, i == 5, i == 7)))
    
    # 15. The Ford driver has a neighbor who drinks Tea
    is_ford = (car[i] == get_idx(cars, 'Ford'))
    has_tea_neighbor = Or(
        And(i > 0, drink[i-1] == get_idx(drinks, 'Tea')),
        And(i < 7, drink[i+1] == get_idx(drinks, 'Tea'))
    )
    solver.add(Implies(is_ford, has_tea_neighbor))
    
    # 16. The Nissan driver does not live in suite #1 or #8 (indices 0 or 7)
    solver.add(Implies(car[i] == get_idx(cars, 'Nissan'), And(i != 0, i != 7)))

# 14. The Wine drinker's suite is to the right of the Coffee drinker's suite
# Use a constraint that for all i, if drink[i] == Wine, there exists j < i such that drink[j] == Coffee
for i in range(8):
    solver.add(Implies(drink[i] == get_idx(drinks, 'Wine'), Or([drink[j] == get_idx(drinks, 'Coffee') for j in range(i)])))

# 17. The Jazz listener's suite number is less than the Blues listener's suite number
for i in range(8):
    solver.add(Implies(music_genre[i] == get_idx(music, 'Jazz'), Or([music_genre[j] == get_idx(music, 'Blues') for j in range(i+1, 8)])))

# 18. The Dutch person lives in suite #1 (index 0)
solver.add(nat[0] == get_idx(nationalities, 'Dutch'))

# Solve
if solver.check() == sat:
    print("STATUS: sat")
    m = solver.model()
    lizard_owner_nat = ""
    for i in range(8):
        n_idx = m[nat[i]].as_long()
        p_idx = m[pet[i]].as_long()
        if p_idx == get_idx(pets, 'Lizard'):
            lizard_owner_nat = nationalities[n_idx]
        print(f"Suite {i+1}: {nationalities[n_idx]}, {professions[m[prof[i]].as_long()]}, {cars[m[car[i]].as_long()]}, {drinks[m[drink[i]].as_long()]}, {music[m[music_genre[i]].as_long()]}, {pets[p_idx]}, {destinations[m[dest[i]].as_long()]}")
    print(f"Lizard owner: {lizard_owner_nat}")
else:
    print("STATUS: unsat")