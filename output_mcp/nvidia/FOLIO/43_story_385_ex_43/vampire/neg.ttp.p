% Axioms
fof(axiom_rank_highly, axiom, ! [X] : (ranked_highly_by_WTA(X) => most_active_major_tennis_player(X))).
fof(axiom_lost_to_iga, axiom, ! [X] : (lost_to_Iga_at_Roland_Garros_2022(X) => ranked_highly_by_WTA(X))).
fof(axiom_female_lost_to_iga, axiom, ! [X] : (female_tennis_player_at_Roland_Garros_2022(X) => lost_to_Iga_at_Roland_Garros_2022(X))).
fof(axiom_all_players_female_or_male, axiom, ! [X] : (tennis_player_at_Roland_Garros_2022(X) => (female_tennis_player_at_Roland_Garros_2022(X) | male_tennis_player_at_Roland_Garros_2022(X))) ).
fof(axiom_male_lost_to_rafael, axiom, ! [X] : (male_tennis_player_at_Roland_Garros_2022(X) => lost_to_Rafael_Nadal_2022(X))).
fof(axiom_coco_cond, axiom, (ranked_highly_by_WTA(coco_gauff) | lost_to_Rafael_Nadal_2022(coco_gauff)) => ~male_tennis_player_at_Roland_Garros_2022(coco_gauff)).
fof(axiom_coco_at_event, axiom, tennis_player_at_Roland_Garros_2022(coco_gauff)).
fof(distinct_constants, axiom, (coco_gauff != iga_swiatek & coco_gauff != rafael_nadal & iga_swiatek != rafael_nadal)).
fof(conjecture, conjecture, ~most_active_major_tennis_player(coco_gauff)).