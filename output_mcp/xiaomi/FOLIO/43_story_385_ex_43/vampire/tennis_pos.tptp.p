fof(p1, axiom, ! [X] : (ranked_highly(X) => most_active(X))).
fof(p2, axiom, ! [X] : (lost_to_swiatek(X) => ranked_highly(X))).
fof(p3, axiom, ! [X] : ((at_rg_2022(X) & female(X)) => lost_to_swiatek(X))).
fof(p4, axiom, ! [X] : (at_rg_2022(X) => (female(X) | male(X)))).
fof(p5, axiom, ! [X] : ((at_rg_2022(X) & male(X)) => lost_to_nadal(X))).
fof(p6, axiom, ((ranked_highly(coco_gauff) | lost_to_nadal(coco_gauff)) => ~male(coco_gauff))).
fof(p7, axiom, at_rg_2022(coco_gauff)).
fof(goal, conjecture, most_active(coco_gauff)).