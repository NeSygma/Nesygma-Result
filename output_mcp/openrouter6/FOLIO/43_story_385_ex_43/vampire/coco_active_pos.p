% Positive TPTP file: conclusion as conjecture
fof(premise_1, axiom, ! [X] : (ranked_highly_wta(X) => most_active_major(X))).
fof(premise_2, axiom, ! [X] : (lost_to_iga(X) => ranked_highly_wta(X))).
fof(premise_3, axiom, ! [X] : (female(X) => lost_to_iga(X))).
fof(premise_4, axiom, ! [X] : (at_rg2022(X) => (female(X) | male(X)))).
fof(premise_5, axiom, ! [X] : (male(X) => lost_to_rafael(X))).
fof(premise_6, axiom, (ranked_highly_wta(coco) | lost_to_rafael(coco)) => ~male(coco)).
fof(premise_7, axiom, at_rg2022(coco)).
fof(goal, conjecture, most_active_major(coco)).