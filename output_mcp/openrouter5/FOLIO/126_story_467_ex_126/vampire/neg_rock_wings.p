% Negative file: negated claim as conjecture
% All of Peter's pets that are mammals are also animals.
fof(axiom1, axiom, ! [X] : ((pet_of_peter(X) & mammal(X)) => animal(X))).

% All monkeys are mammals.
fof(axiom2, axiom, ! [X] : (monkey(X) => mammal(X))).

% Peter's pets are all either monkeys or birds.
fof(axiom3, axiom, ! [X] : (pet_of_peter(X) => (monkey(X) | bird(X)))).

% Peter's birds can fly.
fof(axiom4, axiom, ! [X] : ((pet_of_peter(X) & bird(X)) => can_fly(X))).

% All animals that are Peter's pets can breathe.
fof(axiom5, axiom, ! [X] : ((animal(X) & pet_of_peter(X)) => can_breathe(X))).

% If Peter's pet can fly, then it has wings.
fof(axiom6, axiom, ! [X] : ((pet_of_peter(X) & can_fly(X)) => has_wings(X))).

% Rock is Peter's pet.
fof(axiom7, axiom, pet_of_peter(rock)).

% Rock can fly, or Rock is a bird, or Rock cannot breathe.
fof(axiom8, axiom, (can_fly(rock) | bird(rock) | ~can_breathe(rock))).

% Negated conclusion: Rock does NOT have wings.
fof(goal_neg, conjecture, ~has_wings(rock)).