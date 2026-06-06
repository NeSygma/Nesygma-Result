% Premises
fof(premise_1, axiom, ! [X] : (in_club(X) & perform_talent(X) => attend_engaged(X))).
fof(premise_2, axiom, ! [X] : (in_club(X) => (perform_talent(X) | inactive_disinterested(X)))).
fof(premise_3, axiom, ! [X] : (in_club(X) & chaperone_dance(X) => ~student(X))).
fof(premise_4, axiom, ! [X] : (in_club(X) & inactive_disinterested(X) => chaperone_dance(X))).
fof(premise_5, axiom, ! [X] : (in_club(X) & young_teen_wish_education(X) => student(X))).

% Bonnie facts
fof(bonnie_in_club, axiom, in_club(bonnie)).
fof(bonnie_attend_student, axiom, (attend_engaged(bonnie) & student(bonnie)) | (~attend_engaged(bonnie) & ~student(bonnie))).

% Negated conclusion to evaluate
fof(negated_conclusion, conjecture, 
    ~(((chaperone_dance(bonnie) | (~chaperone_dance(bonnie) & perform_talent(bonnie))) 
     => 
     (young_teen_wish_education(bonnie) & inactive_disinterested(bonnie))))).

% Distinctness (only one constant)
fof(distinct_bonnie, axiom, in_club(bonnie)).