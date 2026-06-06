fof(prem1, axiom, ! [X] : (hydrocarbon(X) => organic(X))).
fof(prem2, axiom, ! [X] : (alkane(X) => hydrocarbon(X))).
fof(prem3, axiom, ! [X] : (organic(X) => chemical(X))).
fof(prem4, axiom, ! [X] : (organic(X) => contains_carbon(X))).
fof(prem5, axiom, ! [X] : (chemical(X) => ~only_one_element(X))).
fof(prem6a, axiom, chemical(mixture) => only_one_element(mixture)).
fof(prem6b, axiom, only_one_element(mixture) => chemical(mixture)).
fof(conjecture, conjecture, contains_carbon(mixture)).