fof(p1, axiom, ! [X] : ((in_club(X) & perform_talent_show(X)) => (attend_school_events(X) & engaged_school_events(X)))).
fof(p2, axiom, ! [X] : (in_club(X) => (perform_talent_show(X) | inactive_disinterested(X)))).
fof(p3, axiom, ! [X] : ((in_club(X) & chaperone_dances(X)) => ~student_attends_school(X))).
fof(p4, axiom, ! [X] : ((in_club(X) & inactive_disinterested(X)) => chaperone_dances(X))).
fof(p5, axiom, ! [X] : ((in_club(X) & young_or_teen(X) & wishes_academic_career(X)) => student_attends_school(X))).
fof(p6, axiom, in_club(bonnie) & ((attend_school_events(bonnie) & engaged_school_events(bonnie) & student_attends_school(bonnie)) | (~(attend_school_events(bonnie) & engaged_school_events(bonnie)) & ~student_attends_school(bonnie)))).
fof(goal, conjecture, (( (young_or_teen(bonnie) & wishes_academic_career(bonnie) & chaperone_dances(bonnie)) | ~(young_or_teen(bonnie) & wishes_academic_career(bonnie)) ) => (student_attends_school(bonnie) | inactive_disinterested(bonnie)))).