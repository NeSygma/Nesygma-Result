fof(pet_rock, axiom, pet(rock)).
fof(rule1, axiom, ![X] : ((pet(X) & mammal(X)) => animal(X))).
fof(rule2, axiom, ![X] : (monkey(X) => mammal(X))).
fof(rule3, axiom, ![X] : (pet(X) => (monkey(X) | bird(X)))).
fof(rule4, axiom, ![X] : ((pet(X) & bird(X)) => fly(X))).
fof(rule5, axiom, ![X] : ((pet(X) & animal(X)) => breathe(X))).
fof(rule6, axiom, ![X] : ((pet(X) & fly(X)) => wings(X))).
fof(disj, axiom, (fly(rock) | bird(rock) | ~breathe(rock))).
fof(conjecture, conjecture, ~wings(rock)).