fof(premise1, axiom, ! [X] : ((pet(X) & mammal(X)) => animal(X))).
fof(premise2, axiom, ! [X] : (monkey(X) => mammal(X))).
fof(premise3, axiom, ! [X] : (pet(X) => (monkey(X) | bird(X)))).
fof(premise4, axiom, ! [X] : ((bird(X) & pet(X)) => can_fly(X))).
fof(premise5, axiom, ! [X] : ((animal(X) & pet(X)) => breathe(X))).
fof(premise6, axiom, ! [X] : ((pet(X) & can_fly(X)) => has_wings(X))).
fof(premise7, axiom, pet(rock)).
fof(premise8, axiom, (can_fly(rock) | bird(rock) | ~breathe(rock))).
fof(goal, conjecture, has_wings(rock)).