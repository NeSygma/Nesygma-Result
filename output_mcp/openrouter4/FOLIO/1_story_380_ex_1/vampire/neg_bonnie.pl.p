fof(premise1, axiom, ! [X] : (performs(X) => attends_engaged(X))).
fof(premise2, axiom, ! [X] : ((performs(X) & ~inactive(X)) | (~performs(X) & inactive(X)))).
fof(premise3, axiom, ! [X] : (chaperones(X) => ~student(X))).
fof(premise4, axiom, ! [X] : (inactive(X) => chaperones(X))).
fof(premise5, axiom, ! [X] : ((young_teen(X) & wishes_academic(X)) => student(X))).
fof(premise6, axiom, ((attends_engaged(bonnie) & student(bonnie)) | (~attends_engaged(bonnie) & ~student(bonnie)))).
fof(goal, conjecture, ~performs(bonnie)).