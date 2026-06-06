fof(p1, axiom, ! [X] : (romance(X) => indo_european(X))).
fof(p2, axiom, language_family(romance_languages)).
fof(p3, axiom, ! [X] : (romance(X) => in_family(X, romance_languages))).
fof(p4, axiom, ! [X, Y, F] : ((in_family(X, F) & in_family(Y, F) & language_family(F)) => related(X, Y))).
fof(p5, axiom, romance(french)).
fof(p6, axiom, romance(spanish)).
fof(p7, axiom, related(german, spanish)).
fof(p8, axiom, ! [X] : ~related(basque, X)).
fof(goal, conjecture, romance(basque)).