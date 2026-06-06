fof(premise_1, axiom, ! [X] : ((pet_of_peter(X) & mammal(X)) => animal(X))).
fof(premise_2, axiom, ! [X] : (monkey(X) => mammal(X))).
fof(premise_3, axiom, ! [X] : (pet_of_peter(X) => (monkey(X) | bird(X)))).
fof(premise_4, axiom, ! [X] : ((pet_of_peter(X) & bird(X)) => can_fly(X))).
fof(premise_5, axiom, ! [X] : ((animal(X) & pet_of_peter(X)) => can_breathe(X))).
fof(premise_6, axiom, ! [X] : ((pet_of_peter(X) & can_fly(X)) => has_wings(X))).
fof(premise_7, axiom, pet_of_peter(rock)).
fof(premise_8, axiom, (can_fly(rock) | bird(rock) | ~can_breathe(rock))).
fof(distinct, axiom, rock != a & rock != b & rock != c).
fof(goal, conjecture, ~has_wings(rock)).