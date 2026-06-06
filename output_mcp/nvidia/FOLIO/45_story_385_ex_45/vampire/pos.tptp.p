% Axioms
fof(axiom_ranked_impl_most_active, axiom, ! [X] : (ranked_highly(X) => most_active(X))).
fof(axiom_lost_to_iga_impl_ranked, axiom, ! [X] : (lost_to_iga(X) => ranked_highly(X))).
fof(axiom_female_lost_to_iga, axiom, ! [X] : (female(X) & at_rg2022(X) => lost_to_iga(X))).
fof(axiom_player_gender_partition, axiom, ! [X] : (at_rg2022(X) => (female(X) | male(X))) ).
fof(axiom_male_lost_to_rafael, axiom, ! [X] : (male(X) & at_rg2022(X) => lost_to_rafael(X))).
fof(axiom_coco_conditional, axiom, ((ranked_highly(coco_gauff) | lost_to_rafael(coco_gauff)) => ~(male(coco_gauff) & at_rg2022(coco_gauff)))).
fof(axiom_coco_at_rg2022, axiom, at_rg2022(coco_gauff)).
fof(axiom_distinct_constants, axiom, (coco_gauff != iga_swiatek & coco_gauff != rafael_nadal & iga_swiatek != rafael_nadal)).
fof(conjecture, conjecture, ~(lost_to_iga(coco_gauff) & most_active(coco_gauff))).