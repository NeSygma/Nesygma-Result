tff(campus_type, type, campus: $i).
tff(rockie_type, type, rockie: $i).

tff(can_be_spotted_near_type, type, can_be_spotted_near: ($i * $i) > $o).
tff(cute_type, type, cute: $i > $o).
tff(turtle_type, type, turtle: $i > $o).
tff(rabbit_type, type, rabbit: $i > $o).
tff(squirrel_type, type, squirrel: $i > $o).
tff(skittish_type, type, skittish: $i > $o).
tff(calm_type, type, calm: $i > $o).

% Premise 1: All rabbits that can be spotted near the campus are cute.
fof(premise1, axiom, ! [X: $i] : ((rabbit(X) & can_be_spotted_near(X, campus)) => cute(X))).

% Premise 2: Some turtles can be spotted near the campus.
fof(premise2, axiom, ? [X: $i] : (turtle(X) & can_be_spotted_near(X, campus))).

% Premise 3: The only animals that can be spotted near the campus are rabbits and squirrels.
fof(premise3, axiom, ! [X: $i] : (can_be_spotted_near(X, campus) => (rabbit(X) | squirrel(X)))).

% Premise 4: If something is skittish, then it is not calm.
fof(premise4, axiom, ! [X: $i] : (skittish(X) => ~calm(X))).

% Premise 5: All the squirrels that can be spotted near the campus are skittish.
fof(premise5, axiom, ! [X: $i] : ((squirrel(X) & can_be_spotted_near(X, campus)) => skittish(X))).

% Premise 6: Rockie can be spotted near the campus, and it is calm.
fof(premise6a, axiom, can_be_spotted_near(rockie, campus)).
fof(premise6b, axiom, calm(rockie)).

% Conclusion to evaluate: Rockie is a turtle or cute.
fof(conclusion, conjecture, turtle(rockie) | cute(rockie)).