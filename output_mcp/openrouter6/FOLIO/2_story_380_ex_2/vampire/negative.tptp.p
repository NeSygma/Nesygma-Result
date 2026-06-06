fof(premise1, axiom, ! [X] : (in_club(X) & performs_talent_shows(X) => attends_engaged(X))).
fof(premise2, axiom, ! [X] : (in_club(X) => (performs_talent_shows(X) | inactive_disinterested(X)))).
fof(premise3, axiom, ! [X] : (in_club(X) & chaperone_dances(X) => ~student_attends_school(X))).
fof(premise4, axiom, ! [X] : (in_club(X) & inactive_disinterested(X) => chaperone_dances(X))).
fof(premise5, axiom, ! [X] : (in_club(X) & young_wish_academic(X) => student_attends_school(X))).
fof(premise6, axiom, in_club(bonnie) & ((attends_engaged(bonnie) & student_attends_school(bonnie)) | (~attends_engaged(bonnie) & ~student_attends_school(bonnie)))).
fof(negated_conclusion, conjecture, (young_wish_academic(bonnie) <=> chaperone_dances(bonnie)) & ~student_attends_school(bonnie) & ~inactive_disinterested(bonnie)).