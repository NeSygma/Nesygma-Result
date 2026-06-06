fof(rule_ranked_active, axiom, ! [X] : (ranked_highly(X) => active_major(X))).
fof(rule_female_or_male, axiom, ! [X] : (at_roland_garros(X) => (female(X) | male(X)))).
fof(rule_male_lost_nadal, axiom, ! [X] : ((at_roland_garros(X) & male(X)) => lost_to_nadal(X))).
fof(rule_female_lost_Iga, axiom, ! [X] : ((at_roland_garros(X) & female(X)) => lost_to_Iga(X))).
fof(rule_lost_Iga_ranked, axiom, ! [X] : ((at_roland_garros(X) & lost_to_Iga(X)) => ranked_highly(X))).
fof(rule_ranked_or_lost_nadal_not_male, axiom, ((ranked_highly(coco_gauff) | lost_to_nadal(coco_gauff)) => ~male(coco_gauff))).
fof(fact_coco_at_roland, axiom, at_roland_garros(coco_gauff)).
fof(goal, conjecture, active_major(coco_gauff)).