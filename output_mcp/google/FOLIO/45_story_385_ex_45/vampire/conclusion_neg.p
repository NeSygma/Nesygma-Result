fof(p1, axiom, ! [X] : (ranked_wta(X) => active_major(X))).
fof(p2, axiom, ! [X] : (lost_to_iga(X) => ranked_wta(X))).
fof(p3, axiom, ! [X] : ((player_rg2022(X) & female(X)) => lost_to_iga(X))).
fof(p4, axiom, ! [X] : (player_rg2022(X) => (female(X) | male(X)))).
fof(p5, axiom, ! [X] : ((player_rg2022(X) & male(X)) => lost_to_rafa(X))).
fof(p6, axiom, ! [X] : ((ranked_wta(X) | lost_to_rafa(X)) => ~ (player_rg2022(X) & male(X)))).
fof(p7, axiom, player_rg2022(coco_gauff)).
fof(goal, conjecture, ~ (lost_to_iga(coco_gauff) & active_major(coco_gauff))).