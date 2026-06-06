fof(p1, axiom, ! [X] : ((club(X) & perform(X)) => attend_engaged(X))).
fof(p2, axiom, ! [X] : (club(X) => (perform(X) | inactive(X)))).
fof(p3, axiom, ! [X] : ((club(X) & chaperone(X)) => ~student(X))).
fof(p4, axiom, ! [X] : ((club(X) & inactive(X)) => chaperone(X))).
fof(p5, axiom, ! [X] : ((club(X) & young_wish(X)) => student(X))).
fof(p6, axiom, club(bonnie)).
fof(p7, axiom, ((attend_engaged(bonnie) & student(bonnie)) | (~attend_engaged(bonnie) & ~student(bonnie)))).
fof(goal, conjecture, ~((chaperone(bonnie) | (~chaperone(bonnie) => perform(bonnie))) => (young_wish(bonnie) & inactive(bonnie)))).