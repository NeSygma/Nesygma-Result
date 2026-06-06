fof(p1, axiom, ! [X] : (hydrocarbon(X) => organic_compound(X))).
fof(p2, axiom, ! [X] : (alkane(X) => hydrocarbon(X))).
fof(p3, axiom, ! [X] : (organic_compound(X) => chemical_compound(X))).
fof(p4, axiom, ! [X] : (organic_compound(X) => contains_carbon(X))).
fof(p5, axiom, ! [X] : (chemical_compound(X) => ~contains_only_one_element(X))).
fof(p6, axiom, ((chemical_compound(the_mixture) & contains_only_one_element(the_mixture)) | (~chemical_compound(the_mixture) & ~contains_only_one_element(the_mixture)))).
fof(goal, conjecture, ~(alkane(the_mixture) & contains_carbon(the_mixture))).