% Negative run: negated conclusion as conjecture
% Negation of: Walden contains knowledge.

fof(premise_1, axiom, ! [X] : (book(X) => contains_knowledge(X))).
fof(premise_2, axiom, ! [X, Y] : ((person(X) & book(Y) & reads(X, Y)) => gains_knowledge(X))).
fof(premise_3, axiom, ! [X] : (gains_knowledge(X) => becomes_smarter(X))).
fof(premise_4, axiom, person(harry) & book(walden) & reads(harry, walden)).

fof(goal_neg, conjecture, ~contains_knowledge(walden)).