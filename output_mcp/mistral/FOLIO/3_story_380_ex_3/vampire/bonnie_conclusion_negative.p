fof(performs_implies_attends, axiom, ! [X] : (performs_in_talent_shows(X) => attends_and_engaged(X))).
fof(club_perform_or_inactive, axiom, ! [X] : (in_club(X) => (performs_in_talent_shows(X) | inactive_disinterested(X)))).
fof(chaperones_implies_not_student, axiom, ! [X] : (chaperones_dances(X) => ~is_student_attending_school(X))).
fof(inactive_implies_chaperones, axiom, ! [X] : (inactive_disinterested(X) => chaperones_dances(X))).
fof(young_academic_implies_student, axiom, ! [X] : ((young_child_or_teenager(X) & wishes_academic_career(X)) => is_student_attending_school(X))).
fof(bonnie_in_club, axiom, in_club(bonnie)).
fof(bonnie_attendance_status, axiom, ((attends_and_engaged(bonnie) & is_student_attending_school(bonnie)) | (~attends_and_engaged(bonnie) & ~is_student_attending_school(bonnie)))).
fof(conclusion_negation, conjecture, (chaperones_dances(bonnie) | performs_in_talent_shows(bonnie)) & (~young_child_or_teenager(bonnie) | ~wishes_academic_career(bonnie) | ~inactive_disinterested(bonnie))).