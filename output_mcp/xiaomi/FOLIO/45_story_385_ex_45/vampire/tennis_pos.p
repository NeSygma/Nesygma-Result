fof(p1, axiom, ! [X] : (ranked_highly(X) => active_major(X))).
fof(p2, axiom, ! [X] : (lost_to_swiatek(X) => ranked_highly(X))).
fof(p3, axiom, ! [X] : ((at_rg_2022(X) & female_player(X)) => lost_to_swiatek(X))).
fof(p4, axiom, ! [X] : (at_rg_2022(X) => (female_player(X) | male_player(X)))).
fof(p5, axiom, ! [X] : ((at_rg_2022(X) & male_player(X)) => lost_to_nadal(X))).
fof(p6, axiom, ((ranked_highly(coco_gauff) | lost_to_nadal(coco_gauff)) => ~male_player(coco_gauff))).
fof(p7, axiom, at_rg_2022(coco_gauff)).
fof(goal, conjecture, ~(lost_to_swiatek(coco_gauff) & active_major(coco_gauff))).