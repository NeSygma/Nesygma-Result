fof(premise1, axiom, ! [X] : (hydrocarbon(X) => organic(X)).
fof(premise2, axiom, ! [X] : (alkane(X) => hydrocarbon(X)).
fof(premise3, axiom, ! [X] : (organic(X) => chemical(X)).
fof(premise4, axiom, ! [X] : (organic(X) => containsCarbon(X)).
fof(premise5, axiom, ! [X] : (chemical(X) => ~containsOnlyOneElement(X)).
fof(premise6, axiom, (chemical(mixture) => containsOnlyOneElement(mixture))).
fof(neg_conclusion, conjecture, ~(alkane(mixture) & containsCarbon(mixture))).