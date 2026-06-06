fof(premise1, axiom, ! [X] : (club(X) & performs_often(X) => (attends(X) & engaged(X)))).
fof(premise2, axiom, ! [X] : (club(X) => (performs_often(X) | inactive_disinterested(X)))).
fof(premise3, axiom, ! [X] : (club(X) & chaperones_dances(X) => ~student_attends_school(X))).
fof(premise4, axiom, ! [X] : (club(X) & inactive_disinterested(X) => chaperones_dances(X))).
fof(premise5, axiom, ! [X] : (club(X) & young_child_or_teen(X) & wishes_academic_career(X) => student_attends_school(X))).
fof(premise6, axiom, club(bonnie) & ((attends(bonnie) & engaged(bonnie) & student_attends_school(bonnie)) | (~(attends(bonnie) & engaged(bonnie)) & ~student_attends_school(bonnie)))).
fof(goal, conjecture, performs_often(bonnie)).