% Negative version: Rock does NOT have wings
fof(premise_1, axiom, ! [X] : ((pet(X) & mammal(X)) => animal(X))).
fof(premise_2, axiom, ! [X] : (monkey(X) => mammal(X))).
fof(premise_3, axiom, ! [X] : (pet(X) => (monkey(X) | bird(X)))).
fof(premise_4, axiom, ! [X] : ((pet(X) & bird(X)) => fly(X))).
fof(premise_5, axiom, ! [X] : ((animal(X) & pet(X)) => breathe(X))).
fof(premise_6, axiom, ! [X] : ((pet(X) & fly(X)) => wings(X))).
fof(premise_7, axiom, pet(rock)).
fof(premise_8, axiom, (fly(rock) | bird(rock) | ~breathe(rock))).
fof(goal, conjecture, ~wings(rock)).