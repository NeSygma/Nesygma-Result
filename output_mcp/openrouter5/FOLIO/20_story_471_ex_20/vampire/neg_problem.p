% Negative version: negated conclusion as conjecture
% Premises:

% All rabbits that can be spotted near the campus are cute.
fof(rabbit_cute, axiom, ! [X] : ((rabbit(X) & spotted(X)) => cute(X))).

% Some turtles can be spotted near the campus.
fof(some_turtle_spotted, axiom, ? [X] : (turtle(X) & spotted(X))).

% The only animals that can be spotted near the campus are rabbits and squirrels.
fof(only_rabbits_squirrels, axiom, ! [X] : (spotted(X) => (rabbit(X) | squirrel(X)))).

% If something is skittish, then it is not calm.
fof(skittish_not_calm, axiom, ! [X] : (skittish(X) => ~calm(X))).

% All the squirrels that can be spotted near the campus are skittish.
fof(squirrel_spotted_skittish, axiom, ! [X] : ((squirrel(X) & spotted(X)) => skittish(X))).

% Rockie can be spotted near the campus, and it is calm.
fof(rockie_spotted, axiom, spotted(rockie)).
fof(rockie_calm, axiom, calm(rockie)).

% Negated conclusion: ~((~(turtle(rockie) & squirrel(rockie))) => (cute(rockie) | skittish(rockie)))
% This is equivalent to: (~(turtle(rockie) & squirrel(rockie))) & ~(cute(rockie) | skittish(rockie))
% i.e., (~(turtle(rockie) & squirrel(rockie))) & ~cute(rockie) & ~skittish(rockie)
fof(neg_conclusion, conjecture, (~(turtle(rockie) & squirrel(rockie))) & ~cute(rockie) & ~skittish(rockie)).