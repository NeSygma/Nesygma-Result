fof(p1, axiom, ! [X] : (ranked_wta(X) => active_major(X))).
fof(p2, axiom, ! [X] : (lost_to_iga(X, rg2022) => ranked_wta(X))).
fof(p3, axiom, ! [X] : (female(X, rg2022) => lost_to_iga(X, rg2022))).
fof(p4, axiom, ! [X] : (at_rg2022(X) => (female(X, rg2022) | male(X, rg2022)))).
fof(p5, axiom, ! [X] : (male(X, rg2022) => lost_to_rafael(X, rg2022))).
fof(p6, axiom, ((ranked_wta(coco_gauff) | lost_to_rafael(coco_gauff, rg2022)) => ~male(coco_gauff, rg2022))).
fof(p7, axiom, at_rg2022(coco_gauff)).
fof(goal, conjecture, ~lost_to_rafael(coco_gauff, rg2022)).