% Positive version: original conclusion as conjecture
% Conclusion: Coco Gauff is not both a player who lost to Iga Swiatek at Roland Garros 2022 and one of the most active players in major tennis.
% i.e., ~(lost_to_swiatek(coco_gauff) & most_active(coco_gauff))

% Predicates:
% ranked_high(X) - X is ranked highly by the Women's Tennis Association
% most_active(X) - X is one of the most active players in major tennis
% lost_to_swiatek(X) - X lost to Iga Swiatek at Roland Garros 2022
% female(X) - X is a female tennis player at Roland Garros 2022
% male(X) - X is a male tennis player at Roland Garros 2022
% at_roland_garros(X) - X is a tennis player at Roland Garros 2022
% lost_to_nadal(X) - X lost to Rafael Nadal

% Constants:
% coco_gauff

fof(distinct, axiom, $true).  % No distinctness needed for single constant

% Premise 1: If someone is ranked highly by the Women's Tennis Association, then they are one of the most active players in major tennis.
fof(premise_1, axiom, ! [X] : (ranked_high(X) => most_active(X))).

% Premise 2: Everyone who lost to Iga Swiatek at Roland Garros 2022 is ranked highly by the Women's Tennis Association.
fof(premise_2, axiom, ! [X] : (lost_to_swiatek(X) => ranked_high(X))).

% Premise 3: All female tennis players at Roland Garros 2022 lost to Iga Swiatek.
fof(premise_3, axiom, ! [X] : (female(X) => lost_to_swiatek(X))).

% Premise 4: All tennis players at Roland Garros 2022 are either female or male.
fof(premise_4, axiom, ! [X] : (at_roland_garros(X) => (female(X) | male(X)))).

% Premise 5: All male tennis players at Roland Garros in 2022 lost to Rafael Nadal.
fof(premise_5, axiom, ! [X] : (male(X) => lost_to_nadal(X))).

% Premise 6: If Coco Gauff is ranked highly by the Women's Tennis Association or lost to Rafael Nadal, then Coco Gauff is not a male tennis player at Roland Garros 2022.
fof(premise_6, axiom, (ranked_high(coco_gauff) | lost_to_nadal(coco_gauff)) => ~male(coco_gauff)).

% Premise 7: Coco Gauff is at Roland Garros 2022.
fof(premise_7, axiom, at_roland_garros(coco_gauff)).

% Conclusion: Coco Gauff is not both a player who lost to Iga Swiatek at Roland Garros 2022 and one of the most active players in major tennis.
fof(conclusion, conjecture, ~(lost_to_swiatek(coco_gauff) & most_active(coco_gauff))).