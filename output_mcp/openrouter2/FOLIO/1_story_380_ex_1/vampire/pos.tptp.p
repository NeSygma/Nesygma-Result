fof(rule1, axiom, ![X] : ((in_club(X) & performs_in_school_talent_shows_often(X)) => (attends_school(X) & very_engaged_with_school_events(X)))).
fof(rule2, axiom, ![X] : (in_club(X) => (performs_in_school_talent_shows_often(X) | inactive_and_disinterested(X)))).
fof(rule3, axiom, ![X] : ((in_club(X) & chaperone_high_school_dances(X)) => ~(student(X) & attends_school(X)))).
fof(rule4, axiom, ![X] : ((in_club(X) & inactive_and_disinterested(X)) => chaperone_high_school_dances(X))).
fof(rule5, axiom, ![X] : ((in_club(X) & young_child_or_teenager(X) & wish_to_further_academic_careers(X)) => (student(X) & attends_school(X)))).
fof(bonnie_axiom, axiom, in_club(bonnie) & ((attends_school(bonnie) & very_engaged_with_school_events(bonnie) & student(bonnie)) | ~(attends_school(bonnie) & very_engaged_with_school_events(bonnie) & student(bonnie)))).
fof(goal, conjecture, performs_in_school_talent_shows_often(bonnie)).