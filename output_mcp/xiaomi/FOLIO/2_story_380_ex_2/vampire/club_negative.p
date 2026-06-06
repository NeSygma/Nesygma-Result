fof(p1, axiom, ! [X] : (in_club(X) & performs(X) => attends_engaged(X))).
fof(p2, axiom, ! [X] : (in_club(X) => (performs(X) | inactive_disinterested(X)))).
fof(p3, axiom, ! [X] : (in_club(X) & chaperones(X) => ~student_attends(X))).
fof(p4, axiom, ! [X] : (in_club(X) & inactive_disinterested(X) => chaperones(X))).
fof(p5, axiom, ! [X] : (in_club(X) & young_child_or_teen(X) & wishes_academic(X) => student_attends(X))).
fof(p6, axiom, in_club(bonnie) & ((attends_engaged(bonnie) & student_attends(bonnie)) | (~attends_engaged(bonnie) & ~student_attends(bonnie)))).
fof(conclusion, conjecture, ~(((young_child_or_teen(bonnie) & wishes_academic(bonnie) & chaperones(bonnie)) | (~young_child_or_teen(bonnie) & ~wishes_academic(bonnie))) => (student_attends(bonnie) | inactive_disinterested(bonnie)))).