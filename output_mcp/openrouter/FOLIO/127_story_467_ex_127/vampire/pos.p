% Positive test: prove ~has_wings(rock)
fof(pet_mammal_animal, axiom, ! [X] : ((pet(X) & mammal(X)) => animal(X))).
fof(monkey_mammal, axiom, ! [X] : (monkey(X) => mammal(X))).
fof(pet_monkey_or_bird, axiom, ! [X] : (pet(X) => (monkey(X) | bird(X)))).
fof(pet_bird_fly, axiom, ! [X] : ((pet(X) & bird(X)) => can_fly(X))).
fof(pet_animal_breathe, axiom, ! [X] : ((pet(X) & animal(X)) => breathe(X))).
fof(pet_fly_wings, axiom, ! [X] : ((pet(X) & can_fly(X)) => has_wings(X))).
fof(rock_is_pet, axiom, pet(rock)).
fof(rock_disjunction, axiom, (can_fly(rock) | bird(rock) | ~breathe(rock))).
fof(goal, conjecture, ~has_wings(rock)).