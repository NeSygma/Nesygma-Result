% Positive version: original conclusion as conjecture
% Conclusion: Rockie is a turtle or cute.

% Predicates:
% spotted(X) - X can be spotted near the campus
% rabbit(X) - X is a rabbit
% turtle(X) - X is a turtle
% squirrel(X) - X is a squirrel
% cute(X) - X is cute
% skittish(X) - X is skittish
% calm(X) - X is calm

% Constants:
% rockie

% All rabbits that can be spotted near the campus are cute.
fof(axiom1, axiom, ! [X] : ((rabbit(X) & spotted(X)) => cute(X))).

% Some turtles can be spotted near the campus.
fof(axiom2, axiom, ? [X] : (turtle(X) & spotted(X))).

% The only animals that can be spotted near the campus are rabbits and squirrels.
fof(axiom3, axiom, ! [X] : (spotted(X) => (rabbit(X) | squirrel(X)))).

% If something is skittish, then it is not calm.
fof(axiom4, axiom, ! [X] : (skittish(X) => ~calm(X))).

% All the squirrels that can be spotted near the campus are skittish.
fof(axiom5, axiom, ! [X] : ((squirrel(X) & spotted(X)) => skittish(X))).

% Rockie can be spotted near the campus, and it is calm.
fof(axiom6, axiom, spotted(rockie) & calm(rockie)).

% Conclusion: Rockie is a turtle or cute.
fof(conclusion, conjecture, (turtle(rockie) | cute(rockie))).