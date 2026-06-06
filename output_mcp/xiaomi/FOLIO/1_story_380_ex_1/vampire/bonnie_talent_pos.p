fof(premise1, axiom, ! [X] : ((in_club(X) & performs_talent_shows(X)) => attends_engaged(X))).
fof(premise2, axiom, ! [X] : (in_club(X) => (performs_talent_shows(X) | inactive_disinterested(X)))).
fof(premise3, axiom, ! [X] : ((in_club(X) & chaperones_dances(X)) => ~student_attends(X))).
fof(premise4, axiom, ! [X] : ((in_club(X) & inactive_disinterested(X)) => chaperones_dances(X))).
fof(premise5, axiom, ! [X] : ((in_club(X) & young_child_or_teen(X) & wishes_academic(X)) => student_attends(X))).
fof(premise6, axiom, (in_club(bonnie) & ((attends_engaged(bonnie) & student_attends(bonnie)) | (~attends_engaged(bonnie) & ~student_attends(bonnie))))).
fof(goal, conjecture, performs_talent_shows(bonnie)).