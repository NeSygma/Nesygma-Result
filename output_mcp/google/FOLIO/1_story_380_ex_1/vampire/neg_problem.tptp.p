fof(p1, axiom, ! [X] : ((in_club(X) & performs_often(X)) => attends_and_engaged(X))).
fof(p2, axiom, ! [X] : (in_club(X) => (performs_often(X) | inactive_disinterested(X)))).
fof(p3, axiom, ! [X] : ((in_club(X) & chaperones(X)) => ~is_student(X))).
fof(p4, axiom, ! [X] : ((in_club(X) & inactive_disinterested(X)) => chaperones(X))).
fof(p5, axiom, ! [X] : ((in_club(X) & young_or_teen(X) & wishes_academic(X)) => is_student(X))).
fof(p6, axiom, (in_club(bonnie) & ((attends_and_engaged(bonnie) & is_student(bonnie)) | (~attends_and_engaged(bonnie) & ~is_student(bonnie))))).
fof(goal, conjecture, ~performs_often(bonnie)).