% Negative version: negated conclusion as conjecture
% "Coco Gauff is NOT among the most active Grand-Slam players"

fof(distinct, axiom, (coco_gauff != iga_swiatek & coco_gauff != rafael_nadal & iga_swiatek != rafael_nadal)).

fof(premise_1, axiom, ! [X] : (ranked_high_wta(X) => most_active_major(X))).

fof(premise_2, axiom, ! [X] : (lost_to_iga_rg22(X) => ranked_high_wta(X))).

fof(premise_3, axiom, ! [X] : (female_player_rg22(X) => lost_to_iga_rg22(X))).

fof(premise_4, axiom, ! [X] : (at_rg22(X) => (female_player_rg22(X) | male_player_rg22(X)))).

fof(premise_5, axiom, ! [X] : (male_player_rg22(X) => lost_to_nadal_rg22(X))).

fof(premise_6, axiom, (ranked_high_wta(coco_gauff) | lost_to_nadal_rg22(coco_gauff)) => ~male_player_rg22(coco_gauff)).

fof(premise_7, axiom, at_rg22(coco_gauff)).

% Negated conclusion: Coco Gauff is NOT among the most active Grand-Slam players.
fof(conclusion_neg, conjecture, ~most_active_major(coco_gauff)).