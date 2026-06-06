fof(pet_mammal_animal, axiom, ! [X] : ((pet_of_peter(X) & mammal(X)) => animal(X))).
fof(monkey_mammal, axiom, ! [X] : (monkey(X) => mammal(X))).
fof(pet_monkey_or_bird, axiom, ! [X] : (pet_of_peter(X) => (monkey(X) | bird(X)))).
fof(peter_bird_fly, axiom, ! [X] : ((pet_of_peter(X) & bird(X)) => can_fly(X))).
fof(pet_animal_breathe, axiom, ! [X] : ((pet_of_peter(X) & animal(X)) => can_breathe(X))).
fof(fly_wings, axiom, ! [X] : ((pet_of_peter(X) & can_fly(X)) => has_wings(X))).
fof(rock_pet, axiom, pet_of_peter(rock)).
fof(rock_disjunct, axiom, (can_fly(rock) | bird(rock) | ~can_breathe(rock))).
fof(goal, conjecture, has_wings(rock)).