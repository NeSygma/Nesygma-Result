fof(axiom1, axiom, ! [X] : ((in_club(X) & performs_often(X)) => attend_engaged(X))).
fof(axiom2, axiom, ! [X] : (in_club(X) => (performs_often(X) | inactive_disinterested(X)))).
fof(axiom3, axiom, ! [X] : ((in_club(X) & chaperone_dances(X)) => ~student(X))).
fof(axiom4, axiom, ! [X] : ((in_club(X) & inactive_disinterested(X)) => chaperone_dances(X))).
fof(axiom5, axiom, ! [X] : ((in_club(X) & young_child_teenager(X) & wishes_academic(X)) => student(X))).
fof(axiom6, axiom, in_club(bonnie)).
fof(conclusion, conjecture, ~performs_often(bonnie)).