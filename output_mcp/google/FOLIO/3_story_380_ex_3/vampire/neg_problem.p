fof(p1, axiom, ! [X] : ((in_club(X) & perform_talent_show(X)) => (attend_school_events(X) & engaged_school_events(X)))).
fof(p2, axiom, ! [X] : (in_club(X) => (perform_talent_show(X) | inactive_disinterested(X)))).
fof(p3, axiom, ! [X] : ((in_club(X) & chaperone_dances(X)) => ~student_attends_school(X))).
fof(p4, axiom, ! [X] : ((in_club(X) & inactive_disinterested(X)) => chaperone_dances(X))).
fof(p5, axiom, ! [X] : ((in_club(X) & young_teen(X) & wish_academic(X)) => student_attends_school(X))).
fof(p6, axiom, in_club(bonnie)).
fof(p7, axiom, ((attend_school_events(bonnie) & engaged_school_events(bonnie) & student_attends_school(bonnie)) | (~(attend_school_events(bonnie) & engaged_school_events(bonnie)) & ~student_attends_school(bonnie)))).
fof(conclusion, conjecture, ~((chaperone_dances(bonnie) | (~chaperone_dances(bonnie) => perform_talent_show(bonnie))) => (young_teen(bonnie) & wish_academic(bonnie) & inactive_disinterested(bonnie)))).