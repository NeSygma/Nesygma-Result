% Negative file: Negated conclusion as conjecture
fof(premise1, axiom, ! [X] : (in_club(X) & perform_talent(X) => attend_engaged(X))).
fof(premise2, axiom, ! [X] : (in_club(X) => (perform_talent(X) | inactive_disinterested(X)))).
fof(premise3, axiom, ! [X] : (in_club(X) & chaperone_dance(X) => ~student(X))).
fof(premise4, axiom, ! [X] : (in_club(X) & inactive_disinterested(X) => chaperone_dance(X))).
fof(premise5, axiom, ! [X] : (in_club(X) & (young_child(X) | teenager(X)) & wishes_academic(X) => student(X))).
fof(premise6, axiom, in_club(bonnie) & ((attend_engaged(bonnie) & student(bonnie)) | ~(attend_engaged(bonnie) & student(bonnie)))).
fof(distinct_bonnie, axiom, bonnie != a & bonnie != b & bonnie != c). % Ensure bonnie is distinct
fof(negated_conclusion, conjecture, 
    ((young_child(bonnie) | teenager(bonnie)) & wishes_academic(bonnie) & chaperone_dance(bonnie) | 
     ~((young_child(bonnie) | teenager(bonnie)) & wishes_academic(bonnie))) 
    & 
    ~(student(bonnie) | inactive_disinterested(bonnie))
).