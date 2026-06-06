fof(transitivity, axiom, ! [X,Y,Z] : ((taller(X,Y) & taller(Y,Z)) => taller(X,Z))).
fof(man_michael, axiom, man(michael)).
fof(man_peter, axiom, man(peter)).
fof(man_windy, axiom, man(windy)).
fof(distinct_people, axiom, michael != peter & michael != windy & peter != windy).
fof(michael_in_class, axiom, in_class(michael, michael_class)).
fof(michael_taller_than_others, axiom, ! [Y] : ((in_class(Y, michael_class) & Y != michael) => taller(michael, Y))).
fof(peter_taller_than_michael, axiom, taller(peter, michael)).
fof(conjecture, conjecture, ~(? [Y] : (man(Y) & in_class(Y, michael_class) & taller(Y, peter)))).