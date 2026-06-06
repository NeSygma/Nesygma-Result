% Positive run: conjecture = lost_nadal(coco)
fof(p1, axiom, ! [X] : (ranked_highly(X) => active_major(X))).
fof(p2, axiom, ! [X] : (lost_iga(X) => ranked_highly(X))).
fof(p3, axiom, ! [X] : (female(X) => lost_iga(X))).
fof(p4, axiom, ! [X] : (player(X) => (female(X) | male(X)))).
fof(p5, axiom, ! [X] : (male(X) => lost_nadal(X))).
fof(p6, axiom, (ranked_highly(coco) | lost_nadal(coco)) => ~male(coco)).
fof(p7, axiom, player(coco)).
fof(goal, conjecture, lost_nadal(coco)).