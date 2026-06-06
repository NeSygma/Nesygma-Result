fof(club_member_bonnie, axiom, club_member(bonnie)).
fof(rule1, axiom, ! [X] : ((club_member(X) & perform_in_talent_show_often(X)) => (attends_school_events(X) & very_engaged_with_school_events(X)))).
fof(rule2, axiom, ! [X] : (club_member(X) => (perform_in_talent_show_often(X) | inactive_and_disinterested_member(X)))).
fof(rule3, axiom, ! [X] : ((club_member(X) & chaperone_high_school_dance(X)) => ~student_attends_school(X))).
fof(rule4, axiom, ! [X] : ((club_member(X) & inactive_and_disinterested_member(X)) => chaperone_high_school_dance(X))).
fof(rule5, axiom, ! [X] : ((club_member(X) & young_child_or_teenager(X) & wish_to_further_academic_career(X)) => student_attends_school(X))).
fof(bonnie_disjunction, axiom, ((attends_school_events(bonnie) & very_engaged_with_school_events(bonnie) & student_attends_school(bonnie)) | ~(attends_school_events(bonnie) & very_engaged_with_school_events(bonnie) & ~student_attends_school(bonnie)))).
fof(conjecture, conjecture, (((young_child_or_teenager(bonnie) & wish_to_further_academic_career(bonnie) & chaperone_high_school_dance(bonnie)) | ~young_child_or_teenager(bonnie)) & ~(student_attends_school(bonnie) | inactive_and_disinterested_member(bonnie)))).