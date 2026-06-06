fof(distinct_constants, axiom, (coco != iga & coco != rafa & iga != rafa)).

fof(premise_1, axiom, ! [X] : (ranked_highly(X) => most_active(X))).
fof(premise_2, axiom, ! [X] : (lost_to_iga(X) => ranked_highly(X))).
fof(premise_3, axiom, ! [X] : (female(X) => lost_to_iga(X))).
fof(premise_4, axiom, ! [X] : (at_rg2022(X) => (female(X) | male(X)))).
fof(premise_5, axiom, ! [X] : (male(X) => lost_to_rafael(X))).
fof(premise_6, axiom, (ranked_highly(coco) | lost_to_rafael(coco)) => ~male(coco)).
fof(premise_7, axiom, at_rg2022(coco)).

fof(conclusion, conjecture, ~(lost_to_iga(coco) & most_active(coco))).