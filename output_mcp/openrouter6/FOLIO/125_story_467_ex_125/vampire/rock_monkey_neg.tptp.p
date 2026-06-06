fof(premise1, axiom, ! [X] : ((pet_of_peter(X) & mammal(X)) => animal(X))).
fof(premise2, axiom, ! [X] : (monkey(X) => mammal(X))).
fof(premise3, axiom, ! [X] : (pet_of_peter(X) => (monkey(X) | bird(X)))).
fof(premise4, axiom, ! [X] : ((bird(X) & pet_of_peter(X)) => can_fly(X))).
fof(premise5, axiom, ! [X] : ((animal(X) & pet_of_peter(X)) => can_breathe(X))).
fof(premise6, axiom, ! [X] : ((pet_of_peter(X) & can_fly(X)) => has_wings(X))).
fof(premise7, axiom, pet_of_peter(rock)).
fof(premise8, axiom, can_fly(rock) | bird(rock) | ~can_breathe(rock)).
fof(conclusion, conjecture, ~monkey(rock)).