fof(premise_1, axiom, ! [X] : (ranked_highly_wta(X) => active_player(X))).
fof(premise_2, axiom, ! [X] : (lost_to_iga(X) => ranked_highly_wta(X))).
fof(premise_3, axiom, ! [X] : (female_player(X) => lost_to_iga(X))).
fof(premise_4, axiom, ! [X] : (at_roland_garros_2022(X) => (female_player(X) | male_player(X)))).
fof(premise_5, axiom, ! [X] : (male_player(X) => lost_to_rafael(X))).
fof(premise_6, axiom, (ranked_highly_wta(coco_gauff) | lost_to_rafael(coco_gauff)) => ~male_player(coco_gauff)).
fof(premise_7, axiom, at_roland_garros_2022(coco_gauff)).
fof(goal, conjecture, lost_to_iga(coco_gauff) & active_player(coco_gauff)).