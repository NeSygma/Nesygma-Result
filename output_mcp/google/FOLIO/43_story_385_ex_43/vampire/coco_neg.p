fof(p1, axiom, ! [X] : (ranked_wta(X) => active_player(X))).
fof(p2, axiom, ! [X] : (lost_to_iga(X) => ranked_wta(X))).
fof(p3, axiom, ! [X] : (female(X) => lost_to_iga(X))).
fof(p4, axiom, ! [X] : (player(X) => (female(X) | male(X)))).
fof(p5, axiom, ! [X] : (male(X) => lost_to_rafa(X))).
fof(p6, axiom, ! [X] : ((ranked_wta(X) | lost_to_rafa(X)) => ~male(X))).
fof(p7, axiom, player(coco_gauff)).
fof(goal, conjecture, ~active_player(coco_gauff)).