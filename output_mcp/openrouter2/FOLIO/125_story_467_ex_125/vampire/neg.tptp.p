fof(pet_of_rock, axiom, pet_of_peter(rock)).
fof(bird_fly_rule, axiom, ! [X] : ((pet_of_peter(X) & bird(X)) => fly(X))).
fof(mammal_animal_rule, axiom, ! [X] : ((pet_of_peter(X) & mammal(X)) => animal(X))).
fof(animal_breathe_rule, axiom, ! [X] : ((pet_of_peter(X) & animal(X)) => breathe(X))).
fof(fly_wing_rule, axiom, ! [X] : ((pet_of_peter(X) & fly(X)) => winged(X))).
fof(monkey_mammal_rule, axiom, ! [X] : (monkey(X) => mammal(X))).
fof(pet_monkey_or_bird_rule, axiom, ! [X] : (pet_of_peter(X) => (monkey(X) | bird(X)))).
fof(rock_disjunction, axiom, fly(rock) | bird(rock) | ~breathe(rock)).
fof(conjecture, conjecture, ~monkey(rock)).