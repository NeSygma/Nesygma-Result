% Tennis problem - positive version (original conclusion)
fof(rule_1, axiom, ! [X] : (ranked_highly_wta(X) => active_player(X))).
fof(rule_2, axiom, ! [X] : (lost_to_iga(X) => ranked_highly_wta(X))).
fof(rule_3, axiom, ! [X] : (female_player(X) => lost_to_iga(X))).
fof(rule_4, axiom, ! [X] : (at_roland_garros_2022(X) => (female_player(X) | male_player(X)))).
fof(rule_5, axiom, ! [X] : (male_player(X) => lost_to_rafael(X))).
fof(rule_6, axiom, (ranked_highly_wta(coco_gauff) | lost_to_rafael(coco_gauff)) => ~male_player(coco_gauff)).
fof(fact_1, axiom, at_roland_garros_2022(coco_gauff)).
fof(distinct_entities, axiom, (iga_swiatek != rafael_nadal & iga_swiatek != coco_gauff & rafael_nadal != coco_gauff)).
fof(goal, conjecture, active_player(coco_gauff)).