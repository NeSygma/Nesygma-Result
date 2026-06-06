fof(axiom_1, axiom, ! [X] : (ranked_highly_by_wta(X) => most_active(X))).
fof(axiom_2, axiom, ! [X] : (lost_to_iga(X) => ranked_highly_by_wta(X))).
fof(axiom_3, axiom, ! [X] : ((female(X) & player_RG(X)) => lost_to_iga(X))).
fof(axiom_4, axiom, ! [X] : (player_RG(X) => (female(X) | male(X)))).
fof(axiom_5, axiom, ! [X] : ((male(X) & player_RG(X)) => lost_to_rafael_nadal(X))).
fof(axiom_6, axiom, (ranked_highly_by_wta(coco_gauff) | lost_to_rafael_nadal(coco_gauff)) => ~(male(coco_gauff) & player_RG(coco_gauff))).
fof(axiom_7, axiom, player_RG(coco_gauff)).
fof(conclusion, conjecture, lost_to_rafael_nadal(coco_gauff)).