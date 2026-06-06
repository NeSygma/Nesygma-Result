fof(pet_of_rock, axiom, pet_of_peter(rock)).
fof(disjunction, axiom, (can_fly(rock) | bird(rock) | ~can_breathe(rock))).
fof(rule1, axiom, ! [X] : ((pet_of_peter(X) & mammal(X)) => animal(X))).
fof(rule2, axiom, ! [X] : (monkey(X) => mammal(X))).
fof(rule3, axiom, ! [X] : (pet_of_peter(X) => (monkey(X) | bird(X)))).
fof(rule4, axiom, ! [X] : ((pet_of_peter(X) & bird(X)) => can_fly(X))).
fof(rule5, axiom, ! [X] : ((pet_of_peter(X) & animal(X)) => can_breathe(X))).
fof(rule6, axiom, ! [X] : ((pet_of_peter(X) & can_fly(X)) => has_wings(X))).
fof(conjecture, conjecture, ~has_wings(rock)).