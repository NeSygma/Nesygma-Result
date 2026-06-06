% Positive file: original claim as conjecture
% Premises:

% All of Peter's pets that are mammals are also animals.
fof(premise1, axiom, ! [X] : ((pet_of(X, peter) & mammal(X)) => animal(X))).

% All monkeys are mammals.
fof(premise2, axiom, ! [X] : (monkey(X) => mammal(X))).

% Peter's pets are all either monkeys or birds.
fof(premise3, axiom, ! [X] : (pet_of(X, peter) => (monkey(X) | bird(X)))).

% Peter's birds can fly.
fof(premise4, axiom, ! [X] : ((pet_of(X, peter) & bird(X)) => can_fly(X))).

% All animals that are Peter's pets can breathe.
fof(premise5, axiom, ! [X] : ((animal(X) & pet_of(X, peter)) => can_breathe(X))).

% If Peter's pet can fly, then it has wings.
fof(premise6, axiom, ! [X] : ((pet_of(X, peter) & can_fly(X)) => has_wings(X))).

% Rock is Peter's pet.
fof(premise7, axiom, pet_of(rock, peter)).

% Rock can fly, or Rock is a bird, or Rock cannot breathe.
fof(premise8, axiom, (can_fly(rock) | bird(rock) | ~can_breathe(rock))).

% Distinctness: no extra constants beyond rock and peter, but ensure no unwanted collapse
fof(distinct, axiom, rock != peter).

% Conclusion: Rock is a monkey.
fof(goal, conjecture, monkey(rock)).