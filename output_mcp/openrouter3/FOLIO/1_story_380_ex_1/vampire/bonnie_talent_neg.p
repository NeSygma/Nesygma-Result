% Problem: Bonnie performs in school talent shows often
% Negative version: negated conclusion as conjecture

fof(in_club_bonnie, axiom, in_club(bonnie)).

fof(premise_1, axiom, 
    ! [X] : (in_club(X) & perform_talent(X) => attend_engaged(X))).

fof(premise_2, axiom, 
    ! [X] : (in_club(X) => (perform_talent(X) | inactive_disinterested(X)))).

fof(premise_3, axiom, 
    ! [X] : (in_club(X) & chaperone_dance(X) => ~student_attend_school(X))).

fof(premise_4, axiom, 
    ! [X] : (in_club(X) & inactive_disinterested(X) => chaperone_dance(X))).

fof(premise_5, axiom, 
    ! [X] : (in_club(X) & (young_child(X) | teenager(X)) & wish_academic(X) => student_attend_school(X))).

fof(premise_6, axiom, 
    (attend_engaged(bonnie) & student_attend_school(bonnie)) | 
    (~attend_engaged(bonnie) & ~student_attend_school(bonnie))).

fof(conclusion, conjecture, ~perform_talent(bonnie)).