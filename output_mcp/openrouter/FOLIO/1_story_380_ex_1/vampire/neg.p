% Negative version (negated claim)
fof(premise1, axiom, ! [X] : (perform(X) => attend_engaged(X))).
fof(premise2, axiom, ! [X] : (perform(X) | inactive_disinterested(X))).
fof(premise3, axiom, ! [X] : (chaperone(X) => ~student(X))).
fof(premise4, axiom, ! [X] : (inactive_disinterested(X) => chaperone(X))).
fof(premise5, axiom, ! [X] : (aspiring(X) => student(X))).
fof(bonnie_info, axiom, (attend_engaged(bonnie) & student(bonnie)) | (~attend_engaged(bonnie) & ~student(bonnie))).
fof(goal, conjecture, ~perform(bonnie)).