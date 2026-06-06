% Positive version: original conclusion as conjecture
% Conclusion: If Rockie is cute and calm, then Rockie is a skittish turtle.
% Formalized: (cute(rockie) & calm(rockie)) => (skittish(rockie) & turtle(rockie))

fof(distinct_animals, axiom, (rabbit != turtle & rabbit != squirrel & turtle != squirrel)).

% All rabbits that can be spotted near the campus are cute.
fof(rule1, axiom, ! [X] : ((rabbit(X) & spotted(X)) => cute(X))).

% Some turtles can be spotted near the campus.
fof(rule2, axiom, ? [X] : (turtle(X) & spotted(X))).

% The only animals that can be spotted near the campus are rabbits and squirrels.
fof(rule3, axiom, ! [X] : (spotted(X) => (rabbit(X) | squirrel(X)))).

% If something is skittish, then it is not calm.
fof(rule4, axiom, ! [X] : (skittish(X) => ~calm(X))).

% All the squirrels that can be spotted near the campus are skittish.
fof(rule5, axiom, ! [X] : ((squirrel(X) & spotted(X)) => skittish(X))).

% Rockie can be spotted near the campus, and it is calm.
fof(fact1, axiom, spotted(rockie)).
fof(fact2, axiom, calm(rockie)).

% Conclusion: If Rockie is cute and calm, then Rockie is a skittish turtle.
fof(goal, conjecture, ((cute(rockie) & calm(rockie)) => (skittish(rockie) & turtle(rockie)))).