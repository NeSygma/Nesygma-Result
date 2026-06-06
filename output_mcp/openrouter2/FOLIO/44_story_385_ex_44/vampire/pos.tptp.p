fof(distinct, axiom, (coco_gauff != iga_swiatek & coco_gauff != rafael_nadal & iga_swiatek != rafael_nadal)).
fof(rule1, axiom, ! [X] : (ranked_highly_by_wta(X) => active_player(X))).
fof(rule2, axiom, ! [X] : ((lost_to(X, iga_swiatek) & at_roland_garros_2022(X)) => ranked_highly_by_wta(X))).
fof(rule3, axiom, ! [X] : ((at_roland_garros_2022(X) & female(X)) => lost_to(X, iga_swiatek))).
fof(rule4, axiom, ! [X] : (at_roland_garros_2022(X) => (female(X) | male(X)))).
fof(rule5, axiom, ! [X] : ((at_roland_garros_2022(X) & male(X)) => lost_to(X, rafael_nadal))).
fof(rule6, axiom, ((ranked_highly_by_wta(coco_gauff) | lost_to(coco_gauff, rafael_nadal)) => ~ (male(coco_gauff) & at_roland_garros_2022(coco_gauff)))).
fof(fact_coco, axiom, at_roland_garros_2022(coco_gauff)).
fof(goal, conjecture, lost_to(coco_gauff, rafael_nadal)).