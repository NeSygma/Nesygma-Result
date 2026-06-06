% Negative version: negated conclusion as conjecture
% Original conclusion: ~(lost_to_swiatek(coco_gauff) & most_active(coco_gauff))
% Negated conclusion: ~~(lost_to_swiatek(coco_gauff) & most_active(coco_gauff))
% i.e., lost_to_swiatek(coco_gauff) & most_active(coco_gauff)

fof(distinct, axiom, $true).

% Premise 1
fof(premise_1, axiom, ! [X] : (ranked_high(X) => most_active(X))).

% Premise 2
fof(premise_2, axiom, ! [X] : (lost_to_swiatek(X) => ranked_high(X))).

% Premise 3
fof(premise_3, axiom, ! [X] : (female(X) => lost_to_swiatek(X))).

% Premise 4
fof(premise_4, axiom, ! [X] : (at_roland_garros(X) => (female(X) | male(X)))).

% Premise 5
fof(premise_5, axiom, ! [X] : (male(X) => lost_to_nadal(X))).

% Premise 6
fof(premise_6, axiom, (ranked_high(coco_gauff) | lost_to_nadal(coco_gauff)) => ~male(coco_gauff)).

% Premise 7
fof(premise_7, axiom, at_roland_garros(coco_gauff)).

% Negated conclusion: Coco Gauff lost to Iga Swiatek AND is one of the most active players
fof(neg_conclusion, conjecture, (lost_to_swiatek(coco_gauff) & most_active(coco_gauff))).