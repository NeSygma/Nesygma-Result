% Positive version: original conclusion as conjecture
% "Coco Gauff is among the most active Grand-Slam players"
% Represented as: most_active_gs_player(coco_gauff)

% Predicates:
% ranked_high_wta(X)   - X is ranked highly by the Women's Tennis Association
% most_active_major(X) - X is one of the most active players in major tennis
% lost_to_iga_rg22(X)  - X lost to Iga Swiatek at Roland Garros 2022
% female_player_rg22(X) - X is a female tennis player at Roland Garros 2022
% male_player_rg22(X)  - X is a male tennis player at Roland Garros 2022
% at_rg22(X)           - X is at Roland Garros 2022
% lost_to_nadal_rg22(X) - X lost to Rafael Nadal at Roland Garros 2022

% Constants:
% coco_gauff, iga_swiatek, rafael_nadal

% Distinctness
fof(distinct, axiom, (coco_gauff != iga_swiatek & coco_gauff != rafael_nadal & iga_swiatek != rafael_nadal)).

% Premise 1: If someone is ranked highly by the WTA, then they are one of the most active players in major tennis.
fof(premise_1, axiom, ! [X] : (ranked_high_wta(X) => most_active_major(X))).

% Premise 2: Everyone who lost to Iga Swiatek at Roland Garros 2022 is ranked highly by the WTA.
fof(premise_2, axiom, ! [X] : (lost_to_iga_rg22(X) => ranked_high_wta(X))).

% Premise 3: All female tennis players at Roland Garros 2022 lost to Iga Swiatek.
fof(premise_3, axiom, ! [X] : (female_player_rg22(X) => lost_to_iga_rg22(X))).

% Premise 4: All tennis players at Roland Garros 2022 are either female or male.
fof(premise_4, axiom, ! [X] : (at_rg22(X) => (female_player_rg22(X) | male_player_rg22(X)))).

% Premise 5: All male tennis players at Roland Garros 2022 lost to Rafael Nadal.
fof(premise_5, axiom, ! [X] : (male_player_rg22(X) => lost_to_nadal_rg22(X))).

% Premise 6: If Coco Gauff is ranked highly by the WTA or lost to Rafael Nadal, then Coco Gauff is not a male tennis player at Roland Garros 2022.
fof(premise_6, axiom, (ranked_high_wta(coco_gauff) | lost_to_nadal_rg22(coco_gauff)) => ~male_player_rg22(coco_gauff)).

% Premise 7: Coco Gauff is at Roland Garros 2022.
fof(premise_7, axiom, at_rg22(coco_gauff)).

% Conclusion: Coco Gauff is among the most active Grand-Slam players.
% We interpret "most active Grand-Slam players" as "most active players in major tennis" (same as premise 1's consequent).
fof(conclusion, conjecture, most_active_major(coco_gauff)).