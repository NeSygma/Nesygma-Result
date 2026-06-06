% Problem: Rockie is a turtle or cute (negated)
% Premises and negated conjecture

fof(premise_1, axiom, ! [X] : ((rabbit(X) & spotted_near_campus(X)) => cute(X))).
fof(premise_2, axiom, ? [X] : (turtle(X) & spotted_near_campus(X))).
fof(premise_3, axiom, ! [X] : (spotted_near_campus(X) => (rabbit(X) | squirrel(X)))).
fof(premise_4, axiom, ! [X] : (skittish(X) => ~calm(X))).
fof(premise_5, axiom, ! [X] : ((squirrel(X) & spotted_near_campus(X)) => skittish(X))).
fof(premise_6, axiom, spotted_near_campus(rockie) & calm(rockie)).

% Negated conclusion: Rockie is NOT a turtle AND NOT cute
fof(goal_neg, conjecture, ~(turtle(rockie) | cute(rockie))). % Equivalent to: ~turtle(rockie) & ~cute(rockie)