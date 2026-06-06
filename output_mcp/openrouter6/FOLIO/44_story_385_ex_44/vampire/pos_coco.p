fof(premise_1, axiom, ! [X] : (ranked_highly_wta(X) => most_active_player(X))).
fof(premise_2, axiom, ! [X] : (lost_to_iga(X) => ranked_highly_wta(X))).
fof(premise_3, axiom, ! [X] : (female_tennis_player(X) => lost_to_iga(X))).
fof(premise_4, axiom, ! [X] : (tennis_player_at_rg2022(X) => (female_tennis_player(X) | male_tennis_player(X)))).
fof(premise_5, axiom, ! [X] : (male_tennis_player(X) => lost_to_rafael(X))).
fof(premise_6, axiom, (ranked_highly_wta(coco) | lost_to_rafael(coco)) => ~male_tennis_player(coco)).
fof(premise_7, axiom, tennis_player_at_rg2022(coco)).
fof(distinct, axiom, (coco != iga & coco != rafael & iga != rafael)).
fof(goal, conjecture, lost_to_rafael(coco)).