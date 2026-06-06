% Negative version: negated claim as conjecture
% It is NOT the case that (the mixture is an alkane and contains carbon).

fof(premise_1, axiom, ! [X] : (hydrocarbon(X) => organic_compound(X))).
fof(premise_2, axiom, ! [X] : (alkane(X) => hydrocarbon(X))).
fof(premise_3, axiom, ! [X] : (organic_compound(X) => chemical_compound(X))).
fof(premise_4, axiom, ! [X] : (organic_compound(X) => contains_carbon(X))).
fof(premise_5, axiom, ! [X] : (chemical_compound(X) => ~contains_only_one_element(X))).
fof(premise_6, axiom, ! [X] : (mixture(X) => ((chemical_compound(X) & contains_only_one_element(X)) | (~chemical_compound(X) & ~contains_only_one_element(X))))).
fof(premise_7, axiom, ! [X] : (((chemical_compound(X) & contains_only_one_element(X)) | (~chemical_compound(X) & ~contains_only_one_element(X))) => mixture(X))).

fof(distinct, axiom, mixture(m)).

fof(goal, conjecture, ~(alkane(m) & contains_carbon(m))).