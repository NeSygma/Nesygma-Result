% Positive version: original claim as conjecture
% Premises:

% All rabbits that can be spotted near the campus are cute.
fof(rabbit_cute, axiom,
    ! [X] : ((rabbit(X) & spotted_near_campus(X)) => cute(X))).

% Some turtles can be spotted near the campus.
fof(some_turtle_spotted, axiom,
    ? [X] : (turtle(X) & spotted_near_campus(X))).

% The only animals that can be spotted near the campus are rabbits and squirrels.
fof(only_rabbits_squirrels, axiom,
    ! [X] : (spotted_near_campus(X) => (rabbit(X) | squirrel(X)))).

% If something is skittish, then it is not calm.
fof(skittish_not_calm, axiom,
    ! [X] : (skittish(X) => ~calm(X))).

% All the squirrels that can be spotted near the campus are skittish.
fof(squirrel_skittish, axiom,
    ! [X] : ((squirrel(X) & spotted_near_campus(X)) => skittish(X))).

% Rockie can be spotted near the campus, and it is calm.
fof(rockie_spotted_calm, axiom,
    (spotted_near_campus(rockie) & calm(rockie))).

% Distinctness: Rockie is a distinct individual (no other constants to distinguish from)
% No explicit distinctness needed for a single constant.

% Conclusion: Rockie is not a turtle.
fof(goal, conjecture,
    ~turtle(rockie)).