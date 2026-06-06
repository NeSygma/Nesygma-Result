% Negative version: negated conclusion as conjecture
% Conclusion: Coco Gauff has NOT lost to Rafael Nadal.

fof(distinct, axiom, (coco != iga & coco != rafael & iga != rafael)).

fof(premise1, axiom, ! [X] : (ranked_high(X) => most_active(X))).

fof(premise2, axiom, ! [X] : (lost_to_iga(X) => ranked_high(X))).

fof(premise3, axiom, ! [X] : ((female(X) & at_rg2022(X)) => lost_to_iga(X))).

fof(premise4, axiom, ! [X] : (at_rg2022(X) => (female(X) | male(X)))).

fof(premise5, axiom, ! [X] : ((male(X) & at_rg2022(X)) => lost_to_rafael(X))).

fof(premise6, axiom, (ranked_high(coco) | lost_to_rafael(coco)) => ~(male(coco) & at_rg2022(coco))).

fof(premise7, axiom, at_rg2022(coco)).

% Negated conclusion: Coco Gauff has NOT lost to Rafael Nadal.
fof(goal, conjecture, ~lost_to_rafael(coco)).