% Positive file: original claim as conjecture
% Claim: Rock does not have wings.

% Predicates:
% pet_of(X,Y) - X is a pet of Y
% mammal(X) - X is a mammal
% animal(X) - X is an animal
% monkey(X) - X is a monkey
% bird(X) - X is a bird
% can_fly(X) - X can fly
% can_breathe(X) - X can breathe
% has_wings(X) - X has wings

% Constants:
% peter - Peter
% rock - Rock

% Distinctness
fof(distinct, axiom, rock != peter).

% Premise 1: All of Peter's pets that are mammals are also animals.
fof(premise1, axiom, ! [X] : ((pet_of(X, peter) & mammal(X)) => animal(X))).

% Premise 2: All monkeys are mammals.
fof(premise2, axiom, ! [X] : (monkey(X) => mammal(X))).

% Premise 3: Peter's pets are all either monkeys or birds.
fof(premise3, axiom, ! [X] : (pet_of(X, peter) => (monkey(X) | bird(X)))).

% Premise 4: Peter's birds can fly.
fof(premise4, axiom, ! [X] : ((pet_of(X, peter) & bird(X)) => can_fly(X))).

% Premise 5: All animals that are Peter's pets can breathe.
fof(premise5, axiom, ! [X] : ((animal(X) & pet_of(X, peter)) => can_breathe(X))).

% Premise 6: If Peter's pet can fly, then it has wings.
fof(premise6, axiom, ! [X] : ((pet_of(X, peter) & can_fly(X)) => has_wings(X))).

% Premise 7: Rock is Peter's pet.
fof(premise7, axiom, pet_of(rock, peter)).

% Premise 8: Rock can fly, or Rock is a bird, or Rock cannot breathe.
fof(premise8, axiom, (can_fly(rock) | bird(rock) | ~can_breathe(rock))).

% Conclusion: Rock does not have wings.
fof(conclusion, conjecture, ~has_wings(rock)).