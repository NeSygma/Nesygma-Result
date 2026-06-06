fof(premise1, axiom, ! [X] : ((in_club(X) & performs_in_school_talent_shows_often(X)) => (attends_school_events(X) & very_engaged_with_school_events(X)))).
fof(premise2, axiom, ! [X] : (in_club(X) => (performs_in_school_talent_shows_often(X) | inactive_and_disinterested_member(X)))).
fof(premise3, axiom, ! [X] : ((in_club(X) & chaperone_high_school_dances(X)) => ~student_attends_school(X))).
fof(premise4, axiom, ! [X] : ((in_club(X) & inactive_and_disinterested_member(X)) => chaperone_high_school_dances(X))).
fof(premise5, axiom, ! [X] : ((in_club(X) & young_teen_wishes_academic(X)) => student_attends_school(X))).
fof(bonnie_in_club, axiom, in_club(bonnie)).
fof(bonnie_disjunction, axiom, ((attends_school_events(bonnie) & very_engaged_with_school_events(bonnie) & student_attends_school(bonnie)) | ~(attends_school_events(bonnie) & very_engaged_with_school_events(bonnie) & ~student_attends_school(bonnie)))).
fof(conjecture, conjecture, ~((chaperone_high_school_dances(bonnie) | performs_in_school_talent_shows_often(bonnie)) => (young_teen_wishes_academic(bonnie) & inactive_and_disinterested_member(bonnie)))).