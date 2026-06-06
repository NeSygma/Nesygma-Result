% Positive version: original claim as conjecture
% Predicates:
%   istanbul_plate(X) - X's plate is from Istanbul
%   begins_with_34(X) - X's plate begins with 34
%   begins_with_35(X) - X's plate begins with 35

fof(premise_1, axiom, ! [X] : (istanbul_plate(X) => begins_with_34(X))).
fof(premise_2, axiom, ! [X] : (~begins_with_34(X) => ~istanbul_plate(X))).
fof(premise_3, axiom, istanbul_plate(joe)).
fof(premise_4, axiom, begins_with_35(tom)).
fof(premise_5, axiom, ! [X] : (begins_with_35(X) => ~begins_with_34(X))).

fof(goal, conjecture, begins_with_34(joe)).