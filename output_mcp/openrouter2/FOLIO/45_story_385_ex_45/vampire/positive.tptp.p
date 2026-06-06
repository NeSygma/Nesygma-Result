fof(distinct, axiom, (coco != iga & coco != rafael & iga != rafael)).
fof(at_rg2022_coco, axiom, at_rg2022(coco)).
fof(premise1, axiom, ! [X] : (ranked_highly_by_wta(X) => active_major(X))).
fof(premise2, axiom, ! [X] : (lost_to_iga(X) => ranked_highly_by_wta(X))).
fof(premise3, axiom, ! [X] : (female(X) => lost_to_iga(X))).
fof(premise4, axiom, ! [X] : (at_rg2022(X) => (female(X) | male(X)))).
fof(premise5, axiom, ! [X] : (male(X) => lost_to_nadal(X))).
fof(premise6, axiom, ((ranked_highly_by_wta(coco) | lost_to_nadal(coco)) => ~male(coco))).
fof(conjecture, conjecture, ~ (lost_to_iga(coco) & active_major(coco))).