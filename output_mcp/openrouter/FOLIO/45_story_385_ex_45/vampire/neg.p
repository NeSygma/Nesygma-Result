% Negative conjecture: both lost to Iga and most active
fof(distinct1, axiom, coco_gauff != iga_swiatek).
fof(distinct2, axiom, coco_gauff != rafael_nadal).
fof(distinct3, axiom, iga_swiatek != rafael_nadal).

% Premise 1
fof(premise1, axiom, ! [X] : (ranked_highly(X) => most_active(X))).
% Premise 2
fof(premise2, axiom, ! [X] : (lost_to(X, iga_swiatek) => ranked_highly(X))).
% Premise 3
fof(premise3, axiom, ! [X] : ((female(X) & at_roland_garros_2022(X)) => lost_to(X, iga_swiatek))).
% Premise 4
fof(premise4, axiom, ! [X] : (at_roland_garros_2022(X) => (female(X) | male(X)))).
% Premise 5
fof(premise5, axiom, ! [X] : ((male(X) & at_roland_garros_2022(X)) => lost_to(X, rafael_nadal))).
% Premise 6
fof(premise6, axiom, ((ranked_highly(coco_gauff) | lost_to(coco_gauff, rafael_nadal)) => (~male(coco_gauff) | ~at_roland_garros_2022(coco_gauff)))).
% Premise 7
fof(premise7, axiom, at_roland_garros_2022(coco_gauff)).

% Goal (negative)
fof(goal, conjecture, (lost_to(coco_gauff, iga_swiatek) & most_active(coco_gauff))).