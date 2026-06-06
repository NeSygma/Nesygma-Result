fof(man_michael, axiom, man(michael)).
fof(man_peter, axiom, man(peter)).
fof(taller_peter_michael, axiom, taller(peter, michael)).
fof(transitivity, axiom, ! [X, Y, Z] : ((taller(X, Y) & taller(Y, Z)) => taller(X, Z))).
fof(michael_class_rule, axiom, ! [X] : ((in_class(X, michael_class) & X != michael) => taller(michael, X))).
fof(irreflexivity, axiom, ! [X] : ~taller(X, X)).
fof(antisymmetry, axiom, ! [X, Y] : (taller(X, Y) => ~taller(Y, X))).
fof(conclusion, conjecture, ? [X] : (in_class(X, michael_class) & man(X) & taller(X, peter))).