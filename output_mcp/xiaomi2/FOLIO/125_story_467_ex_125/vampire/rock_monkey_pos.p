fof(premise_1, axiom, ! [X] : ((pet(X) & mammal(X)) => animal(X))).
fof(premise_2, axiom, ! [X] : (monkey(X) => mammal(X))).
fof(premise_3, axiom, ! [X] : (pet(X) => (monkey(X) | bird(X)))).
fof(premise_4, axiom, ! [X] : ((pet(X) & bird(X)) => can_fly(X))).
fof(premise_5, axiom, ! [X] : ((animal(X) & pet(X)) => can_breathe(X))).
fof(premise_6, axiom, ! [X] : ((pet(X) & can_fly(X)) => has_wings(X))).
fof(premise_7, axiom, pet(rock)).
fof(premise_8, axiom, (can_fly(rock) | bird(rock) | ~can_breathe(rock))).
fof(goal, conjecture, monkey(rock)).