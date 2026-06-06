fof(premise1, axiom, ! [X] : (horse(X) => hoofed(X))).
fof(premise2, axiom, ! [X] : (human(X) => ~hoofed(X))).
fof(conjecture, conjecture, ? [X] : (human(X) & horse(X))).