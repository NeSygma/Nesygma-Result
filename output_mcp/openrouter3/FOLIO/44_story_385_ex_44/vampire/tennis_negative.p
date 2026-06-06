% Tennis problem - negative version (negated conclusion as conjecture)
fof(rule_1, axiom, ! [X] : (ranked_highly_wta(X) => active_player(X))).
fof(rule_2, axiom, ! [X] : (lost_to_iga(X) => ranked_highly_wta(X))).
fof(rule_3, axiom, ! [X] : (female_player(X) => lost_to_iga(X))).
fof(rule_4, axiom, ! [X] : (at_rg2022(X) => (female_player(X) | male_player(X)))).
fof(rule_5, axiom, ! [X] : (male_player(X) => lost_to_rafael(X))).
fof(rule_6, axiom, (ranked_highly_wta(coco_gauff) | lost_to_rafael(coco_gauff)) => ~male_player(coco_gauff)).
fof(fact_1, axiom, at_rg2022(coco_gauff)).
fof(goal, conjecture, ~lost_to_rafael(coco_gauff)).