fof(premise1, axiom, ! [X] : (ranked_highly(X) => active_major(X))).
fof(premise2, axiom, ! [X] : (lost_to_swiatek(X) => ranked_highly(X))).
fof(premise3, axiom, ! [X] : ((at_rg_2022(X) & female_player(X)) => lost_to_swiatek(X))).
fof(premise4, axiom, ! [X] : (at_rg_2022(X) => (female_player(X) | male_player(X)))).
fof(premise5, axiom, ! [X] : ((at_rg_2022(X) & male_player(X)) => lost_to_nadal(X))).
fof(premise6, axiom, ((ranked_highly(coco_gauff) | lost_to_nadal(coco_gauff)) => ~male_player(coco_gauff))).
fof(premise7, axiom, at_rg_2022(coco_gauff)).
fof(distinct, axiom, (coco_gauff != iga_swiatek & coco_gauff != rafael_nadal & iga_swiatek != rafael_nadal)).
fof(goal, conjecture, ~lost_to_nadal(coco_gauff)).