fof(pet_mammal_animal, axiom, ! [X] : ((pet_of_peter(X) & mammal(X)) => animal(X))).
fof(monkey_mammal, axiom, ! [X] : (monkey(X) => mammal(X))).
fof(pet_monkey_or_bird, axiom, ! [X] : (pet_of_peter(X) => (monkey(X) | bird(X)))).
fof(bird_can_fly, axiom, ! [X] : (pet_of_peter(X) & bird(X) => can_fly(X))).
fof(animal_pet_can_breathe, axiom, ! [X] : (pet_of_peter(X) & animal(X) => can_breathe(X))).
fof(pet_can_fly_has_wings, axiom, ! [X] : (pet_of_peter(X) & can_fly(X) => has_wings(X))).
fof(rock_is_pet, axiom, pet_of_peter(rock)).
fof(rock_fly_or_bird_or_not_breathe, axiom, can_fly(rock) | bird(rock) | ~can_breathe(rock)).
fof(conclusion_negation, conjecture, has_wings(rock)).