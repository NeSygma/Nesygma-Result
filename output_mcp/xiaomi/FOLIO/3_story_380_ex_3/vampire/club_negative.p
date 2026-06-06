fof(p1, axiom, ! [X] : (in_club(X) & performs_talent(X) => attends_engaged(X))).
fof(p2, axiom, ! [X] : (in_club(X) => (performs_talent(X) | inactive_disinterested(X)))).
fof(p3, axiom, ! [X] : (in_club(X) & chaperones(X) => ~student_attends(X))).
fof(p4, axiom, ! [X] : (in_club(X) & inactive_disinterested(X) => chaperones(X))).
fof(p5, axiom, ! [X] : (in_club(X) & young_wishes_academic(X) => student_attends(X))).
fof(p6, axiom, in_club(bonnie) & ((attends_engaged(bonnie) & student_attends(bonnie)) | (~attends_engaged(bonnie) & ~student_attends(bonnie)))).
fof(goal, conjecture, ~((chaperones(bonnie) | (~chaperones(bonnie) & performs_talent(bonnie))) => (young_wishes_academic(bonnie) & inactive_disinterested(bonnie)))).