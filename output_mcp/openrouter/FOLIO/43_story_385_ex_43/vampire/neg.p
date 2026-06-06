% Negative version
fof(premise1, axiom, ! [X] : (ranked_highly(X) => active_major(X))).
fof(premise2, axiom, ! [X] : (lost_to(X, iga_swiatek) => ranked_highly(X))).
fof(premise3, axiom, ! [X] : ((female(X) & at_rg2022(X)) => lost_to(X, iga_swiatek))).
fof(premise4, axiom, ! [X] : (at_rg2022(X) => (female(X) | male(X)))).
fof(premise5, axiom, ! [X] : ((male(X) & at_rg2022(X)) => lost_to(X, rafael_nadal))).
fof(premise6, axiom, ((ranked_highly(coco_gauff) | lost_to(coco_gauff, rafael_nadal)) => (~male(coco_gauff) | ~at_rg2022(coco_gauff)))).
fof(premise7, axiom, at_rg2022(coco_gauff)).
fof(goal, conjecture, ~active_major(coco_gauff)).