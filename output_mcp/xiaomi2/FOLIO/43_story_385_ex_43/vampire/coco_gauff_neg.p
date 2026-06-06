% Premise 1: Ranked highly by WTA => most active in major tennis
fof(p1, axiom, ! [X] : (ranked_highly_wta(X) => most_active_major(X))).

% Premise 2: Lost to Iga at RG 2022 => ranked highly by WTA
fof(p2, axiom, ! [X] : (lost_to_iga_rg2022(X) => ranked_highly_wta(X))).

% Premise 3: Female tennis player at RG 2022 => lost to Iga
fof(p3, axiom, ! [X] : (female_tennis_player_rg2022(X) => lost_to_iga_rg2022(X))).

% Premise 4: Tennis player at RG 2022 => female or male
fof(p4, axiom, ! [X] : (tennis_player_rg2022(X) => (female_tennis_player_rg2022(X) | male_tennis_player_rg2022(X)))).

% Premise 5: Male tennis player at RG 2022 => lost to Nadal
fof(p5, axiom, ! [X] : (male_tennis_player_rg2022(X) => lost_to_nadal_rg2022(X))).

% Premise 6: If Coco Gauff ranked highly by WTA or lost to Nadal, then not male at RG 2022
fof(p6, axiom, ((ranked_highly_wta(coco_gauff) | lost_to_nadal_rg2022(coco_gauff)) => ~male_tennis_player_rg2022(coco_gauff))).

% Premise 7: Coco Gauff is at Roland Garros 2022 (i.e., is a tennis player there)
fof(p7, axiom, tennis_player_rg2022(coco_gauff)).

% Negated conclusion: Coco Gauff is NOT among the most active Grand-Slam players
fof(goal, conjecture, ~most_active_major(coco_gauff)).