fof(p1, axiom, ! [X] : (hydrocarbon(X) => organic_compound(X))).
fof(p2, axiom, ! [X] : (alkane(X) => hydrocarbon(X))).
fof(p3, axiom, ! [X] : (organic_compound(X) => chemical_compound(X))).
fof(p4, axiom, ! [X] : (organic_compound(X) => contains_carbon(X))).
fof(p5, axiom, ! [X] : (chemical_compound(X) => ~contains_only_one_element(X))).
fof(p6, axiom, ! [X] : ((chemical_compound(X) & contains_only_one_element(X)) | (~chemical_compound(X) & ~contains_only_one_element(X)))).

fof(goal, conjecture, ~(! [X] : ((contains_only_one_element(X) | contains_carbon(X)) => (~chemical_compound(X) & ~alkane(X))))).