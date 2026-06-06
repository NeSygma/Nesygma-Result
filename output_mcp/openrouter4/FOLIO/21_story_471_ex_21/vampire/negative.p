% Negative file: check if premises entail the NEGATED conclusion
% Negated conclusion: ~((cute(rockie) & calm(rockie)) => (skittish(rockie) & turtle(rockie)))
% Which simplifies to: (cute(rockie) & calm(rockie)) & ~(skittish(rockie) & turtle(rockie))
% Which is: (cute(rockie) & calm(rockie)) & (~skittish(rockie) | ~turtle(rockie))

fof(distinct, axiom, (rockie != dummy_entity)).

% Premise 1: All rabbits that can be spotted near the campus are cute.
fof(premise_1, axiom, ! [X] : ((rabbit(X) & spotted(X)) => cute(X))).

% Premise 2: Some turtles can be spotted near the campus.
fof(premise_2, axiom, ? [X] : (turtle(X) & spotted(X))).

% Premise 3: The only animals that can be spotted near the campus are rabbits and squirrels.
fof(premise_3, axiom, ! [X] : (spotted(X) => (rabbit(X) | squirrel(X)))).

% Premise 4: If something is skittish, then it is not calm.
fof(premise_4, axiom, ! [X] : (skittish(X) => ~calm(X))).

% Premise 5: All the squirrels that can be spotted near the campus are skittish.
fof(premise_5, axiom, ! [X] : ((squirrel(X) & spotted(X)) => skittish(X))).

% Premise 6: Rockie can be spotted near the campus, and it is calm.
fof(premise_6, axiom, spotted(rockie) & calm(rockie)).

% Negated conclusion: (cute(rockie) & calm(rockie)) & (~skittish(rockie) | ~turtle(rockie))
fof(goal_negated, conjecture, (cute(rockie) & calm(rockie)) & (~skittish(rockie) | ~turtle(rockie))).