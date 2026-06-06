fof(premise1, axiom, ! [X] : (ranked_highly_by_wta(X) => most_active_major_tennis(X))).
fof(premise2, axiom, ! [X] : ((lost_to_iga(X) & at_roland_garros_2022(X)) => ranked_highly_by_wta(X))).
fof(premise3, axiom, ! [X] : ((female_player(X) & at_roland_garros_2022(X)) => lost_to_iga(X))).
fof(premise4, axiom, ! [X] : (at_roland_garros_2022(X) => (female_player(X) | male_player(X)))).
fof(premise5, axiom, ! [X] : ((male_player(X) & at_roland_garros_2022(X)) => lost_to_rafael(X))).
fof(premise6, axiom, ! [X] : ((ranked_highly_by_wta(X) | lost_to_rafael(X)) => ~(male_player(X) & at_roland_garros_2022(X)))).
fof(premise7, axiom, at_roland_garros_2022(coco_gauff)).
fof(conclusion_negation, conjecture, ~lost_to_rafael(coco_gauff)).