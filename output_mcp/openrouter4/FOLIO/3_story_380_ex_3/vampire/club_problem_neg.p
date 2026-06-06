fof(premise1, axiom, ! [X] : ((club(X) & performs(X)) => attends(X))).
fof(premise2, axiom, ! [X] : (club(X) => (performs(X) | inactive(X)))).
fof(premise3, axiom, ! [X] : ((club(X) & chaperones(X)) => ~student(X))).
fof(premise4, axiom, ! [X] : ((club(X) & inactive(X)) => chaperones(X))).
fof(premise5, axiom, ! [X] : ((club(X) & young_teen(X) & wishes(X)) => student(X))).
fof(premise6, axiom, (club(bonnie) & ((attends(bonnie) & student(bonnie)) | (~attends(bonnie) & ~student(bonnie))))).

fof(conclusion_neg, conjecture, ~((chaperones(bonnie) | performs(bonnie)) => (young_teen(bonnie) & wishes(bonnie) & inactive(bonnie)))).