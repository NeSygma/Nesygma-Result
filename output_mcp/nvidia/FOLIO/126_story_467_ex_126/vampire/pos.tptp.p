fof(prem1, axiom, ! [X] : ((pet(X) & mammal(X)) => animal(X)) ).
fof(prem2, axiom, ! [X] : (monkey(X) => mammal(X)) ).
fof(prem3, axiom, ! [X] : (pet(X) => (monkey(X) | bird(X))) ).
fof(prem4, axiom, ! [X] : ((bird(X) & pet(X)) => can_fly(X)) ).
fof(prem5, axiom, ! [X] : ((animal(X) & pet(X)) => breathe(X)) ).
fof(prem6, axiom, ! [X] : ((pet(X) & can_fly(X)) => has_wings(X)) ).
fof(fact_pet_rock, axiom, pet(rock) ).
fof(disjunction, axiom, (can_fly(rock) | bird(rock) | ~breathe(rock)) ).
fof(goal, conjecture, has_wings(rock) ).