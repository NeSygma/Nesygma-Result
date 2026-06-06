% Positive version
fof(distinct1, axiom, coco_gauff != iga_swiatek).
fof(distinct2, axiom, coco_gauff != rafael_nadal).
fof(distinct3, axiom, iga_swiatek != rafael_nadal).

fof(rule1, axiom, ! [X] : (ranked_highly(X) => active_major(X))).
fof(rule2, axiom, ! [X] : (lost_to(X, iga_swiatek) => ranked_highly(X))).
fof(rule3, axiom, ! [X] : ((female(X) & at_rg2022(X)) => lost_to(X, iga_swiatek))).
fof(rule4, axiom, ! [X] : (at_rg2022(X) => (female(X) | male(X)))).
fof(rule5, axiom, ! [X] : ((male(X) & at_rg2022(X)) => lost_to(X, rafael_nadal))).
fof(rule6, axiom, ((ranked_highly(coco_gauff) | lost_to(coco_gauff, rafael_nadal)) => ~male(coco_gauff))).
fof(fact1, axiom, at_rg2022(coco_gauff)).

fof(goal, conjecture, lost_to(coco_gauff, rafael_nadal)).