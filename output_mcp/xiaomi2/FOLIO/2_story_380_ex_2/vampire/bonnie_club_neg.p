fof(p1, axiom, ! [X] : ((in_club(X) & perform_talent(X)) => attend_engaged(X))).
fof(p2, axiom, ! [X] : (in_club(X) => (perform_talent(X) | inactive_disinterested(X)))).
fof(p3, axiom, ! [X] : ((in_club(X) & chaperone_dances(X)) => ~student_attend(X))).
fof(p4, axiom, ! [X] : ((in_club(X) & inactive_disinterested(X)) => chaperone_dances(X))).
fof(p5, axiom, ! [X] : ((in_club(X) & young_child_teenager(X) & further_academic(X)) => student_attend(X))).
fof(p6, axiom, (in_club(bonnie) & ((attend_engaged(bonnie) & student_attend(bonnie)) | (~attend_engaged(bonnie) & ~student_attend(bonnie))))).

% Negated conclusion
fof(goal, conjecture, ~(
    ((young_child_teenager(bonnie) & further_academic(bonnie) & chaperone_dances(bonnie))
     | (~(young_child_teenager(bonnie) & further_academic(bonnie)) & ~chaperone_dances(bonnie)))
    =>
    (student_attend(bonnie) | inactive_disinterested(bonnie))
)).