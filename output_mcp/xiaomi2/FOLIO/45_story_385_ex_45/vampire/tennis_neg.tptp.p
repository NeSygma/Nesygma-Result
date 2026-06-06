fof(p1, axiom, ! [X] : (ranked_highly_wta(X) => most_active_major(X))).
fof(p2, axiom, ! [X] : (lost_to_iga_rg2022(X) => ranked_highly_wta(X))).
fof(p3, axiom, ! [X] : (female_tennis_rg2022(X) => lost_to_iga_rg2022(X))).
fof(p4, axiom, ! [X] : (at_rg2022(X) => (female_tennis_rg2022(X) | male_tennis_rg2022(X)))).
fof(p5, axiom, ! [X] : (male_tennis_rg2022(X) => lost_to_nadal(X))).
fof(p6, axiom, ((ranked_highly_wta(coco_gauff) | lost_to_nadal(coco_gauff)) => ~male_tennis_rg2022(coco_gauff))).
fof(p7, axiom, at_rg2022(coco_gauff)).
fof(goal, conjecture, lost_to_iga_rg2022(coco_gauff) & most_active_major(coco_gauff)).