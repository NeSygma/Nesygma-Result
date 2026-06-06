% Positive version: original conclusion as conjecture
% Conclusion: Coco Gauff has lost to Rafael Nadal.

% Predicates:
% ranked_high(X) - X is ranked highly by the Women's Tennis Association
% most_active(X) - X is one of the most active players in major tennis
% lost_to_iga(X) - X lost to Iga Swiatek at Roland Garros 2022
% female(X) - X is a female tennis player
% male(X) - X is a male tennis player
% at_rg2022(X) - X is a tennis player at Roland Garros 2022
% lost_to_rafael(X) - X lost to Rafael Nadal

% Constants:
% coco - Coco Gauff

fof(distinct, axiom, (coco != iga & coco != rafael & iga != rafael)).

% Premise 1: If someone is ranked highly by the WTA, then they are one of the most active players in major tennis.
fof(premise1, axiom, ! [X] : (ranked_high(X) => most_active(X))).

% Premise 2: Everyone who lost to Iga Swiatek at Roland Garros 2022 is ranked highly by the WTA.
fof(premise2, axiom, ! [X] : (lost_to_iga(X) => ranked_high(X))).

% Premise 3: All female tennis players at Roland Garros 2022 lost to Iga Swiatek.
fof(premise3, axiom, ! [X] : ((female(X) & at_rg2022(X)) => lost_to_iga(X))).

% Premise 4: All tennis players at Roland Garros 2022 are either female or male.
fof(premise4, axiom, ! [X] : (at_rg2022(X) => (female(X) | male(X)))).

% Premise 5: All male tennis players at Roland Garros in 2022 lost to Rafael Nadal.
fof(premise5, axiom, ! [X] : ((male(X) & at_rg2022(X)) => lost_to_rafael(X))).

% Premise 6: If Coco Gauff is ranked highly by the WTA or lost to Rafael Nadal, then Coco Gauff is not a male tennis player at Roland Garros 2022.
fof(premise6, axiom, (ranked_high(coco) | lost_to_rafael(coco)) => ~(male(coco) & at_rg2022(coco))).

% Premise 7: Coco Gauff is at Roland Garros 2022.
fof(premise7, axiom, at_rg2022(coco)).

% Conclusion: Coco Gauff has lost to Rafael Nadal.
fof(goal, conjecture, lost_to_rafael(coco)).