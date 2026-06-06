% Positive version
fof(premise1, axiom, ![X] : (perform_often(X) => attend_engaged(X))).
fof(premise2, axiom, ![X] : (perform_often(X) | inactive_disinterested(X))).
fof(premise3, axiom, ![X] : (chaperone(X) => ~student(X))).
fof(premise4, axiom, ![X] : (inactive_disinterested(X) => chaperone(X))).
fof(premise5, axiom, ![X] : (wish_academic(X) => student(X))).
fof(premise6a, axiom, attend_engaged(bonnie) => student(bonnie)).
fof(premise6b, axiom, student(bonnie) => attend_engaged(bonnie)).
fof(goal, conjecture, (chaperone(bonnie) | perform_often(bonnie)) => (wish_academic(bonnie) & inactive_disinterested(bonnie))).