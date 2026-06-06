fof(club_member_bonnie, axiom, club_member(bonnie)).
fof(premise1, axiom, ! [X] : (club_member(X) & performs_often(X) => attends_and_engaged(X))).
fof(premise2, axiom, ! [X] : (club_member(X) => (performs_often(X) | inactive_disinterested(X)))).
fof(premise3, axiom, ! [X] : (club_member(X) & chaperones_dances(X) => ~student_attends_school(X))).
fof(premise4, axiom, ! [X] : (club_member(X) & inactive_disinterested(X) => chaperones_dances(X))).
fof(premise5, axiom, ! [X] : (club_member(X) & young_child_teenager(X) & wishes_academic_career(X) => student_attends_school(X))).
fof(premise6, axiom, club_member(bonnie) & ((attends_and_engaged(bonnie) & student_attends_school(bonnie)) | (~attends_and_engaged(bonnie) & ~student_attends_school(bonnie)))).
fof(conclusion, conjecture, performs_often(bonnie)).